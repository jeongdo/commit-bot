# ============================================================================
# 020 - variadic_argument (*args, **kwargs)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. *args (가변 위치 인수 → 튜플)와 **kwargs (가변 키워드 인수 → 딕셔너리)를 완전히 이해한다
#   2. 파라미터 선언 순서 규칙을 암기한다
#   3. * / ** 언패킹으로 호출하는 패턴을 익힌다
#   4. 범용 래퍼/데코레이터 패턴을 구현할 수 있다
#
# [왜 필요한가]
#   - 데코레이터 구현의 핵심: wrapper(*args, **kwargs)
#   - print(), format(), dict() 같은 내장 함수도 이 방식 사용
#   - 유연한 API 설계의 필수 도구
#
# [Java 비교]
#   Java  : void func(String... args)  → String[] 배열
#           varargs는 한 개만, 마지막에만, **kwargs 없음
#   Python: def func(*args, **kwargs)  → 튜플 + 딕셔너리
# ============================================================================

import functools

# ── LEVEL 1: *args 기초 ──────────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: *args 기초")
print("=" * 50)

def sum_all(*args):
    """임의 개수의 수를 받아 합계 반환"""
    print(f"  args = {args}, type = {type(args).__name__}")
    return sum(args)

print(f"sum_all()           = {sum_all()}")
print(f"sum_all(1)          = {sum_all(1)}")
print(f"sum_all(1,2,3)      = {sum_all(1,2,3)}")
print(f"sum_all(1,2,3,4,5)  = {sum_all(1,2,3,4,5)}")

# ── LEVEL 1: **kwargs 기초 ───────────────────────────────────────────────────

print("\nLEVEL 1: **kwargs 기초")

def show_info(**kwargs):
    """임의 키워드 인수를 받아 출력"""
    print(f"  kwargs = {kwargs}, type = {type(kwargs).__name__}")
    for key, val in kwargs.items():
        print(f"  {key}: {val}")

show_info()
show_info(name="Alice", age=30)
show_info(name="Bob", role="admin", active=True)

# ── LEVEL 2: 혼합 파라미터 선언 순서 ────────────────────────────────────────

print("\nLEVEL 2: 파라미터 선언 순서")
print("-" * 40)

# 순서: 일반 → *args → 키워드전용 → **kwargs
def full_signature(
    required,           # 필수 위치 인수
    optional=10,        # 기본값 있는 위치 인수
    *args,              # 나머지 위치 인수 → 튜플
    kw_only="default",  # *args 뒤 → 키워드 전용
    **kwargs            # 나머지 키워드 인수 → 딕셔너리
):
    print(f"  required={required!r}, optional={optional!r}")
    print(f"  args={args}")
    print(f"  kw_only={kw_only!r}")
    print(f"  kwargs={kwargs}")

print("full_signature(1, 2, 3, 4, kw_only='hi', x=10, y=20):")
full_signature(1, 2, 3, 4, kw_only="hi", x=10, y=20)

# ── LEVEL 2: * / ** 언패킹으로 전달 ─────────────────────────────────────────

print("\nLEVEL 2: 언패킹으로 전달")
print("-" * 40)

def add(a, b, c):
    return a + b + c

# 리스트/튜플 → * 언패킹
args_list = [1, 2, 3]
print(f"add(*[1,2,3])  = {add(*args_list)}")

args_tuple = (10, 20, 30)
print(f"add(*(10,20,30)) = {add(*args_tuple)}")

# 딕셔너리 → ** 언패킹
kwargs_dict = {"a": 100, "b": 200, "c": 300}
print(f"add(**{{a:100,...}}) = {add(**kwargs_dict)}")

# 혼합
print(f"add(1, *[2,3]) = {add(1, *[2, 3])}")

# 리스트/딕셔너리 병합에도 활용
list1 = [1, 2, 3]
list2 = [4, 5, 6]
merged = [*list1, *list2, 7, 8]
print(f"\n[*list1, *list2, 7, 8] = {merged}")

d1 = {"a": 1, "b": 2}
d2 = {"b": 99, "c": 3}   # b 충돌 → d2가 우선
merged_d = {**d1, **d2}
print(f"{{**d1, **d2}} = {merged_d}")  # b=99 (d2 우선)

# ── LEVEL 3: 내부 동작 — 패킹/언패킹 과정 ───────────────────────────────────

print("\nLEVEL 3: 내부 동작")
print("-" * 40)

