# ============================================================================
# 007 - float (부동소수점)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. IEEE 754 배정밀도의 한계를 이해하고 함정을 피한다
#   2. math.isclose()로 올바른 float 비교를 한다
#   3. decimal 모듈로 정확한 소수 계산을 한다
#   4. 특수 float (inf, nan) 처리를 안다
#
# [왜 필요한가]
#   - "0.1 + 0.2 != 0.3" 같은 부동소수점 함정은 금융/과학 계산에서 치명적
#   - 단순히 == 비교하면 false negative 발생
#   - Java의 BigDecimal과 유사한 decimal 모듈 이해 필요
#
# [Java 비교]
#   Java  : double, float (IEEE 754 동일), BigDecimal (정밀 계산)
#   Python: float (IEEE 754 배정밀도), decimal.Decimal (임의 정밀도)
#           fractions.Fraction (유리수 정확 표현)
# ============================================================================

import math
import sys
import struct
from decimal import Decimal, getcontext
from fractions import Fraction

# ── LEVEL 1: float 기초 ──────────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: float 기초")
print("=" * 50)

x = 3.14
print(f"3.14          = {x}")
print(f"type          = {type(x)}")
print(f"1e3           = {1e3}")       # 1000.0 (지수 표기)
print(f"1.5e-3        = {1.5e-3}")    # 0.0015
print(f"6.022e23      = {6.022e23}")  # 아보가드로 수

# 특수 값
inf  = float("inf")
ninf = float("-inf")
nan  = float("nan")
print(f"\nfloat('inf')  = {inf}")
print(f"float('-inf') = {ninf}")
print(f"float('nan')  = {nan}")
print(f"math.inf      = {math.inf}")

# 특수 값 판별
print(f"\nmath.isinf(inf) = {math.isinf(inf)}")   # True
print(f"math.isnan(nan) = {math.isnan(nan)}")      # True
print(f"nan == nan      = {nan == nan}")            # False! (IEEE 754 규정)
print(f"nan is nan      = {nan is nan}")            # True  (같은 객체)

# 산술 with 특수 값
print(f"\ninf + 1       = {inf + 1}")    # inf
print(f"inf - inf      = {inf - inf}")   # nan
print(f"inf * -1       = {inf * -1}")    # -inf
print(f"1 / 0.0        → ZeroDivisionError")

# ── LEVEL 2: IEEE 754 정밀도 문제 ────────────────────────────────────────────

print("\nLEVEL 2: 부동소수점 정밀도 문제")
print("-" * 40)

print(f"0.1 + 0.2             = {0.1 + 0.2}")          # 0.30000000000000004
print(f"0.1 + 0.2 == 0.3      = {0.1 + 0.2 == 0.3}")  # False!

# 이유: 0.1은 이진수로 정확히 표현 불가
import struct
b = struct.pack("d", 0.1)
print(f"\n0.1의 IEEE 754 표현: {b.hex()}")
print(f"0.1 실제 저장 값: {0.1:.55f}")  # 0.1000000000000000055511151231257827021181583404541015625

# 올바른 float 비교 방법들
a = 0.1 + 0.2
b = 0.3

# 방법 1: 절대 오차 (작은 수에 적합)
print(f"\nabs(a-b) < 1e-9    = {abs(a - b) < 1e-9}")         # True

# 방법 2: math.isclose (권장 — 상대/절대 오차 모두 지원)
print(f"math.isclose(a, b) = {math.isclose(a, b)}")           # True
print(f"isclose 기본 rel_tol=1e-09, abs_tol=0.0")

# 방법 3: round() 후 비교 (간단하지만 부정확할 수 있음)
print(f"round(a,10)==round(b,10) = {round(a,10) == round(b,10)}")

# ── LEVEL 3: decimal 모듈 — 정확한 소수 계산 ─────────────────────────────────

print("\nLEVEL 3: decimal 모듈")
print("-" * 40)

# 금융 계산에서 float 사용 금지 이유
price = 19.99
quantity = 3
wrong = price * quantity
print(f"float: {price} * {quantity} = {wrong}")         # 59.97000000000000..

# decimal 사용 — 정확한 계산
getcontext().prec = 28   # 기본 28자리 정밀도
d_price = Decimal("19.99")   # 반드시 문자열로 초기화!
d_qty   = Decimal("3")
correct = d_price * d_qty
print(f"Decimal: {d_price} * {d_qty} = {correct}")     # 59.97 (정확!)

# 초기화 주의: Decimal(0.1) 은 float의 부정확함 그대로 가져옴
print(f"\nDecimal(0.1)   = {Decimal(0.1)}")     # 정확하지 않음!
print(f"Decimal('0.1') = {Decimal('0.1')}")    # 정확함

# 반올림 모드
from decimal import ROUND_HALF_UP, ROUND_HALF_EVEN
d = Decimal("2.675")
print(f"\n2.675 ROUND_HALF_UP  = {d.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}")
print(f"2.675 ROUND_HALF_EVEN = {d.quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)}")

