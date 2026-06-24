# ============================================================================
# 001 - print()
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. print()의 모든 파라미터(sep, end, file, flush)를 완전히 이해한다
#   2. print()의 내부 동작 원리를 CPython 수준에서 파악한다
#   3. 실무에서 print()를 언제 쓰고 언제 logging으로 전환하는지 안다
#
# [왜 필요한가]
#   - Python의 가장 기본 출력 메커니즘
#   - 내부적으로 sys.stdout.write() + 버퍼 flush의 조합
#   - 디버깅·CLI 인터페이스·로그의 가장 빠른 수단
#
# [Java 비교]
#   Java  : System.out.println("Hello");      → 줄바꿈 포함
#           System.out.print("A" + "B");       → 직접 연결
#           System.out.printf("%.2f", 3.14);   → 형식 지정
#   Python: print("Hello")                    → end='\n' 기본
#           print("A", "B", sep="")           → sep으로 구분
#           print(f"{3.14:.2f}")              → f-string 형식
#
# [실무 사용 사례]
#   - 빠른 디버그 출력: print(f"[DEBUG] val={x!r}")
#   - 실시간 프로그레스 바: print(".", end="", flush=True)
#   - stderr 분리 출력: print("ERROR", file=sys.stderr)
#   - 출력 캡처 테스트: StringIO 버퍼 활용
# ============================================================================

import sys
import io
import time

# ── LEVEL 1: 기초 사용법 ─────────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 기초 사용법")
print("=" * 50)

print("Hello, Python!")              # 기본: end='\n' 포함
print()                              # 빈 줄 출력
print("one", "two", "three")        # 자동으로 공백 구분 → "one two three"
print(42, 3.14, True, None)         # 모든 타입 str() 변환 후 출력

# ── LEVEL 2: sep / end 파라미터 ──────────────────────────────────────────────

print("\nLEVEL 2: sep / end 파라미터")
print("-" * 40)

# sep: 인수 사이 구분자 (기본값 " ")
print("2024", "06", "15", sep="-")          # 2024-06-15
print("192", "168", "0", "1", sep=".")      # 192.168.0.1
print("A", "B", "C", sep="→")              # A→B→C

# 리스트 언패킹 + sep 조합
headers = ["id", "name", "score"]
print(*headers, sep=",")                    # id,name,score  (CSV 헤더!)

# end: 마지막에 붙는 문자 (기본값 "\n")
print("Step1", end=" → ")
print("Step2", end=" → ")
print("완료")                               # Step1 → Step2 → 완료

# 같은 줄에 순차 출력
for i in range(1, 6):
    print(i, end=" ")
print()  # 줄바꿈

# ── LEVEL 3: file / flush 파라미터 + 내부 동작 ───────────────────────────────

print("\nLEVEL 3: file / flush 파라미터")
print("-" * 40)

# file=sys.stderr: 에러/경고를 별도 스트림으로
print("[WARNING] 설정 파일 없음", file=sys.stderr)
print("[ERROR] DB 연결 실패",   file=sys.stderr)

# file=StringIO: 출력을 문자열로 캡처 (테스트·로그 저장에 활용)
buf = io.StringIO()
print("캡처된 내용", file=buf)
print("두 번째 줄",  file=buf)
captured = buf.getvalue()
print(f"캡처 결과: {captured!r}")           # 'captured\n두 번째 줄\n'

# flush=True: I/O 버퍼를 즉시 비움 → 실시간 출력 보장
print("진행중", end="", flush=True)
for i in range(1, 6):
    time.sleep(0.05)                        # 실제로는 I/O 대기 상황 시뮬레이션
    print(f" {i}", end="", flush=True)
print(" 완료")

# ── LEVEL 3: print() 내부 동작 직접 구현 ────────────────────────────────────

print("\nLEVEL 3: print() 내부 동작 재현")
print("-" * 40)

