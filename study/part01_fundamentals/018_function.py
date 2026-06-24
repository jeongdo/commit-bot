# ============================================================================
# 018 - function (함수)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. 함수가 1급 객체(first-class citizen)임을 완전히 이해한다
#   2. 다중 반환값, docstring, 타입 힌트 작성법을 익힌다
#   3. 함수의 내부 속성(__name__, __doc__, __code__, __annotations__)을 안다
#   4. 순수 함수(pure function) 설계 원칙을 체화한다
#
# [왜 필요한가]
#   - 함수 = 1급 객체: 변수에 저장, 인자로 전달, 반환값으로 사용
#   - 이 특성이 데코레이터, 클로저, 고차함수의 기반
#   - 순수 함수 설계는 테스트 가능성, 유지보수성의 핵심
#
# [Java 비교]
#   Java  : 함수는 반드시 클래스 내 메서드 — 독립 존재 불가
#           메서드 참조(::) 로 함수처럼 전달 (Java 8+)
#   Python: 함수는 최상위(top-level)에 독립 존재
#           변수에 할당, 리스트에 저장, 인자로 전달, 반환 모두 가능
# ============================================================================

import inspect
import time
from typing import Callable, Any

# ── LEVEL 1: 함수 정의 기초 ─────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 함수 정의 기초")
print("=" * 50)

def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def nothing():
    pass  # return None 과 동일

print(greet("Alice"))             # Hello, Alice!
print(add(3, 4))                  # 7
print(nothing())                  # None
print(f"nothing() is None: {nothing() is None}")

# ── LEVEL 2: 다중 반환값 ────────────────────────────────────────────────────

print("\nLEVEL 2: 다중 반환값")
print("-" * 40)

# 사실 튜플을 반환하는 것
def stats(nums: list) -> tuple:
    if not nums:
        return None, None, None, None
    return min(nums), max(nums), sum(nums)/len(nums), sum(nums)

data = [3, 1, 4, 1, 5, 9, 2, 6]
minimum, maximum, avg, total = stats(data)   # 언패킹
print(f"min={minimum}, max={maximum}, avg={avg:.2f}, sum={total}")

# 반환 타입을 명시적으로 tuple로
def divmod_custom(a: int, b: int) -> tuple[int, int]:
    return a // b, a % b   # 튜플 패킹

q, r = divmod_custom(17, 5)
print(f"17 ÷ 5 = {q} 나머지 {r}")

# ── LEVEL 2: docstring ───────────────────────────────────────────────────────

print("\nLEVEL 2: docstring")
print("-" * 40)

def fibonacci(n: int) -> list[int]:
    """
    피보나치 수열을 n번째까지 반환한다.

    Args:
        n: 생성할 피보나치 수의 개수 (1 이상)

    Returns:
        n개의 피보나치 수로 구성된 리스트

    Raises:
        ValueError: n이 1 미만인 경우

    Examples:
        >>> fibonacci(5)
        [1, 1, 2, 3, 5]
        >>> fibonacci(1)
        [1]
    """
    if n < 1:
        raise ValueError(f"n은 1 이상이어야 함 (입력: {n})")
    a, b = 1, 1
    result = [a]
    for _ in range(n - 1):
        a, b = b, a + b
        result.append(a)
    return result

print(f"fibonacci(8) = {fibonacci(8)}")
print(f"\ndocstring: {fibonacci.__doc__[:60]}...")

# ── LEVEL 3: 함수는 1급 객체 ────────────────────────────────────────────────

print("\nLEVEL 3: 함수 = 1급 객체")
print("-" * 40)

# 1) 변수에 할당
square = lambda x: x ** 2
cube   = lambda x: x ** 3

fn = square
print(f"fn(5) = {fn(5)}")   # 25

# 2) 자료구조에 저장
operations = {
    "add": lambda x, y: x + y,
    "sub": lambda x, y: x - y,
    "mul": lambda x, y: x * y,
    "div": lambda x, y: x / y if y != 0 else None,
}
for op, func in operations.items():
    print(f"  {op}(10, 3) = {func(10, 3)}")

# 3) 인자로 전달 (고차 함수)
def apply_twice(func: Callable, x: Any) -> Any:
    return func(func(x))

print(f"\napply_twice(square, 2) = {apply_twice(square, 2)}")  # (2²)²=16
print(f"apply_twice(str.upper, 'hi') = {apply_twice(str.upper, 'hi')!r}")

# 4) 반환값으로 사용 (팩토리 함수)
def make_multiplier(factor: int) -> Callable:
    """factor를 곱하는 함수를 생성해 반환"""
    def multiply(x):
        return x * factor   # factor를 클로저로 캡처
    multiply.__name__ = f"multiply_by_{factor}"
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
by_10  = make_multiplier(10)

print(f"\ndouble(5)    = {double(5)}")    # 10
print(f"triple(5)    = {triple(5)}")      # 15
print(f"by_10(5)     = {by_10(5)}")       # 50

