# ============================================================================
# 009 - input() (사용자 입력)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. input()의 동작 원리와 한계를 이해한다
#   2. 타입 변환, 다중 입력, 입력 검증 패턴을 익힌다
#   3. 실무에서 input() 대신 사용하는 argparse/환경변수를 안다
#
# [왜 필요한가]
#   - 모든 CLI 스크립트의 기본 입력 수단
#   - "항상 str 반환" 규칙을 잊으면 TypeError 발생
#   - 입력 검증 패턴은 모든 프로그램에 필요
#
# [Java 비교]
#   Java  : Scanner sc = new Scanner(System.in);
#           int n = sc.nextInt();   → 타입 지정 읽기
#   Python: n = int(input())        → 항상 str, 변환은 개발자 몫
# ============================================================================

import sys
import io

# ─── 테스트용 stdin 시뮬레이션 ───────────────────────────────────────────────
def simulate(*lines):
    """여러 줄 입력을 시뮬레이션 (실제 실행시엔 직접 input() 사용)"""
    sys.stdin = io.StringIO("\n".join(lines) + "\n")

def restore():
    sys.stdin = sys.__stdin__

# ── LEVEL 1: input() 기초 ───────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: input() 기초")
print("=" * 50)

# input()은 항상 str 반환!
simulate("Alice")
name = input("이름을 입력하세요: ")  # 시뮬레이션: "Alice"
restore()
print(f"name = {name!r}, type = {type(name).__name__}")   # str

# 타입 변환 필수
simulate("25")
age_str = input("나이: ")
restore()
age = int(age_str)         # str → int 명시적 변환
print(f"age = {age}, age + 1 = {age + 1}")

# 한 줄로 압축 (경쟁 프로그래밍 스타일)
simulate("100")
n = int(input("숫자: "))
restore()
print(f"n * 2 = {n * 2}")

# ── LEVEL 2: 다양한 입력 패턴 ───────────────────────────────────────────────

print("\nLEVEL 2: 다양한 입력 패턴")
print("-" * 40)

# 패턴 1: 공백으로 구분된 여러 값
simulate("1 2 3 4 5")
nums = list(map(int, input("숫자들: ").split()))
restore()
print(f"nums = {nums}, sum = {sum(nums)}")

# 패턴 2: 여러 변수 언패킹
simulate("10 20")
a, b = map(int, input("두 수: ").split())
restore()
print(f"a={a}, b={b}, a+b={a+b}")

# 패턴 3: float 입력
simulate("3.14")
pi_approx = float(input("원주율 근사값: "))
restore()
print(f"pi ≈ {pi_approx}, 오차 = {abs(pi_approx - 3.14159265358979):.6f}")

# 패턴 4: 여러 줄 입력 (EOF까지)
simulate("line1", "line2", "line3")
lines = []
while True:
    try:
        line = input()
        lines.append(line)
    except EOFError:
        break
restore()
print(f"입력된 줄: {lines}")

# ── LEVEL 3: 입력 검증 패턴 ─────────────────────────────────────────────────

print("\nLEVEL 3: 입력 검증 패턴")
print("-" * 40)

def get_int(prompt, min_val=None, max_val=None, max_retry=3):
    """검증 포함 정수 입력 — 실무 패턴"""
    retry = 0
    while retry < max_retry:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"  {min_val} 이상이어야 합니다")
                retry += 1; continue
            if max_val is not None and value > max_val:
                print(f"  {max_val} 이하이어야 합니다")
                retry += 1; continue
            return value
        except ValueError:
            print(f"  정수를 입력해주세요")
            retry += 1
    raise ValueError(f"{max_retry}회 실패")

def get_choice(prompt, choices):
    """선택지 입력 — 실무 패턴"""
    choice_str = "/".join(choices)
    while True:
        val = input(f"{prompt} [{choice_str}]: ").strip().lower()
        if val in choices:
            return val
        print(f"  {choice_str} 중 하나를 입력하세요")

