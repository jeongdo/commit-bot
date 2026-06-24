# ============================================================================
# 005 - bool (불리언과 단락 평가)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. bool이 int의 서브클래스임을 이해하고 그 함의를 안다
#   2. Falsy/Truthy 값 전체를 암기한다
#   3. 단락 평가(short-circuit evaluation)를 활용한 Pythonic 패턴을 익힌다
#   4. __bool__, __len__ 오버라이드로 커스텀 truthy 동작을 구현한다
#
# [왜 필요한가]
#   - if/while 조건, 논리 연산, 기본값 설정의 핵심
#   - 단락 평가 이해 없이는 "x or default" 패턴을 제대로 못 씀
#   - bool은 int라는 사실이 sum([True, False, True]) == 2 같은 패턴을 가능케 함
#
# [Java 비교]
#   Java  : boolean은 완전히 별도 타입, int와 무관
#           0이 false가 아님, "" 가 false가 아님
#   Python: bool은 int 서브클래스
#           0, "", [], {}, None 등 다양한 Falsy 값 존재
# ============================================================================

# ── LEVEL 1: bool 기초 ──────────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: bool 기초")
print("=" * 50)

print(f"True  = {True},  type = {type(True)}")
print(f"False = {False}, type = {type(False)}")

# bool은 int 서브클래스!
print(f"\nbool의 부모: {bool.__bases__}")           # (<class 'int'>,)
print(f"isinstance(True, int) = {isinstance(True, int)}")  # True

# bool 산술 연산 (Java에서는 불가능)
print(f"\nTrue  + True   = {True + True}")     # 2
print(f"True  + False  = {True + False}")    # 1
print(f"True  * 5      = {True * 5}")        # 5
print(f"False * 100    = {False * 100}")     # 0
print(f"True  == 1     = {True == 1}")       # True
print(f"False == 0     = {False == 0}")      # True

# 실용: 조건 충족 개수 세기
results = [True, False, True, True, False]
print(f"\n충족 개수: sum({results}) = {sum(results)}")  # 3
# Java: results.stream().filter(x->x).count()

# ── LEVEL 2: Falsy / Truthy 규칙 ────────────────────────────────────────────

print("\nLEVEL 2: Falsy / Truthy 전체 목록")
print("-" * 40)

falsy = [
    (False,   "bool"),
    (0,       "int 0"),
    (0.0,     "float 0.0"),
    (0j,      "complex 0j"),
    ("",      "빈 str"),
    ([],      "빈 list"),
    ((),      "빈 tuple"),
    ({},      "빈 dict"),
    (set(),   "빈 set"),
    (None,    "None"),
]

print("  Falsy 값:")
for val, desc in falsy:
    print(f"    bool({val!r:<12}) = {bool(val)}  # {desc}")

# 주의: "0"은 문자열이므로 Truthy!
print(f"\n  bool('0')  = {bool('0')}   # 문자열 '0'은 Truthy!")
print(f"  bool('  ') = {bool('  ')}   # 공백 문자열도 Truthy!")
print(f"  bool([0])  = {bool([0])}   # 원소가 0인 리스트도 Truthy!")

# ── LEVEL 2: 논리 연산자 ────────────────────────────────────────────────────

print("\nLEVEL 2: 논리 연산자 (and / or / not)")
print("-" * 40)

print(f"True  and True  = {True and True}")    # True
print(f"True  and False = {True and False}")   # False
print(f"False or  True  = {False or True}")    # True
print(f"False or  False = {False or False}")   # False
print(f"not True        = {not True}")         # False
print(f"not not 'hello' = {not not 'hello'}")  # True (이중 부정 = bool 변환)

# ── LEVEL 3: 단락 평가 (Short-circuit Evaluation) ───────────────────────────

print("\nLEVEL 3: 단락 평가")
print("-" * 40)

# and: 첫 Falsy 반환 (없으면 마지막 값)
print(f"0   and 'hello' = {0 and 'hello'!r}")      # 0     (0이 Falsy → 즉시 반환)
print(f"1   and 'hello' = {1 and 'hello'!r}")      # 'hello' (1이 Truthy → 계속)
print(f"1   and 2       = {1 and 2}")              # 2     (둘 다 Truthy → 마지막)
print(f"1   and 0       = {1 and 0}")              # 0     (0이 Falsy)

# or: 첫 Truthy 반환 (없으면 마지막 값)
print(f"''  or 'default' = {''.or_('default')!r}" if False else
      f"''  or 'default' = {'' or 'default'!r}")   # 'default' ('' Falsy → 계속)
print(f"'hi' or 'default'= {'hi' or 'default'!r}") # 'hi' (Truthy → 즉시 반환)
print(f"0   or 0         = {0 or 0}")              # 0    (둘 다 Falsy → 마지막)
print(f"None or 0 or []  = {None or 0 or []!r}")   # [] (모두 Falsy → 마지막)

# 단락 평가 → 함수 호출 생략
def side_effect(msg):
    print(f"  [side_effect 호출됨: {msg}]")
    return True