# Python이 *args 처리하는 방식 재현
def trace_args(*args, **kwargs):
    print(f"  args    = {args!r}   (튜플, 불변)")
    print(f"  kwargs  = {kwargs!r}  (딕셔너리, 가변)")

    # args 순회
    for i, a in enumerate(args):
        print(f"  args[{i}] = {a!r}")

    # kwargs 순회
    for k, v in kwargs.items():
        print(f"  kwargs[{k!r}] = {v!r}")

trace_args("pos1", "pos2", 42, key1="val1", key2=100)

# ── LEVEL 4: 범용 래퍼 패턴 — 데코레이터의 핵심 ────────────────────────────

print("\nLEVEL 4: 범용 래퍼 패턴")
print("-" * 40)

# 패턴 1: 타이밍 데코레이터
def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start  = time.perf_counter()
        result = func(*args, **kwargs)           # 원본 함수 호출
        elapsed= time.perf_counter() - start
        print(f"  [{func.__name__}] {elapsed*1000:.3f}ms")
        return result
    return wrapper

@timed
def slow_add(a, b, delay=0.001):
    import time
    time.sleep(delay)
    return a + b

result = slow_add(3, 4)
print(f"  결과: {result}")

# 패턴 2: 로깅 데코레이터
def logged(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr   = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature   = ", ".join(args_repr + kwargs_repr)
        print(f"  호출: {func.__name__}({signature})")
        try:
            result = func(*args, **kwargs)
            print(f"  반환: {result!r}")
            return result
        except Exception as e:
            print(f"  예외: {type(e).__name__}: {e}")
            raise
    return wrapper

@logged
def divide(a, b):
    return a / b

divide(10, 4)
try:
    divide(1, 0)
except ZeroDivisionError:
    pass

# 패턴 3: 캐싱 데코레이터
def simple_cache(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
            print(f"  [MISS] {func.__name__}{args} → {cache[key]}")
        else:
            print(f"  [HIT ] {func.__name__}{args} → {cache[key]}")
        return cache[key]
    wrapper.cache = cache
    return wrapper

@simple_cache
def factorial(n):
    return 1 if n <= 1 else n * factorial.__wrapped__(n-1)

# functools.wraps 는 __wrapped__ 속성도 설정
factorial.__wrapped__ = factorial.__wrapped__ if hasattr(factorial, "__wrapped__") else (lambda n: 1 if n<=1 else n*(n-1))
for n in [3, 4, 3, 5]:
    print(f"  factorial({n}) = {factorial(n)}")

# ── LEVEL 5: 오픈소스 패턴 ──────────────────────────────────────────────────

print("\nLEVEL 5: 오픈소스 패턴")
print("-" * 40)

# Flask/FastAPI 라우팅 데코레이터 스타일
class Router:
    def __init__(self):
        self.routes = {}

    def route(self, path, methods=None):
        methods = methods or ["GET"]
        def decorator(func):
            self.routes[path] = {"handler": func, "methods": methods}
            return func
        return decorator

    def dispatch(self, path, method="GET", **request_data):
        if path not in self.routes:
            return {"error": "404 Not Found"}
        route_info = self.routes[path]
        if method not in route_info["methods"]:
            return {"error": "405 Method Not Allowed"}
        return route_info["handler"](**request_data)

app = Router()

@app.route("/users", methods=["GET"])
def get_users(limit=10, **kwargs):
    return {"users": [f"user_{i}" for i in range(1, min(limit+1, 4))]}

@app.route("/users", methods=["POST"])
def create_user(**data):
    return {"created": data}

print(f"GET  /users      : {app.dispatch('/users', 'GET', limit=3)}")
print(f"POST /users      : {app.dispatch('/users', 'POST', name='Alice', role='admin')}")
print(f"DELETE /users    : {app.dispatch('/users', 'DELETE')}")
print(f"GET  /not-found  : {app.dispatch('/not-found')}")

# ============================================================================
# [주의사항]
#   1. 선언 순서: positional → *args → keyword-only → **kwargs
#   2. *args 와 **kwargs 는 이름 변경 가능 (관례상 *args/**kwargs)
#   3. @functools.wraps(func) 없으면 __name__, __doc__ 소실
#   4. **kwargs 병합 시 같은 키: 마지막이 우선 ({**d1, **d2} → d2)
#   5. 함수 호출 시 * 언패킹 후 추가 위치 인수 불가
#
# [다음 단계]
#   → 021_keyword_argument.py: 키워드 전용 인수, / 위치 전용 인수
# ============================================================================
