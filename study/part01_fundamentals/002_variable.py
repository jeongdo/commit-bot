# ============================================================================
# 002 - variable (변수와 객체 참조 모델)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. Python 변수가 '이름표(label)'임을 이해한다 — Java의 '상자(box)'와 다름
#   2. id(), is, == 의 차이를 완전히 구분한다
#   3. 소형 정수 캐싱, 문자열 intern 같은 CPython 최적화를 안다
#   4. 다중 할당, 증강 할당, 변수 교환을 Pythonic 하게 쓴다
#
# [왜 필요한가]
#   - '변수 = 이름표' 개념이 틀리면 mutable/copy 관련 버그가 계속 발생
#   - is vs == 혼동은 None 체크 오류의 주원인
#   - 소형 정수 캐싱을 모르면 is 연산 결과가 예측 불가
#
# [Java 비교]
#   Java  : int x = 10;        → x 상자에 값 10 저장 (stack)
#           String s = "hi";   → s 상자에 참조 저장, 힙에 객체
#   Python: x = 10             → 정수 객체 10을 x라는 이름으로 참조
#           s = "hi"           → 문자열 객체를 s라는 이름으로 참조
#           → 모든 변수는 참조(reference)만 저장. primitive 없음
#
# [실무 사용 사례]
#   - 다중 반환값 언패킹: a, b = func()
#   - 스왑: a, b = b, a  (임시 변수 불필요)
#   - 타입 힌트 명시: count: int = 0
# ============================================================================

import sys
import copy

# ── LEVEL 1: 기본 할당 ───────────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 기본 할당과 타입")
print("=" * 50)

x      = 10          # int 객체를 'x'라는 이름표로 참조
name   = "Alice"     # str 객체 참조
pi     = 3.14159     # float 객체 참조
active = True        # bool 객체 참조
data   = None        # None 싱글톤 참조

print(f"x={x}, name={name}, pi={pi}, active={active}, data={data}")
print(f"타입: {type(x)}, {type(name)}, {type(pi)}, {type(active)}, {type(data)}")

# PEP 8 변수명 규칙
user_name   = "Bob"          # ✓ snake_case (Python 표준)
MAX_RETRIES = 3              # ✓ UPPER_SNAKE (상수 관례)
_internal   = "내부용"       # ✓ 언더스코어 접두사 (모듈 내부)
# userName  = "Bad"         # ✗ camelCase는 Python 비권장

# ── LEVEL 2: 동적 타이핑 — 같은 이름표가 다른 타입을 가리킬 수 있음 ──────────

print("\nLEVEL 2: 동적 타이핑")
print("-" * 40)

val = 42
print(f"val = {val}, type = {type(val).__name__}")  # int

val = "hello"
print(f"val = {val}, type = {type(val).__name__}")  # str — 이름표가 새 객체 가리킴

val = [1, 2, 3]
print(f"val = {val}, type = {type(val).__name__}")  # list

# 다중 할당
a, b, c = 10, 20, 30
print(f"a={a}, b={b}, c={c}")

# 연쇄 할당 — 같은 객체를 세 이름이 가리킴
x = y = z = 0
print(f"x={x}, y={y}, z={z}, 같은 객체? {x is y is z}")  # True

# 스왑 (Java는 temp 변수 필요!)
a, b = 100, 200
a, b = b, a      # 오른쪽 (b, a) 를 튜플로 묶어 왼쪽에 언패킹
print(f"스왑 후: a={a}, b={b}")  # a=200, b=100

# ── LEVEL 3: 변수는 이름표 — id()와 메모리 참조 모델 ─────────────────────────

print("\nLEVEL 3: id()와 객체 참조 모델")
print("-" * 40)

# id() = CPython에서 객체의 메모리 주소
a = [1, 2, 3]
b = a              # 같은 리스트 객체를 두 이름으로 참조
print(f"id(a)={id(a)}, id(b)={id(b)}")
print(f"a is b: {a is b}")     # True: 동일 객체!

b.append(4)        # b를 통해 수정 → a도 바뀜 (같은 객체이므로)
print(f"b.append(4) 후 a={a}")  # [1, 2, 3, 4]

# 새 객체를 만들려면 명시적 복사 필요
c = a.copy()       # 얕은 복사 → 새 리스트 객체
c.append(5)
print(f"c.append(5) 후 a={a}")  # [1, 2, 3, 4] — 영향 없음
print(f"id(a)={id(a)}, id(c)={id(c)}, 다른 객체? {a is not c}")

# is vs == 차이
lst1 = [1, 2, 3]
lst2 = [1, 2, 3]
print(f"\nlst1 == lst2: {lst1 == lst2}")   # True  — 값이 같음
print(f"lst1 is lst2: {lst1 is lst2}")     # False — 다른 객체
print(f"id(lst1)={id(lst1)}, id(lst2)={id(lst2)}")

# None은 싱글톤 → 반드시 is 로 비교
result = None
print(f"\nresult is None: {result is None}")   # ✓ 올바른 방법
print(f"result == None: {result == None}")     # 작동하지만 비권장

# ── LEVEL 3: CPython 최적화 — 소형 정수 캐싱 ─────────────────────────────────

