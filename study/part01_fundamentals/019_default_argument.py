# ============================================================================
# 019 - default_argument (기본값 인수)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. mutable 기본값의 함정을 완전히 이해하고 절대 반복하지 않는다
#   2. None을 기본값으로 사용하는 패턴을 체화한다
#   3. sentinel 객체 패턴으로 None과 "인수 미전달"을 구분한다
#   4. 기본값이 함수 정의 시 단 한 번 평가됨을 안다
#
# [왜 필요한가]
#   - Python에서 가장 유명한 함정 1위: mutable default argument
#   - 모든 Python 면접에 나오는 질문
#   - 이를 모르면 list/dict를 기본값으로 쓸 때마다 버그 발생
#
# [Java 비교]
#   Java  : 메서드 오버로딩으로 기본값 표현
#           void func() { func(new ArrayList()); }  // 매번 새 객체
#   Python: def func(lst=None): if lst is None: lst = []
# ============================================================================

import time

# ── LEVEL 1: 기본값 파라미터 기초 ───────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 기본값 파라미터 기초")
print("=" * 50)

def greet(name: str, greeting: str = "Hello", punctuation: str = "!") -> str:
    return f"{greeting}, {name}{punctuation}"

print(greet("Alice"))                          # Hello, Alice!
print(greet("Bob", "Hi"))                      # Hi, Bob!
print(greet("Carol", punctuation="?"))         # Hello, Carol?
print(greet("Dave", "Hey", "."))               # Hey, Dave.

# 기본값 있는 파라미터는 없는 파라미터 뒤에
def create_user(name: str, age: int, role: str = "user", active: bool = True):
    return {"name": name, "age": age, "role": role, "active": active}

u1 = create_user("Alice", 30)
u2 = create_user("Bob", 25, "admin")
u3 = create_user("Carol", 28, active=False)
for u in [u1, u2, u3]:
    print(f"  {u}")

# ── LEVEL 2: mutable 기본값의 함정 ──────────────────────────────────────────

print("\nLEVEL 2: mutable 기본값 함정")
print("-" * 40)

# BAD: 리스트를 기본값으로 사용
def add_item_BAD(item, lst=[]):
    lst.append(item)
    return lst

# 기본값 리스트는 함수 객체에 묶여 모든 호출이 공유!
r1 = add_item_BAD("a")
r2 = add_item_BAD("b")
r3 = add_item_BAD("c")
print("BAD 결과 (의도: ['a'], ['b'], ['c']):")
print(f"  r1={r1}, r2={r2}, r3={r3}")   # 모두 ['a','b','c'] !!!
print(f"  r1 is r2: {r1 is r2}")        # True — 같은 리스트 공유!
print(f"  add_item_BAD.__defaults__: {add_item_BAD.__defaults__}")  # 공유 리스트 확인

# GOOD: None을 기본값으로 사용
def add_item(item, lst=None):
    if lst is None:
        lst = []     # 매 호출마다 새 리스트 생성!
    lst.append(item)
    return lst

r1 = add_item("a")
r2 = add_item("b")
r3 = add_item("c")
print("\nGOOD 결과 (의도: ['a'], ['b'], ['c']):")
print(f"  r1={r1}, r2={r2}, r3={r3}")   # ['a'], ['b'], ['c'] 각각 독립

# dict도 동일
def add_entry_BAD(key, val, data={}):
    data[key] = val
    return data

add_entry_BAD("a", 1)
add_entry_BAD("b", 2)
print(f"\nBAD dict: {add_entry_BAD('c', 3)}")  # {"a":1,"b":2,"c":3} 누적!

# ── LEVEL 2: 기본값은 함수 정의 시 단 한 번 평가 ─────────────────────────────

print("\nLEVEL 2: 기본값 평가 시점")
print("-" * 40)

# BAD: 현재 시각을 기본값으로 (정의 시점에 고정됨)
DEFINED_AT = time.time()

def log_event_BAD(msg, ts=DEFINED_AT):
    print(f"  [{ts:.0f}] {msg}")

time.sleep(0.01)
log_event_BAD("이벤트 1")   # 정의 시점 ts — 호출 시점 아님!
time.sleep(0.01)
log_event_BAD("이벤트 2")   # 같은 ts!

# GOOD: None → 함수 내에서 현재 시각 획득
def log_event(msg, ts=None):
    if ts is None:
        ts = time.time()   # 매 호출마다 현재 시각
    print(f"  [{ts:.0f}] {msg}")

log_event("이벤트 1")
time.sleep(0.01)
log_event("이벤트 2")   # 다른 ts

# ── LEVEL 3: Sentinel 패턴 — None과 "미전달"을 구분 ─────────────────────────

print("\nLEVEL 3: Sentinel 패턴")
print("-" * 40)

# None이 유효한 값일 때 (None을 실제로 전달할 수 있는 경우)
_MISSING = object()   # 고유한 sentinel 객체 (모듈 레벨)