# map()에 함수 전달
nums = [1, 2, 3, 4, 5]
doubled = list(map(double, nums))
print(f"map(double, {nums}) = {doubled}")

# ── LEVEL 3: 함수 내부 속성 ─────────────────────────────────────────────────

print("\nLEVEL 3: 함수 내부 속성")
print("-" * 40)

def example(x: int, y: int = 10) -> int:
    """예시 함수"""
    z = x + y
    return z

print(f"__name__       = {example.__name__!r}")
print(f"__qualname__   = {example.__qualname__!r}")
print(f"__doc__        = {example.__doc__!r}")
print(f"__annotations__= {example.__annotations__}")
print(f"__defaults__   = {example.__defaults__}")       # (10,) — y의 기본값

code = example.__code__
print(f"\n__code__.co_varnames  = {code.co_varnames}")
print(f"__code__.co_argcount  = {code.co_argcount}")
print(f"__code__.co_filename  = {code.co_filename}")

# inspect 모듈로 시그니처 분석
sig = inspect.signature(example)
print(f"\nSignature: {sig}")
for param_name, param in sig.parameters.items():
    print(f"  {param_name}: kind={param.kind.name}, default={param.default}")

# ── LEVEL 4: 순수 함수 설계 ─────────────────────────────────────────────────

print("\nLEVEL 4: 순수 함수 설계 원칙")
print("-" * 40)

# 순수 함수: 동일 입력 → 동일 출력, 사이드 이펙트 없음

# Bad: 순수하지 않은 함수 (전역 상태 수정)
global_tax_rate = 0.1
def calc_price_bad(base_price):
    return base_price * (1 + global_tax_rate)   # 전역 의존

# Good: 순수 함수 (모든 의존성 명시)
def calc_price(base_price: float, tax_rate: float = 0.1) -> float:
    """부가세 포함 가격 계산 — 순수 함수"""
    return round(base_price * (1 + tax_rate), 2)

print(f"calc_price(1000)         = {calc_price(1000)}")
print(f"calc_price(1000, 0.2)   = {calc_price(1000, 0.2)}")
print(f"calc_price(1000, 0.0)   = {calc_price(1000, 0.0)}")

# 순수 함수의 장점: 캐싱 가능
import functools

@functools.lru_cache(maxsize=128)
def fib_cached(n: int) -> int:
    """캐싱 가능한 순수 함수 피보나치"""
    if n <= 1:
        return n
    return fib_cached(n-1) + fib_cached(n-2)

t1 = time.perf_counter()
print(f"\nfib(35) = {fib_cached(35)}")
t2 = time.perf_counter()
print(f"fib(35) = {fib_cached(35)} (캐시 히트)")   # 즉시
t3 = time.perf_counter()
print(f"첫 번째: {(t2-t1)*1000:.3f}ms, 캐시: {(t3-t2)*1000:.4f}ms")
print(f"캐시 정보: {fib_cached.cache_info()}")

# ── LEVEL 5: 함수 조합 패턴 ─────────────────────────────────────────────────

print("\nLEVEL 5: 함수 조합 패턴")
print("-" * 40)

# compose: f(g(x)) 함수 조합
def compose(*funcs):
    """여러 함수를 오른쪽에서 왼쪽으로 합성"""
    def composed(x):
        for f in reversed(funcs):
            x = f(x)
        return x
    return composed

strip_lower_split = compose(str.split, str.lower, str.strip)
result = strip_lower_split("  Hello World Python  ")
print(f"compose(split, lower, strip)('  Hello World Python  ') = {result}")

# pipe: f(g(h(x)))를 왼쪽에서 오른쪽 순서로
def pipe(*funcs):
    def piped(x):
        for f in funcs:
            x = f(x)
        return x
    return piped

process = pipe(
    str.strip,
    str.lower,
    str.split,
    lambda words: [w.capitalize() for w in words],
    " ".join
)
result = process("  HELLO WORLD PYTHON  ")
print(f"pipe 결과: {result!r}")

# 실무: 데이터 파이프라인
def pipeline(data, *transforms):
    for transform in transforms:
        data = transform(data)
    return data

raw = [" Alice ", " BOB ", "  carol  ", " Dave "]
clean = pipeline(
    raw,
    lambda lst: [s.strip() for s in lst],
    lambda lst: [s.title() for s in lst],
    sorted,
)
print(f"\n데이터 파이프라인: {clean}")

# ============================================================================
# [주의사항]
#   1. 기본값에 mutable 사용 금지 → 019_default_argument.py에서 상세히
#   2. 함수 내 전역 변수 수정 시 global 선언 필요
#   3. 순수 함수 설계 → 테스트/재사용/캐싱 용이
#   4. lambda는 단일 표현식만 → 복잡하면 def 사용
#   5. __annotations__ 는 런타임에 영향 없음 — mypy/IDE 지원 목적
#
# [다음 단계]
#   → 019_default_argument.py: 기본값 인수 — mutable 함정 완전 정복
# ============================================================================
