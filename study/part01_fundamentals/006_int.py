# ============================================================================
# 006 - int (정수)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. Python int의 무제한 정밀도를 이해한다 (오버플로우 없음)
#   2. 진수 리터럴(0x, 0o, 0b)과 변환 함수를 익힌다
#   3. 비트 연산으로 플래그/마스킹 패턴을 구현한다
#   4. Java와의 나눗셈 차이(floor vs truncate)를 정확히 안다
#
# [왜 필요한가]
#   - Java처럼 int/long 구분 불필요 → 큰 수 계산 자유롭게 가능
#   - 비트 연산: 권한 플래그, 해시, 압축 알고리즘
#   - // 연산자: Java와 음수 처리 다름 → 버그 유발 주의
#
# [Java 비교]
#   Java  : int(32bit, ±2^31), long(64bit, ±2^63) → 오버플로우 발생
#           int a = 2000000000 + 2000000000; → 오버플로우
#   Python: 2_000_000_000 + 2_000_000_000 = 4_000_000_000 (정확!)
#           2**100 도 정확히 계산
# ============================================================================

import sys
import math

# ── LEVEL 1: 기본 정수 연산 ─────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 기본 정수 연산")
print("=" * 50)

a, b = 17, 5

print(f"a={a}, b={b}")
print(f"  a + b  = {a + b}")     # 22   덧셈
print(f"  a - b  = {a - b}")     # 12   뺄셈
print(f"  a * b  = {a * b}")     # 85   곱셈
print(f"  a / b  = {a / b}")     # 3.4  나눗셈 (항상 float!)
print(f"  a // b = {a // b}")    # 3    정수 나눗셈 (몫, floor)
print(f"  a % b  = {a % b}")     # 2    나머지
print(f"  a ** b = {a ** b}")    # 1419857  거듭제곱
print(f"  -a     = {-a}")        # -17  단항 음수
print(f"  abs(a) = {abs(a)}")    # 17   절댓값

# ── LEVEL 1: 무제한 정밀도 ──────────────────────────────────────────────────

print("\nLEVEL 1: 무제한 정밀도 — Java에 없는 기능")
print("-" * 40)

big = 2 ** 100
print(f"2**100 = {big}")
print(f"자릿수: {len(str(big))}자리")

fib_big = 2 ** 1000
print(f"2**1000: {len(str(fib_big))}자리 수")

# 팩토리얼 (Java long으로는 21! 이상 오버플로우)
print(f"100!   : {len(str(math.factorial(100)))}자리 수")
print(f"1000!  : {len(str(math.factorial(1000)))}자리 수")

# 천 단위 언더스코어 (Python 3.6+, 가독성)
big_num = 1_000_000_000
pi_approx = 3_141_592_653_589
print(f"\n1_000_000_000 = {big_num:,}")
print(f"3_141_592_653_589 = {pi_approx:,}")

# ── LEVEL 2: 진수 리터럴과 변환 ─────────────────────────────────────────────

print("\nLEVEL 2: 진수 리터럴과 변환")
print("-" * 40)

# 리터럴
dec = 255
hex_ = 0xFF          # 16진수 접두사 0x
oct_ = 0o377         # 8진수  접두사 0o
bin_ = 0b11111111    # 2진수  접두사 0b

print(f"10진: {dec}, 16진: {hex_}, 8진: {oct_}, 2진: {bin_}")
print(f"모두 같음? {dec == hex_ == oct_ == bin_}")   # True

# 정수 → 진수 문자열 변환
n = 255
print(f"\nhex(255)  = {hex(n)}")         # 0xff
print(f"oct(255)  = {oct(n)}")           # 0o377
print(f"bin(255)  = {bin(n)}")           # 0b11111111
print(f"format(255, 'X') = {n:X}")       # FF (대문자, 접두사 없음)
print(f"format(255, '#010x') = {n:#010x}") # 0x000000ff (8자리 패딩)

# 문자열 → 정수 변환
print(f"\nint('FF', 16)        = {int('FF', 16)}")          # 255
print(f"int('377', 8)         = {int('377', 8)}")           # 255
print(f"int('11111111', 2)    = {int('11111111', 2)}")      # 255
print(f"int('0xff', 16)       = {int('0xff', 16)}")         # 255 (0x 접두사 포함)

# ── LEVEL 2: 나눗셈 주의사항 — Java와 차이 ──────────────────────────────────

print("\nLEVEL 2: 나눗셈 — Java와 핵심 차이")
print("-" * 40)

# Python //: 수학적 floor division (음의 무한대 방향)
# Java   /: truncate division (0 방향)
print("양수 나눗셈:")
print(f"  7 // 2 = {7 // 2}")     # 3  (Python == Java)
print(f"  7 / 2  = {7 / 2}")      # 3.5 (Python float, Java=3 int)

print("\n음수 나눗셈 (Python vs Java 차이!):")
print(f"  -7 // 2 = {-7 // 2}")   # -4 Python (floor toward -∞)
print(f"  -7 / 2  = {-7 / 2}")    # -3.5
# Java: -7 / 2 = -3 (truncate toward 0)
print(f"  7 // -2 = {7 // -2}")   # -4 Python
print(f"  -7 % 2  = {-7 % 2}")    # 1  Python (항상 divisor와 같은 부호)
# Java: -7 % 2 = -1