print("\nand 단락: False → 오른쪽 미평가")
result = False and side_effect("and")   # side_effect 호출 안 됨!
print(f"결과: {result}")

print("\nor  단락: True → 오른쪽 미평가")
result = True or side_effect("or")     # side_effect 호출 안 됨!
print(f"결과: {result}")

# ── LEVEL 4: 실무 패턴 ───────────────────────────────────────────────────────

print("\nLEVEL 4: 실무 패턴")
print("-" * 40)

# 패턴 1: 기본값 설정 (or 패턴) — None 또는 Falsy 모두 처리
def get_config(val=None):
    return val or "기본값"

print(f"get_config()       = {get_config()!r}")       # '기본값'
print(f"get_config(None)   = {get_config(None)!r}")   # '기본값'
print(f"get_config('설정') = {get_config('설정')!r}") # '설정'
print(f"get_config('')     = {get_config('')!r}")      # '기본값' ← 주의! 빈 문자열도 처리

# 패턴 2: None만 구분 (is None 명시)
def get_value(val=None):
    return "기본값" if val is None else val

print(f"get_value()        = {get_value()!r}")     # '기본값'
print(f"get_value('')      = {get_value('')!r}")   # '' (빈 문자열 허용)
print(f"get_value(0)       = {get_value(0)!r}")    # 0  (0 허용)

# 패턴 3: and로 안전한 체이닝 (None guard)
user = {"profile": {"name": "Alice"}}
no_user = None

name1 = user and user.get("profile") and user["profile"].get("name")
name2 = no_user and no_user.get("profile")   # no_user가 None → 즉시 None 반환
print(f"user name: {name1!r}")    # 'Alice'
print(f"no_user  : {name2!r}")    # None (AttributeError 없이 안전)

# 패턴 4: all() / any()
scores = [85, 92, 78, 95, 88]
print(f"\nall >= 70: {all(s >= 70 for s in scores)}")   # True
print(f"any >= 90: {any(s >= 90 for s in scores)}")     # True
print(f"any >= 99: {any(s >= 99 for s in scores)}")     # False

# 권한 체크 패턴
required = {"read", "write"}
user_perms = {"read", "write", "execute"}
print(f"권한 충족: {all(p in user_perms for p in required)}")  # True

# ── LEVEL 4: __bool__ / __len__ 커스터마이즈 ─────────────────────────────────

print("\nLEVEL 4: __bool__ / __len__ 커스터마이즈")
print("-" * 40)

class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)
        return self  # 메서드 체이닝

    def pop(self):
        return self._items.pop()

    def __len__(self):
        return len(self._items)

    # __bool__ 없으면 bool(obj) → bool(len(obj)) 사용
    # 직접 정의하면 __len__보다 우선
    def __bool__(self):
        return len(self._items) > 0

    def __repr__(self):
        return f"Stack({self._items})"

s = Stack()
print(f"빈 스택 bool: {bool(s)}")    # False
s.push(1).push(2)
print(f"스택 후 bool: {bool(s)}")   # True
print(f"if 스택:")
if s:
    print("  스택에 데이터 있음")

# __bool__ 없고 __len__ 있는 경우
class MyList:
    def __init__(self, items):
        self._items = items
    def __len__(self):
        return len(self._items)

ml_empty = MyList([])
ml_full  = MyList([1, 2])
print(f"\nbool(빈 MyList)   = {bool(ml_empty)}")   # False (__len__ 이용)
print(f"bool(채운 MyList) = {bool(ml_full)}")      # True

# ── LEVEL 5: 오픈소스에서 보이는 패턴 ───────────────────────────────────────

print("\nLEVEL 5: 오픈소스 패턴")
print("-" * 40)

# NumPy, Pandas에서 경고가 뜨는 이유: 배열의 bool()이 모호
# if np_array:  → ValueError: ambiguous truth value
# 해결: if len(np_array) > 0: 또는 if np_array.size > 0:

# Django ORM에서 자주 보이는 패턴
class QuerySet:
    def __init__(self, results):
        self._results = results

    def __bool__(self):
        return bool(self._results)

    def __len__(self):
        return len(self._results)

    def exists(self):  # 권장 방법 (DB 쿼리 최소화)
        return bool(self._results)

qs_empty = QuerySet([])
qs_full  = QuerySet([{"id": 1, "name": "Alice"}])

# Django: if queryset.exists(): 가 if queryset: 보다 권장
print(f"빈 QuerySet bool: {bool(qs_empty)}")  # False
print(f"채운 QuerySet bool: {bool(qs_full)}") # True

# ============================================================================
# [주의사항]
#   1. 0 or "default" 는 0도 처리 → 0을 허용해야 하면 is None 체크 사용
#   2. True/False 대소문자 구분 필수 (true → NameError)
#   3. numpy 배열의 if arr: → ValueError, .any() / .all() 사용
#   4. bool(obj) → __bool__ 우선, 없으면 __len__, 없으면 True
#
# [다음 단계]
#   → 006_int.py: 정수 — 무제한 정밀도, 비트 연산, 진수 변환
# ============================================================================
