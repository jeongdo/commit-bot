# ============================================================================
# 025 - main_function (__name__과 진입점)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. __name__의 동작 원리를 정확히 이해한다
#   2. if __name__ == "__main__" 패턴의 이유와 이점을 안다
#   3. main() 함수를 올바르게 설계한다 (테스트 가능, 종료 코드 반환)
#   4. __main__.py 로 패키지를 실행 가능하게 만드는 법을 안다
#
# [왜 필요한가]
#   - Python 파일은 모듈과 실행 파일로 이중 역할 가능
#   - if __name__ 없이 최상위 코드 작성 시 import할 때도 실행됨
#   - sys.exit(main()) 패턴: 종료 코드를 OS에 전달
#
# [Java 비교]
#   Java  : public static void main(String[] args) — 언어 레벨 진입점
#           import 시 main 실행 없음 (클래스 정의만 로드)
#   Python: if __name__ == "__main__" — 규칙 기반 진입점
#           import 시 최상위 코드 실행! → 반드시 분리 필요
# ============================================================================

import sys
import argparse
import time

# ── LEVEL 1: __name__ 기본 ──────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: __name__")
print("=" * 50)

# __name__: 현재 모듈의 이름
# - 직접 실행 시: "__main__"
# - import될 때 : 파일명 (확장자 없음)
print(f"현재 __name__ = {__name__!r}")

# 다른 속성들
print(f"__file__     = {__file__!r}")
print(f"__doc__      = {__doc__!r}")
print(f"__package__  = {__package__!r}")

# ── LEVEL 2: if __name__ == "__main__" 왜 필요한가 ───────────────────────────

print("\nLEVEL 2: import 시 최상위 코드 실행 문제")
print("-" * 40)

# 이런 코드가 모듈 최상위에 있으면:
# expensive_computation()    ← import 시마다 실행됨!
# connect_to_database()      ← import 시마다 연결!

# 올바른 구조:
def expensive_computation():
    """비용이 큰 연산"""
    time.sleep(0.001)
    return sum(range(10000))

def connect_to_database(host="localhost"):
    """DB 연결 (시뮬레이션)"""
    return f"연결됨: {host}"

# 비즈니스 로직은 함수/클래스로 (import 시 실행 안 됨)
def process_data(data: list) -> dict:
    return {"count": len(data), "sum": sum(data)}

# 이 블록만 직접 실행 시 실행됨
if __name__ == "__main__":
    result = expensive_computation()
    print(f"  expensive_computation() = {result}")
    conn = connect_to_database()
    print(f"  connect_to_database() = {conn}")

# ── LEVEL 3: main() 함수 설계 ───────────────────────────────────────────────

print("\nLEVEL 3: main() 함수 설계")
print("-" * 40)

def parse_args(argv=None):
    """CLI 인수 파싱 — 테스트 시 argv 주입 가능"""
    parser = argparse.ArgumentParser(
        description="데이터 처리 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input",
        help="입력 파일 경로"
    )
    parser.add_argument(
        "-o", "--output",
        default="stdout",
        help="출력 대상 (기본: stdout)"
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="처리 행 수 제한"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="상세 출력 모드"
    )
    return parser.parse_args(argv)

def main(argv=None) -> int:
    """
    메인 진입점 — 반환값: 종료 코드 (0=성공, 1+=오류)

    Args:
        argv: CLI 인수 (None이면 sys.argv 사용)

    Returns:
        int: OS 종료 코드
    """
    try:
        args = parse_args(argv)
    except SystemExit as e:
        return int(e.code)

    if args.verbose:
        print(f"  [verbose] 입력: {args.input}")
        print(f"  [verbose] 출력: {args.output}")
        print(f"  [verbose] 제한: {args.limit}")

    # 실제 처리 로직
    try:
        # 여기서 처리 수행
        data = list(range(20))   # 시뮬레이션
        if args.limit:
            data = data[:args.limit]
        result = process_data(data)
        print(f"  결과: {result}")
        return 0   # 성공
    except FileNotFoundError as e:
        print(f"  오류: 파일 없음 — {e}", file=sys.stderr)
        return 1   # 오류
    except Exception as e:
        print(f"  예상치 못한 오류: {e}", file=sys.stderr)
        return 2