# 시뮬레이션으로 테스트
simulate("abc", "200", "25")
try:
    age = get_int("나이 (0-150): ", 0, 150)
    print(f"입력된 나이: {age}")
except ValueError as e:
    print(f"입력 실패: {e}")
restore()

simulate("y")
answer = get_choice("계속하시겠습니까?", ["y", "n"])
restore()
print(f"선택: {answer}")

# ── LEVEL 4: 실무 대안 — argparse ────────────────────────────────────────────

print("\nLEVEL 4: 실무 대안 — argparse")
print("-" * 40)

import argparse

# CLI 도구 인수 처리 (input() 대신 사용)
parser = argparse.ArgumentParser(
    description="파일 처리 도구",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
사용 예시:
  python script.py input.csv -o output.csv --format json
  python script.py data.csv --limit 100 --verbose
"""
)
parser.add_argument("input",              help="입력 파일 경로")
parser.add_argument("-o", "--output",     default="output.txt", help="출력 파일 (기본: output.txt)")
parser.add_argument("--format",           choices=["csv","json","xml"], default="csv")
parser.add_argument("--limit", type=int,  default=None, help="처리 행 수 제한")
parser.add_argument("-v", "--verbose",    action="store_true", help="상세 출력")

# 테스트용 시뮬레이션 (실제로는 sys.argv에서 읽음)
args = parser.parse_args(["data.csv", "-o", "result.json",
                           "--format", "json", "--limit", "100", "-v"])
print(f"input  : {args.input}")
print(f"output : {args.output}")
print(f"format : {args.format}")
print(f"limit  : {args.limit}")
print(f"verbose: {args.verbose}")

# ── LEVEL 4: 실무 대안 — 환경변수 / 설정 파일 ─────────────────────────────

print("\nLEVEL 4: 실무 대안 — 환경변수 / 설정")
print("-" * 40)

import os, json

# 환경변수로 설정 주입 (12-Factor App 방식)
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DEBUG",   "false")

db_host = os.environ.get("DB_HOST", "localhost")
db_port = int(os.environ.get("DB_PORT", "5432"))
debug   = os.environ.get("DEBUG", "false").lower() == "true"

print(f"DB: {db_host}:{db_port}, debug={debug}")

# 설정 파일 (JSON)
config_data = {"max_connections": 10, "timeout": 30, "retry": 3}
config_json = json.dumps(config_data, indent=2)
config = json.loads(config_json)
print(f"설정: max_conn={config['max_connections']}, timeout={config['timeout']}")

# ── LEVEL 5: getpass — 비밀번호 입력 ────────────────────────────────────────

print("\nLEVEL 5: 보안 입력 — getpass")
print("-" * 40)

import getpass

# getpass.getpass(): 화면에 입력 안 보임 (실제 실행 시)
# 테스트용 mock
class MockGetpass:
    @staticmethod
    def getpass(prompt="Password: "):
        return "secret123"  # 시뮬레이션

print("getpass.getpass()는 화면에 입력이 표시되지 않습니다")
password = MockGetpass.getpass("데이터베이스 비밀번호: ")
print(f"입력된 비밀번호 길이: {len(password)}자")  # 값은 노출 안 함

# ============================================================================
# [실행 결과]
#   name = 'Alice', type = str
#   age = 25, age + 1 = 26
#   nums = [1, 2, 3, 4, 5], sum = 15
#   ...
#
# [주의사항]
#   1. input()은 항상 str 반환 → 숫자면 int()/float() 변환 필수
#   2. input("프롬프트:")는 stdout에 출력됨 → stdout 캡처 시 영향
#   3. EOFError: 파이프 입력이나 stdin 종료 시 발생
#   4. 프로덕션 코드에서 input() 대신 argparse, os.environ, 설정 파일 사용
#   5. 비밀번호는 getpass.getpass() — input() 사용 금지
#
# [다음 단계]
#   → 010_eval.py: eval() — 강력하지만 위험한 동적 평가
# ============================================================================