def get_user_field(user: dict, field: str, default=_MISSING):
    """
    user 딕셔너리에서 field를 반환.
    필드가 없으면 default 반환.
    default 미지정 + 필드 없으면 KeyError.
    """
    value = user.get(field, _MISSING)
    if value is _MISSING:
        if default is _MISSING:
            raise KeyError(f"필드 '{field}' 없음")
        return default
    return value

user = {"id": 1, "name": "Alice", "bio": None}  # bio가 None인 경우

print(f"id 조회     : {get_user_field(user, 'id')}")          # 1
print(f"name 조회   : {get_user_field(user, 'name')}")        # Alice
print(f"bio 조회    : {get_user_field(user, 'bio')!r}")       # None (실제 값!)
print(f"age 기본값  : {get_user_field(user, 'age', 0)}")      # 0
print(f"bio or None : {get_user_field(user, 'bio') or '기본'}")  # '기본' (함정!)

try:
    get_user_field(user, "email")
except KeyError as e:
    print(f"email 없음  : KeyError {e}")

# ── LEVEL 4: 실무 패턴 ───────────────────────────────────────────────────────

print("\nLEVEL 4: 실무 패턴")
print("-" * 40)

# 패턴 1: or 단축 기본값 (Falsy 전체 처리)
def connect(host=None, port=None):
    host = host or "localhost"    # None, "", 0 모두 처리
    port = port or 5432
    return f"연결: {host}:{port}"

print(connect())
print(connect("db.server.com", 3306))
print(connect("", 0))   # 빈 문자열, 0도 기본값으로 처리됨 (의도했다면 OK)

# 패턴 2: 딕셔너리 기본값
def build_config(overrides=None):
    defaults = {
        "debug": False,
        "log_level": "INFO",
        "max_connections": 10,
        "timeout": 30,
    }
    if overrides:
        defaults.update(overrides)  # 덮어쓰기
    return defaults

cfg1 = build_config()
cfg2 = build_config({"debug": True, "timeout": 60})
print(f"\n기본 설정: {cfg1}")
print(f"오버라이드: {cfg2}")

# 패턴 3: 타입 힌트 + 기본값 조합
from typing import Optional, List

def process_items(
    items: List[int],
    multiplier: float = 1.0,
    filter_fn: Optional[callable] = None,
    transform_fn: Optional[callable] = None,
) -> List[float]:
    result = items
    if filter_fn:
        result = [x for x in result if filter_fn(x)]
    if transform_fn:
        result = [transform_fn(x) for x in result]
    return [x * multiplier for x in result]

nums = [-2, 0, 3, 5, -1, 7]
print(f"\n원본: {nums}")
print(f"양수만x2: {process_items(nums, 2.0, lambda x: x > 0)}")
print(f"제곱x0.5: {process_items(nums, 0.5, transform_fn=lambda x: x**2)}")

# ── LEVEL 5: 파이썬 표준 라이브러리의 sentinel 활용 예 ──────────────────────

print("\nLEVEL 5: 표준 라이브러리 sentinel 패턴")
print("-" * 40)

# CPython 소스에서 _MISSING 사용 예
# dict.get(key, default=None) 에서 default 없으면 KeyError vs None 구분
# functools.lru_cache 내부에서도 sentinel 사용

# 실제 dict.setdefault 동작 재현
def my_setdefault(d, key, default=None):
    """dict.setdefault() 재현"""
    if key not in d:
        d[key] = default
    return d[key]

d = {"a": 1}
print(f"setdefault('a', 99) = {my_setdefault(d, 'a', 99)}")  # 1 (기존값 유지)
print(f"setdefault('b', 99) = {my_setdefault(d, 'b', 99)}")  # 99 (새로 설정)
print(f"d 최종 = {d}")

# 실무: 그룹핑 패턴
from collections import defaultdict

def group_by(items, key_fn):
    """키 함수로 항목을 그룹핑"""
    groups = defaultdict(list)
    for item in items:
        groups[key_fn(item)].append(item)
    return dict(groups)

words = ["apple","banana","cherry","avocado","blueberry","apricot"]
by_initial = group_by(words, lambda w: w[0])
for letter, ws in sorted(by_initial.items()):
    print(f"  {letter}: {ws}")

# ============================================================================
# [주의사항]
#   1. def f(lst=[]) 절대 금지 — list/dict/set 모두 동일
#   2. def f(ts=time.time()) 도 함정 — None으로 처리
#   3. sentinel = object() 는 반드시 모듈 레벨 싱글톤으로
#   4. or 기본값은 Falsy 전체 처리 → 0, "" 도 기본값으로 대체됨 주의
#   5. __defaults__ 속성으로 기본값 확인 가능 (디버깅 시 유용)
#
# [다음 단계]
#   → 020_variadic_argument.py: *args, **kwargs — 가변 인수
# ============================================================================