def my_print(*args, sep=" ", end="\n", file=None, flush=False):
    """
    CPython print() 내부 동작 재현
    소스: cpython/Lib/_pyio.py 참고
    """
    if file is None:
        file = sys.stdout
    # 1) 모든 인자를 str()로 변환
    # 2) sep으로 join
    # 3) end 추가
    # 4) file.write() 호출
    # 5) flush=True면 버퍼 즉시 비우기
    text = sep.join(str(a) for a in args) + end
    file.write(text)
    if flush:
        file.flush()

my_print("Python", "is", "fun", sep=" | ")   # Python | is | fun
my_print(1, 2, 3, sep="-", end="!\n")        # 1-2-3!

# ── LEVEL 4: 실무 패턴 ───────────────────────────────────────────────────────

print("\nLEVEL 4: 실무 패턴")
print("-" * 40)

# 패턴 1: ANSI 컬러 출력 (터미널 지원 시)
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

print(f"{GREEN}[OK]{RESET}    서버 기동 완료")
print(f"{YELLOW}[WARN]{RESET}  메모리 사용량 80%")
print(f"{RED}[ERROR]{RESET} DB 연결 타임아웃")

# 패턴 2: 고정폭 테이블 출력
def print_table(headers, rows, widths):
    sep_line = "-+-".join("-" * w for w in widths)
    fmt = " | ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*headers))
    print(sep_line)
    for row in rows:
        print(fmt.format(*[str(c) for c in row]))

print_table(
    headers=["Name",  "Age", "City"],
    rows   =[["Alice", 30,   "Seoul"],
             ["Bob",   25,   "Busan"],
             ["Carol", 35,   "Incheon"]],
    widths =[10, 5, 10]
)

# 패턴 3: 프로그레스 바
def progress_bar(current, total, width=30):
    ratio    = current / total
    filled   = int(width * ratio)
    bar      = "█" * filled + "░" * (width - filled)
    percent  = ratio * 100
    print(f"\r[{bar}] {percent:5.1f}% ({current}/{total})",
          end="", flush=True)
    if current == total:
        print()  # 완료 시 줄바꿈

for i in range(1, 11):
    time.sleep(0.03)
    progress_bar(i, 10)

# ── LEVEL 5: 오픈소스에서 보이는 패턴 ───────────────────────────────────────

print("\nLEVEL 5: 실무 전환 — logging 모듈")
print("-" * 40)

# Django, FastAPI, PyTorch 등 모든 프레임워크는 print() 대신 logging 사용
import logging

logging.basicConfig(
    level  = logging.DEBUG,
    format = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
    datefmt= "%H:%M:%S"
)
logger = logging.getLogger("myapp")

logger.debug("디버그 정보 — 개발 중에만 활성화")
logger.info("서비스 정상 동작 중")
logger.warning("주의가 필요한 상황")
logger.error("오류 발생 — 기능 중단")

# print() vs logging 차이:
# - logging: 레벨 필터링, 파일 출력, 형식 지정, 스레드 안전
# - print() : 빠른 디버깅에만 사용, 프로덕션 코드에는 logging

# ============================================================================
# [실행 결과 요약]
#   2024-06-15
#   192.168.0.1
#   id,name,score
#   Step1 → Step2 → 완료
#   1 2 3 4 5
#   [WARNING] 설정 파일 없음  (stderr)
#   캡처 결과: '캡처된 내용\n두 번째 줄\n'
#   진행중 1 2 3 4 5 완료
#   [OK]    서버 기동 완료
#   ...
#
# [주의사항]
#   1. 대용량 반복 출력은 sys.stdout.write()가 print()보다 빠름
#      (함수 호출 오버헤드 제거)
#   2. 멀티스레드 환경: print()는 원자적이지 않아 출력이 섞일 수 있음
#      → logging 모듈은 스레드 안전
#   3. print(obj) 는 str(obj) 호출, repr(obj)가 필요하면 print(repr(obj)) 또는 !r
#   4. flush=True 없이 end="" 사용하면 버퍼에 쌓여 즉시 표시 안 될 수 있음
#
# [다음 단계]
#   → 002_variable.py: 변수와 Python 객체 참조 모델
# ============================================================================