# 테스트 시 argv 직접 주입 가능!
exit_code = main(["data.csv", "--limit", "5", "-v"])
print(f"  종료 코드: {exit_code}")

exit_code = main(["data.csv", "--limit", "10"])
print(f"  종료 코드: {exit_code}")

# ── LEVEL 4: if __name__ == "__main__" 올바른 구조 ──────────────────────────

print("\nLEVEL 4: 올바른 파일 구조")
print("-" * 40)

print("""
# my_tool.py 올바른 구조:

# 1. 임포트
import sys
import argparse

# 2. 상수 (모듈 레벨, 변경 안 함)
VERSION = "1.0.0"
DEFAULT_TIMEOUT = 30

# 3. 유틸리티 함수 (import 시 실행 안 됨, 다른 모듈에서 재사용 가능)
def parse_data(raw): ...
def validate(data): ...
def process(data, config): ...

# 4. 클래스
class DataProcessor: ...

# 5. main() — 진입점 로직만
def main(argv=None) -> int:
    args = parse_args(argv)
    ...
    return 0

# 6. 진입점
if __name__ == "__main__":
    sys.exit(main())   # 종료 코드 OS 전달
""")

# ── LEVEL 4: sys.exit()와 종료 코드 ─────────────────────────────────────────

print("\nLEVEL 4: sys.exit()와 종료 코드")
print("-" * 40)

# 종료 코드 의미 (Unix 관례)
exit_codes = {
    0: "성공",
    1: "일반 오류",
    2: "CLI 인수 오류",
    126: "명령 실행 불가",
    127: "명령 없음",
    130: "Ctrl+C 중단",
}
print("종료 코드 의미:")
for code, meaning in exit_codes.items():
    print(f"  {code}: {meaning}")

# sys.exit()는 SystemExit 예외를 발생시킴 → try-except로 잡을 수 있음
print()
try:
    # sys.exit(0)   # 실제 실행하면 프로세스 종료
    raise SystemExit(0)   # 테스트용 시뮬레이션
except SystemExit as e:
    print(f"SystemExit 잡음: code={e.code}")

# ── LEVEL 5: __main__.py — 패키지 실행 ──────────────────────────────────────

print("\nLEVEL 5: 패키지 실행 구조")
print("-" * 40)

print("""
# 패키지를 실행 가능하게: python -m mypackage

# mypackage/
#   __init__.py
#   __main__.py   ← python -m mypackage 시 이 파일 실행
#   core.py
#   utils.py

# mypackage/__main__.py:
import sys
from .core import main

if __name__ == "__main__":
    sys.exit(main())

# 실행:
# python -m mypackage
# python -m mypackage --help
# python -m mypackage input.csv -o output.csv
""")

# 실제 예시: Python 내장 모듈들
print("Python 내장 패키지 실행 예시:")
print("  python -m http.server 8080")
print("  python -m json.tool data.json")
print("  python -m timeit 'sum(range(1000))'")
print("  python -m cProfile my_script.py")
print("  python -m pytest tests/")

# ============================================================================
# [주의사항]
#   1. 최상위 코드(함수/클래스 밖)는 import 시에도 실행됨 → 분리 필수
#   2. main()은 반드시 int(종료코드) 반환 → sys.exit(main()) 패턴
#   3. main(argv=None) 으로 argv 주입 → 단위 테스트 가능
#   4. __file__ 은 실행 위치에 따라 상대/절대 경로 혼재 → Path(__file__).resolve()
#   5. if __name__ 블록에는 최소한의 코드만 → main() 호출 정도
#
# ★ PART 01 모든 파일 완료! → PART 02: Sequence & Collection
# ============================================================================