# 세금 계산 실무 예제
def calc_total(price_str, tax_rate_str):
    price    = Decimal(price_str)
    tax_rate = Decimal(tax_rate_str)
    tax      = (price * tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total    = price + tax
    return price, tax, total

p, t, tot = calc_total("1234.56", "0.1")
print(f"\n가격: {p}, 세금: {t}, 합계: {tot}")

# ── LEVEL 3: float 내부 구조 ────────────────────────────────────────────────

print("\nLEVEL 3: float 내부 구조 (IEEE 754)")
print("-" * 40)

# 64비트 = 부호(1) + 지수(11) + 가수(52)
print(f"sys.float_info.max       = {sys.float_info.max:.3e}")
print(f"sys.float_info.min       = {sys.float_info.min:.3e}")
print(f"sys.float_info.epsilon   = {sys.float_info.epsilon:.3e}")  # 1.0과 다음 float의 차이
print(f"sys.getsizeof(3.14)      = {sys.getsizeof(3.14)} bytes")   # 항상 24bytes (CPython)

# float 비트 표현 분석
def float_bits(f):
    b = struct.pack(">d", f)
    bits = int.from_bytes(b, "big")
    sign = (bits >> 63) & 1
    exp  = (bits >> 52) & 0x7FF
    mant = bits & ((1 << 52) - 1)
    return sign, exp - 1023, mant

for val in [1.0, 0.1, 0.5, -3.14]:
    sign, exp, mant = float_bits(val)
    print(f"  {val:8}: 부호={sign}, 지수={exp:4d}, 가수=0x{mant:013X}")

# ── LEVEL 4: 실무 패턴 ───────────────────────────────────────────────────────

print("\nLEVEL 4: 실무 패턴")
print("-" * 40)

# 패턴 1: 반올림 주의사항
print("round() — Banker's rounding (Python):")
for n in [0.5, 1.5, 2.5, 3.5, 4.5]:
    print(f"  round({n}) = {round(n)}")  # 짝수로 반올림 (0,2,2,4,4)

# 자릿수 지정 반올림
print(f"  round(3.14159, 2) = {round(3.14159, 2)}")   # 3.14
print(f"  round(3.14159, 4) = {round(3.14159, 4)}")   # 3.1416

# 패턴 2: 형식화 출력
pi = math.pi
print(f"\n형식화 출력:")
print(f"  pi = {pi}")
print(f"  pi = {pi:.4f}")       # 소수 4자리
print(f"  pi = {pi:10.4f}")     # 10자리 우측 정렬
print(f"  pi = {pi:e}")         # 과학적 표기법
print(f"  pi = {pi:.4e}")       # 과학적 4자리

big = 1_234_567.89
print(f"  {big:,.2f}")           # 1,234,567.89 (천 단위 콤마)
print(f"  {big:+.2f}")           # +1234567.89  (부호 표시)

# 패턴 3: fractions.Fraction — 유리수 정확 계산
print("\nFraction (유리수 정확 표현):")
print(f"  1/3 + 1/6 = {Fraction(1,3) + Fraction(1,6)}")    # 1/2
print(f"  1/3 * 3   = {Fraction(1,3) * 3}")                # 1
print(f"  float 변환: {float(Fraction(1,3)):.20f}")

# ── LEVEL 5: math 모듈 중요 함수들 ─────────────────────────────────────────

print("\nLEVEL 5: math 모듈 핵심 함수")
print("-" * 40)

print(f"math.floor(3.7)  = {math.floor(3.7)}")    # 3  (내림)
print(f"math.ceil(3.2)   = {math.ceil(3.2)}")     # 4  (올림)
print(f"math.trunc(3.9)  = {math.trunc(3.9)}")    # 3  (0 방향)
print(f"math.trunc(-3.9) = {math.trunc(-3.9)}")   # -3 (0 방향)
print(f"math.floor(-3.2) = {math.floor(-3.2)}")   # -4 (음의 무한대)

print(f"\nmath.sqrt(2)     = {math.sqrt(2):.10f}")
print(f"math.log(math.e) = {math.log(math.e)}")   # 1.0
print(f"math.log10(1000) = {math.log10(1000)}")   # 3.0
print(f"math.sin(math.pi/2) = {math.sin(math.pi/2):.1f}") # 1.0

print(f"\nmath.fsum([0.1]*10) = {math.fsum([0.1]*10)}")    # 1.0 (정확!)
print(f"sum([0.1]*10)       = {sum([0.1]*10)}")             # 0.999...9998 (부정확)

# ============================================================================
# [주의사항]
#   1. 금융 계산: float 절대 금지 → Decimal("문자열") 사용
#   2. float 비교: == 금지 → math.isclose() 사용
#   3. Decimal(0.1) 은 float의 부정확함을 가져옴 → Decimal("0.1") 으로!
#   4. round(2.5) = 2 (Banker's rounding) — 예상과 다를 수 있음
#   5. nan == nan은 False — nan 체크는 math.isnan() 사용
#
# [다음 단계]
#   → 008_str.py: 문자열 — 유니코드, f-string, 불변성
# ============================================================================