# divmod: 몫과 나머지 동시
q, r = divmod(17, 5)
print(f"\ndivmod(17, 5)  = ({q}, {r})")    # (3, 2)
q, r = divmod(-17, 5)
print(f"divmod(-17, 5) = ({q}, {r})")       # (-4, 3)

# ── LEVEL 3: 비트 연산 ──────────────────────────────────────────────────────

print("\nLEVEL 3: 비트 연산")
print("-" * 40)

a = 0b1010  # 10
b = 0b1100  # 12

ops = [
    ("AND  (&)", a & b, "공통 비트만"),
    ("OR   (|)", a | b, "어느 한쪽이라도"),
    ("XOR  (^)", a ^ b, "다른 비트만"),
    ("NOT  (~)", ~a,    "모든 비트 반전 (2의 보수)"),
    ("L-시프트(<<2)", a << 2, "×4 효과"),
    ("R-시프트(>>1)", a >> 1, "÷2 효과"),
]
for name, result, desc in ops:
    print(f"  {name:<18} = {result:4d} ({bin(result):<12}) # {desc}")

# ── LEVEL 4: 실무 패턴 — 비트 플래그 ────────────────────────────────────────

print("\nLEVEL 4: 실무 패턴 — 비트 플래그")
print("-" * 40)

# 권한 시스템 (Unix 파일 권한 방식)
READ    = 0b001   # 1
WRITE   = 0b010   # 2
EXECUTE = 0b100   # 4

# 권한 부여
admin_perm = READ | WRITE | EXECUTE   # 7 = 0b111
user_perm  = READ | WRITE             # 3 = 0b011
guest_perm = READ                     # 1 = 0b001

def check_perm(perm, flag, name):
    has = bool(perm & flag)
    print(f"  {name:<7}: {'O' if has else 'X'}")

print("admin 권한:")
for flag, name in [(READ,"읽기"), (WRITE,"쓰기"), (EXECUTE,"실행")]:
    check_perm(admin_perm, flag, name)

print("guest 권한:")
for flag, name in [(READ,"읽기"), (WRITE,"쓰기"), (EXECUTE,"실행")]:
    check_perm(guest_perm, flag, name)

# 권한 추가/제거
user_perm_new = user_perm | EXECUTE    # 실행 권한 추가
user_perm_del = user_perm & ~WRITE     # 쓰기 권한 제거
print(f"\n실행 추가: {user_perm:03b} → {user_perm_new:03b}")
print(f"쓰기 제거: {user_perm:03b} → {user_perm_del:03b}")

# 짝홀 판별 (비트 연산이 %보다 빠름)
print("\n짝홀 판별 (비트 연산):")
for n in [-3, 0, 4, 7, 100]:
    even = (n & 1) == 0
    print(f"  {n:4d}: {'짝수' if even else '홀수'}")

# 2의 거듭제곱 확인
def is_power_of_2(n):
    return n > 0 and (n & (n - 1)) == 0

print("\n2의 거듭제곱:")
for n in [1, 2, 3, 4, 8, 16, 15, 32]:
    print(f"  {n:3d}: {is_power_of_2(n)}")

# ── LEVEL 4: 모듈러 지수승 (암호학 활용) ────────────────────────────────────

print("\nLEVEL 4: pow(base, exp, mod) — 모듈러 지수승")
print("-" * 40)

# 일반 방식: (base ** exp) % mod → 중간 계산값이 천문학적으로 커질 수 있음
# 최적 방식: pow(base, exp, mod)  → 내부적으로 모듈러 감소하며 계산
import time

base, exp, mod = 12345, 67890, 99991

t1 = time.perf_counter()
r1 = (base ** exp) % mod
t1 = time.perf_counter() - t1

t2 = time.perf_counter()
r2 = pow(base, exp, mod)     # C 레벨 최적화
t2 = time.perf_counter() - t2

print(f"결과 동일: {r1 == r2}")
print(f"일반 방식: {t1*1000:.2f}ms")
print(f"pow 방식 : {t2*1000:.4f}ms  ← 훨씬 빠름")

# ── LEVEL 5: int 메모리 크기 (CPython 내부) ──────────────────────────────────

print("\nLEVEL 5: CPython int 메모리 구조")
print("-" * 40)

# CPython의 int는 가변 길이 배열로 구현 (longobject)
# 각 "digit"이 30비트 단위로 저장됨
for n in [0, 1, 2**30-1, 2**30, 2**60, 2**90, 2**300]:
    size = sys.getsizeof(n)
    print(f"  2^{n.bit_length()-1 if n > 0 else 0:<3} ({len(str(n))}자리): {size} bytes")

print(f"\n작은 정수 캐싱 범위: -5 ~ 256")
print(f"  id(255)  고정: {id(255)}")
print(f"  id(256)  고정: {id(256)}")

# ============================================================================
# [주의사항]
#   1. a / b 는 항상 float 반환 — 정수 원하면 반드시 //
#   2. -7 // 2 = -4 (Python), Java는 -3 — 음수 처리 반드시 확인
#   3. 무제한 정밀도라도 매우 큰 수의 연산은 느림 → 과학 계산엔 numpy
#   4. 비트 연산 ~ (NOT): ~n = -(n+1) (2의 보수 표현)
#
# [다음 단계]
#   → 007_float.py: 부동소수점 — IEEE 754 함정과 decimal 모듈
# ============================================================================
