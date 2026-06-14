#!/usr/bin/env python3
"""
commit-bot: git diff를 분석해 커밋 메시지를 자동 생성하는 CLI 도구
=================================================================
사용법:
  python commit_bot.py              # staged 변경사항 자동 분석
  python commit_bot.py --dry-run    # 커밋하지 않고 메시지만 출력
  python commit_bot.py --push       # 커밋 후 push까지
  python commit_bot.py --lang en    # 영어 커밋 메시지
"""

import subprocess
import sys
import re
import os
import argparse
from pathlib import Path

# ================================================================
# 1. Git 유틸리티
# ================================================================

def run_git(args: list[str]) -> tuple[str, int]:
    """git 명령 실행 후 (stdout, returncode) 반환"""
    result = subprocess.run(
        ['git'] + args,
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    return result.stdout.strip(), result.returncode


def get_staged_diff() -> str:
    """staged 파일의 diff 반환 (git add 된 것만)"""
    diff, code = run_git(['diff', '--cached'])
    if code != 0 or not diff:
        return ''
    return diff


def get_staged_files() -> list[dict]:
    """
    staged 파일 목록과 상태 반환
    상태 코드: A=추가, M=수정, D=삭제, R=이름변경
    """
    out, _ = run_git(['diff', '--cached', '--name-status'])
    files = []
    for line in out.splitlines():
        parts = line.split('\t')
        if len(parts) >= 2:
            status = parts[0][0]  # 첫 글자만 (R100 → R)
            path = parts[-1]
            files.append({'status': status, 'path': path})
    return files


def get_current_branch() -> str:
    branch, _ = run_git(['rev-parse', '--abbrev-ref', 'HEAD'])
    return branch or 'main'


def check_staged_exists() -> bool:
    """staged 변경사항이 있는지 확인"""
    _, code = run_git(['diff', '--cached', '--quiet'])
    return code != 0  # non-zero = staged 있음


# ================================================================
# 2. Diff 분석기
# ================================================================

class DiffAnalyzer:
    """
    git diff 텍스트를 파싱해 변경 유형과 키워드를 추출
    추출 결과로 Transformer 모델의 입력 토큰(src_words) 생성
    """

    # 파일 확장자 → 영역 분류
    EXT_MAP = {
        '.py': 'backend', '.java': 'backend', '.go': 'backend', '.kt': 'backend',
        '.js': 'frontend', '.ts': 'frontend', '.jsx': 'frontend', '.tsx': 'frontend',
        '.vue': 'frontend', '.html': 'frontend', '.css': 'frontend',
        '.sql': 'database', '.xml': 'config', '.yml': 'config', '.yaml': 'config',
        '.json': 'config', '.md': 'docs', '.txt': 'docs',
        '.sh': 'script', '.bat': 'script',
    }

    # 코드 패턴 → 변경 유형 힌트
    PATTERNS = {
        r'\bfix\b|\bbug\b|\berror\b|\bexception\b|\bnull\b': '버그',
        r'\btest\b|\bspec\b|\bassert\b|\bmock\b': '테스트',
        r'\brefactor\b|\bclean\b|\bimprove\b|\boptimiz': '리팩토링',
        r'\badd\b|\bnew\b|\bcreate\b|\bfeature\b|\bimplement': '기능추가',
        r'\bdelete\b|\bremove\b|\bdrop\b': '삭제',
        r'\bupdate\b|\bmodify\b|\bchange\b|\bedit\b': '수정',
        r'\bdoc\b|\bcomment\b|\breadme\b': '문서',
        r'\bsecurity\b|\bauth\b|\bpassword\b|\btoken\b': '보안',
        r'\bperformance\b|\bcache\b|\bindex\b|\bquery\b': '성능',
    }

    def analyze(self, diff: str, files: list[dict]) -> dict:
        """diff와 파일 목록으로 변경 분석 결과 반환"""
        result = {
            'change_types': [],   # 변경 유형 목록
            'areas': set(),       # 변경된 영역 (frontend/backend/...)
            'file_count': len(files),
            'additions': 0,       # 추가된 라인 수
            'deletions': 0,       # 삭제된 라인 수
            'files': files,
        }

        # 추가/삭제 라인 수 집계
        for line in diff.splitlines():
            if line.startswith('+') and not line.startswith('+++'):
                result['additions'] += 1
            elif line.startswith('-') and not line.startswith('---'):
                result['deletions'] += 1

        # 파일 상태별 분류
        status_counts = {}
        for f in files:
            s = f['status']
            status_counts[s] = status_counts.get(s, 0) + 1
            ext = Path(f['path']).suffix.lower()
            area = self.EXT_MAP.get(ext, 'etc')
            result['areas'].add(area)

        # 파일 상태 → 변경 유형
        if status_counts.get('A', 0) > 0:
            result['change_types'].append('추가')
        if status_counts.get('M', 0) > 0:
            result['change_types'].append('수정')
        if status_counts.get('D', 0) > 0:
            result['change_types'].append('삭제')
        if status_counts.get('R', 0) > 0:
            result['change_types'].append('이름변경')

        # diff 내용 패턴 매칭으로 힌트 보강
        diff_lower = diff.lower()
        hints = set()
        for pattern, hint in self.PATTERNS.items():
            if re.search(pattern, diff_lower):
                hints.add(hint)
        result['hints'] = hints

        return result


# ================================================================
# 3. 커밋 메시지 생성기
# ================================================================

class CommitMessageGenerator:
    """
    분석 결과를 받아 Conventional Commits 형식의 메시지 생성
    
    [Conventional Commits 형식]
    <type>(<scope>): <subject>
    
    type: feat / fix / refactor / docs / test / chore / perf / style
    scope: 변경된 영역 (선택)
    subject: 변경 요약
    """

    # 힌트 → Conventional Commits type
    HINT_TO_TYPE = {
        '버그': 'fix',
        '테스트': 'test',
        '리팩토링': 'refactor',
        '기능추가': 'feat',
        '삭제': 'chore',
        '수정': 'fix',
        '문서': 'docs',
        '보안': 'fix',
        '성능': 'perf',
    }

    # 파일 상태 → 영어 동사
    STATUS_VERB = {
        '추가': 'add',
        '수정': 'update',
        '삭제': 'remove',
        '이름변경': 'rename',
    }

    def generate(self, analysis: dict, lang: str = 'en') -> str:
        hints = analysis['hints']
        change_types = analysis['change_types']
        areas = analysis['areas']
        files = analysis['files']
        additions = analysis['additions']
        deletions = analysis['deletions']

        # type 결정 (힌트 우선, 없으면 파일 상태 기반)
        commit_type = 'chore'
        for hint in ['버그', '보안', '기능추가', '리팩토링', '테스트', '성능', '문서', '수정']:
            if hint in hints:
                commit_type = self.HINT_TO_TYPE[hint]
                break
        if commit_type == 'chore' and '추가' in change_types:
            commit_type = 'feat'

        # scope 결정
        scope = ''
        if len(areas) == 1:
            scope = list(areas)[0]
        elif areas:
            scope = '/'.join(sorted(areas)[:2])

        # subject 생성
        file_count = len(files)
        if file_count == 1:
            fname = Path(files[0]['path']).name
            verb = self.STATUS_VERB.get(change_types[0] if change_types else '수정', 'update')
            subject = f"{verb} {fname}"
        else:
            verb = self.STATUS_VERB.get(change_types[0] if change_types else '수정', 'update')
            subject = f"{verb} {file_count} files"
            if hints:
                top_hint = next(iter(hints))
                subject += f" ({top_hint})"

        # body (변경 통계)
        body_lines = [
            f"",
            f"Changes: +{additions} -{deletions} lines in {file_count} file(s)",
        ]
        if files:
            body_lines.append("Modified files:")
            for f in files[:5]:  # 최대 5개만
                body_lines.append(f"  {f['status']} {f['path']}")
            if len(files) > 5:
                body_lines.append(f"  ... and {len(files)-5} more")

        # 최종 조립
        header = f"{commit_type}"
        if scope:
            header += f"({scope})"
        header += f": {subject}"

        return header + '\n'.join(body_lines)


# ================================================================
# 4. Transformer 기반 키워드 번역 (선택적 사용)
# ================================================================

def try_model_translate(src_words: list[str], model_path: str = "commit_model.pt") -> list[str] | None:
    """
    학습된 Transformer 모델이 있으면 키워드 번역 시도
    없으면 None 반환 → 룰 기반 생성기로 폴백
    """
    if not os.path.exists(model_path):
        return None
    try:
        import torch
        # transformer_model.py의 Seq2SeqTransformer import
        sys.path.insert(0, os.path.dirname(__file__))
        from transformer_model import Seq2SeqTransformer
        model = Seq2SeqTransformer.load(model_path)
        result = model.translate(src_words)
        return result if result else None
    except Exception as e:
        print(f"⚠️  모델 로드 실패: {e}", file=sys.stderr)
        return None


# ================================================================
# 5. CLI 메인
# ================================================================

def main():
    parser = argparse.ArgumentParser(
        description='commit-bot: git diff 분석 후 커밋 메시지 자동 생성',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python commit_bot.py              # 자동 분석 + 커밋
  python commit_bot.py --dry-run    # 커밋 메시지만 출력
  python commit_bot.py --push       # 커밋 + push
  python commit_bot.py --no-model   # 룰 기반만 사용
        """
    )
    parser.add_argument('--dry-run', action='store_true', help='커밋하지 않고 메시지만 출력')
    parser.add_argument('--push', action='store_true', help='커밋 후 push')
    parser.add_argument('--lang', choices=['en', 'ko'], default='en', help='메시지 언어')
    parser.add_argument('--no-model', action='store_true', help='Transformer 모델 사용 안 함')
    parser.add_argument('--model', default='commit_model.pt', help='모델 파일 경로')
    args = parser.parse_args()

    print("🤖 commit-bot 시작")
    print("=" * 50)

    # Git 저장소 확인
    _, code = run_git(['rev-parse', '--is-inside-work-tree'])
    if code != 0:
        print("❌ git 저장소가 아닙니다.")
        sys.exit(1)

    # Staged 변경사항 확인
    if not check_staged_exists():
        print("⚠️  staged 변경사항이 없습니다. 먼저 git add 하세요.")
        sys.exit(0)

    # diff & 파일 목록 수집
    diff = get_staged_diff()
    files = get_staged_files()
    branch = get_current_branch()

    print(f"📁 변경 파일: {len(files)}개  |  브랜치: {branch}")
    for f in files:
        print(f"   {f['status']} {f['path']}")

    # diff 분석
    analyzer = DiffAnalyzer()
    analysis = analyzer.analyze(diff, files)
    print(f"\n🔍 분석 결과:")
    print(f"   변경 유형: {analysis['change_types']}")
    print(f"   영역:     {analysis['areas']}")
    print(f"   힌트:     {analysis['hints']}")
    print(f"   +{analysis['additions']} / -{analysis['deletions']} 라인")

    # 커밋 메시지 생성
    # 1순위: Transformer 모델 (학습된 경우)
    model_keywords = None
    if not args.no_model:
        # 분석 결과의 힌트를 한글 키워드로 변환해서 모델에 입력
        src_words = list(analysis['hints'])[:3] if analysis['hints'] else list(analysis['change_types'])[:2]
        if src_words:
            print(f"\n🧠 모델 번역 시도: {src_words}")
            model_keywords = try_model_translate(src_words, args.model)
            if model_keywords:
                print(f"   → {model_keywords}")

    # 2순위: 룰 기반 생성기
    generator = CommitMessageGenerator()
    commit_msg = generator.generate(analysis, args.lang)

    # 모델 결과가 있으면 subject 앞에 붙임
    if model_keywords:
        first_line = commit_msg.split('\n')[0]
        rest = '\n'.join(commit_msg.split('\n')[1:])
        type_scope = first_line.split(':')[0]
        model_subject = ' '.join(model_keywords)
        commit_msg = f"{type_scope}: {model_subject}\n{rest}"

    print(f"\n📝 생성된 커밋 메시지:")
    print("-" * 40)
    print(commit_msg)
    print("-" * 40)

    if args.dry_run:
        print("\n🔎 dry-run 모드: 커밋하지 않음")
        return

    # 사용자 확인
    print("\n이 메시지로 커밋하시겠습니까? [y/N/e(직접입력)] ", end='')
    choice = input().strip().lower()

    if choice == 'e':
        print("커밋 메시지를 직접 입력하세요:")
        commit_msg = input().strip()
    elif choice != 'y':
        print("❌ 취소")
        return

    # 커밋 실행
    _, code = run_git(['commit', '-m', commit_msg])
    if code == 0:
        print(f"✅ 커밋 완료!")
        hash_out, _ = run_git(['rev-parse', '--short', 'HEAD'])
        print(f"   커밋 해시: {hash_out}")
    else:
        print("❌ 커밋 실패")
        sys.exit(1)

    # push
    if args.push:
        print(f"\n🚀 push 중... (branch: {branch})")
        out, code = run_git(['push', 'origin', branch])
        if code == 0:
            print("✅ push 완료!")
        else:
            print(f"❌ push 실패:\n{out}")
            sys.exit(1)


if __name__ == '__main__':
    main()
