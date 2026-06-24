# ============================================================================
# 023 - local_variable (지역 변수와 스택 프레임)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. 지역 변수의 생존 범위(scope)와 생명주기(lifetime)를 이해한다
#   2. 스택 프레임 개념으로 함수 호출/반환 시 변수 생성/소멸을 안다
#   3. 클로저에서 루프 변수 캡처 함정(late binding)을 피한다
#   4. locals()로 스택 프레임의 지역 변수를 관찰한다
# ============================================================================

import sys
import inspect

# ── LEVEL 1: 지역 변수 기초 ─────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 지역 변수 기초")
print("=" * 50)

name = "Global Alice"  # 전역 변수

def greet():
    name = "Local Bob"    # 지역 변수 (전역과 별개!)
    print(f"  함수 내 name = {name!r}")   # Local Bob

greet()
print(f"전역 name = {name!r}")  # Global Alice (영향 없음)

# 지역 변수는 함수 밖에서 접근 불가
def create_secret():
    secret = "shhh"
    return secret   # 값은 반환 가능

result = create_secret()
print(f"\nresult = {result!r}")   # 'shhh'
try:
    print(secret)
except NameError as e:
    print(f"외부 접근 불가: {e}")

# ── LEVEL 2: 지역 변수의 생명주기 ───────────────────────────────────────────

print("\nLEVEL 2: 지역 변수 생명주기")
print("-" * 40)

# 함수 호출마다 새 스택 프레임 → 새 지역 변수
def stateful_demo(n):
    count = 0     # 매 호출마다 새로 생성
    for i in range(n):
        count += 1
    print(f"  count = {count} (n={n})")
    return count

for _ in range(3):
    stateful_demo(5)   # 항상 count=5 (이전 호출 영향 없음)

# locals() — 현재 스택 프레임의 지역 변수 딕셔너리 (복사본!)
def show_locals():
    x = 1
    y = 2
    z = x + y
    local_ns = locals()
    print(f"  locals() = {local_ns}")
    local_ns["x"] = 999   # 복사본 수정 → 실제 변수에 영향 없음
    print(f"  x after locals()['x']=999 → x = {x}")  # 여전히 1

show_locals()

# ── LEVEL 3: 스택 프레임 직접 관찰 ─────────────────────────────────────────

print("\nLEVEL 3: 스택 프레임 관찰")
print("-" * 40)

def level_c():
    frame = sys._getframe()
    print(f"  level_c 프레임:")
    print(f"    f_code.co_name    = {frame.f_code.co_name}")
    print(f"    f_code.co_filename = ...{frame.f_code.co_filename[-20:]}")
    print(f"    f_lineno          = {frame.f_lineno}")
    print(f"    f_locals (진입시) = {dict(frame.f_locals)}")

    local_a = 10
    local_b = "hello"
    print(f"    f_locals (변수 후)= {frame.f_locals}")
    return "C 완료"

def level_b():
    b_var = 42
    result = level_c()
    return result

def level_a():
    a_var = "start"
    return level_b()

level_a()

# 호출 스택 추적
def get_call_stack():
    stack = []
    frame = sys._getframe(1)
    while frame:
        info = inspect.getframeinfo(frame)
        stack.append(f"{info.function}()  @ line {info.lineno}")
        frame = frame.f_back
    return stack

def deep3():
    return get_call_stack()

def deep2():
    return deep3()

def deep1():
    return deep2()

print("\n호출 스택:")
for line in deep1():
    print(f"  {line}")

# ── LEVEL 4: 클로저 루프 변수 함정 (late binding) ────────────────────────────

print("\nLEVEL 4: 클로저 루프 변수 함정")
print("-" * 40)

# BAD: late binding — 루프 변수를 나중에 참조
funcs_bad = []
for i in range(5):
    funcs_bad.append(lambda: i)   # i를 캡처하는 게 아님! 이름 i를 참조

print("BAD (late binding):")
print(f"  결과: {[f() for f in funcs_bad]}")  # [4,4,4,4,4] ← 모두 마지막 i

# 이유: 람다는 i라는 이름을 참조 (값이 아님)
# 루프 종료 후 i=4 → 모든 람다가 i=4 반환

# GOOD 방법 1: 기본값으로 현재 값 캡처
funcs_good1 = []
for i in range(5):
    funcs_good1.append(lambda i=i: i)   # i=i: 현재 i값을 기본값으로 고정!

print("\nGOOD 방법1 (기본값 캡처):")
print(f"  결과: {[f() for f in funcs_good1]}")  # [0,1,2,3,4]

# GOOD 방법 2: 팩토리 함수로 새 스코프 생성
def make_func(val):
    return lambda: val   # val은 make_func의 지역 변수 → 각각 독립

funcs_good2 = [make_func(i) for i in range(5)]
print("\nGOOD 방법2 (팩토리 함수):")
print(f"  결과: {[f() for f in funcs_good2]}")  # [0,1,2,3,4]

# GOOD 방법 3: functools.partial
from functools import partial

def get_value(i): return i
funcs_good3 = [partial(get_value, i) for i in range(5)]
print("\nGOOD 방법3 (partial):")
print(f"  결과: {[f() for f in funcs_good3]}")  # [0,1,2,3,4]

# ── LEVEL 5: 지역 변수 최적화 패턴 ─────────────────────────────────────────

print("\nLEVEL 5: 지역 변수 최적화")
print("-" * 40)

import time

# 전역 함수를 지역 변수에 바인딩하면 빠름 (LEGB 탐색 단축)
data = list(range(10000))

# 일반: 매번 LEGB로 len, range 탐색
def no_local():
    total = 0
    for i in range(len(data)):
        total += data[i]
    return total

# 최적화: 지역 변수에 바인딩
def with_local():
    _data = data            # 지역 변수에 바인딩 (G→L 탐색 단축)
    _range = range         # 내장 함수를 지역에
    _len = len
    total = 0
    for i in _range(_len(_data)):
        total += _data[i]
    return total

t1 = time.perf_counter()
for _ in range(100): no_local()
t1 = time.perf_counter() - t1

t2 = time.perf_counter()
for _ in range(100): with_local()
t2 = time.perf_counter() - t2

print(f"일반 (100회)  : {t1*1000:.2f}ms")
print(f"지역최적화(100): {t2*1000:.2f}ms")

# ============================================================================
# [주의사항]
#   1. 함수 내 같은 이름 변수가 있으면 전역 접근 위해 global 선언 필수
#   2. locals() 수정은 실제 변수에 영향 없음 (복사본)
#   3. 클로저 루프 변수: lambda x=x: x 패턴 또는 팩토리 함수 사용
#   4. sys._getframe()은 CPython 전용 (구현체 독립 코드에선 inspect 사용)
#   5. 지역 변수 최적화는 타이트 루프에서만 의미 있음
#
# [다음 단계]
#   → 024_global_variable.py: 전역 변수 — 안티패턴과 대안
# ============================================================================