print("\nLEVEL 3: 소형 정수 캐싱 (-5 ~ 256)")
print("-" * 40)

# CPython은 -5 ~ 256 범위의 정수를 시작 시 미리 생성하고 캐싱
x = 256;  y = 256
print(f"256: x is y = {x is y}")   # True  (캐싱 범위 안)

x = 257;  y = 257
print(f"257: x is y = {x is y}")   # False (캐싱 범위 밖, 별도 객체)

x = -5;   y = -5
print(f"-5 : x is y = {x is y}")   # True  (캐싱 최솟값)

x = -6;   y = -6
print(f"-6 : x is y = {x is y}")   # False (캐싱 범위 밖)

# 문자열 intern — 식별자로 쓸 수 있는 문자열은 자동 intern
s1 = "hello"
s2 = "hello"
print(f"\n'hello': s1 is s2 = {s1 is s2}")   # True (intern됨)

s1 = "hello world"
s2 = "hello world"
print(f"'hello world': s1 is s2 = {s1 is s2}")  # 보장 안 됨

import sys
s1 = sys.intern("some arbitrary string!")
s2 = sys.intern("some arbitrary string!")
print(f"sys.intern 사용: s1 is s2 = {s1 is s2}")  # True (강제 intern)

# ── LEVEL 3: 메모리 크기 ─────────────────────────────────────────────────────

print("\nLEVEL 3: 객체별 메모리 크기")
print("-" * 40)

for obj in [None, True, 0, 1, 256, 257, 3.14, "a", "hello", [], [1,2,3], {}]:
    print(f"  {repr(obj):<20} → {sys.getsizeof(obj):4d} bytes")

# ── LEVEL 4: 실무 패턴 ───────────────────────────────────────────────────────

print("\nLEVEL 4: 실무 패턴")
print("-" * 40)

# 패턴 1: 증강 할당
n = 10
n += 5    # n = n + 5  → 15
n -= 3    # n = n - 3  → 12
n *= 2    # n = n * 2  → 24
n //= 5   # n = n // 5 → 4  (정수 나눗셈)
n **= 3   # n = n ** 3 → 64
print(f"증강 할당 결과: n={n}")

# 패턴 2: _ 로 불필요한 값 무시
first, _, third = (1, 2, 3)
print(f"first={first}, third={third}")

# 여러 값 무시
_, important, _ = ("버림", "핵심값", "버림")
print(f"important={important}")

# 패턴 3: 타입 힌트 어노테이션 (Python 3.6+)
count: int = 0
names: list[str] = []      # 런타임에 영향 없음 — IDE/mypy 지원 목적
mapping: dict[str, int] = {}

# 패턴 4: 조건부 할당
raw = ""
# 빈 문자열은 Falsy → 기본값 사용
value = raw or "기본값"
print(f"value={value}")   # 기본값

# None 체크와 빈 문자열 구분이 필요하면 is None 사용
value2 = raw if raw is not None else "기본값"
print(f"value2={value2}")  # ""  (빈 문자열 허용)

# 패턴 5: walrus operator (Python 3.8+)
import re
text = "이메일: alice@example.com"
if m := re.search(r"[\w.]+@[\w.]+", text):   # 조건과 할당 동시
    print(f"이메일 발견: {m.group()}")

# ── LEVEL 5: 오픈소스에서 보이는 패턴 ───────────────────────────────────────

print("\nLEVEL 5: 오픈소스 패턴")
print("-" * 40)

# NumPy, Pandas 등에서 자주 보이는 형태:
# x = x if x is not None else default_value
# result = value or fallback

# Django 소스에서 자주 보이는 패턴
class Config:
    DEBUG    = False
    DB_HOST  = "localhost"
    DB_PORT  = 5432

    @classmethod
    def from_env(cls):
        import os
        cfg = cls()
        cfg.DEBUG   = os.environ.get("DEBUG", "false").lower() == "true"
        cfg.DB_HOST = os.environ.get("DB_HOST", cls.DB_HOST)
        cfg.DB_PORT = int(os.environ.get("DB_PORT", cls.DB_PORT))
        return cfg

cfg = Config.from_env()
print(f"Config: debug={cfg.DEBUG}, host={cfg.DB_HOST}:{cfg.DB_PORT}")

# ============================================================================
# [실행 결과]
#   val = 42,    type = int
#   val = hello, type = str
#   val = [1,2,3], type = list
#   a=10, b=20, c=30
#   스왑 후: a=200, b=100
#   a is b: True
#   b.append(4) 후 a=[1, 2, 3, 4]
#   256: x is y = True
#   257: x is y = False
#   ...
#
# [주의사항]
#   1. x is y 는 동일 객체 비교 — 값 비교는 반드시 ==
#   2. None, True, False 비교는 항상 is / is not 사용
#   3. 소형 정수 캐싱에 의존하는 코드 작성 금지 (구현체마다 다름)
#   4. x = y = [] 는 같은 리스트 공유 → 수정 시 모두 영향받음
#   5. 상수처럼 쓸 값도 Python은 런타임에 변경 가능 — 관례로만 보호
#
# [다음 단계]
#   → 003_data_type.py: Python 내장 타입 전체 조감
# ============================================================================
