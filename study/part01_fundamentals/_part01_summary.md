# PART 01 — Python Fundamentals 요약

> 총 25개 파일 | LEVEL 1~5 단계별 구성 | Java/Spring 개발자 기준 설명

---

## 📌 파트 개요

| 구분 | 내용 |
|------|------|
| 대상 | Java/Spring 백엔드 개발자 |
| 목표 | Python 기초 문법 + Pythonic 사고방식 전환 |
| 핵심 | 동적 타이핑, 이름표 모델, Falsy/Truthy, LEGB |

---

## 📂 파일 목록과 핵심 개념

| 파일 | 주제 | 핵심 포인트 |
|------|------|------------|
| `001_print.py` | print() | sep/end/file/flush, 내부=write+flush, logging 전환 |
| `002_variable.py` | 변수 | 이름표 모델, id/is/==, 소형정수캐싱, 동적타이핑 |
| `003_data_type.py` | 데이터 타입 | type() vs isinstance(), Falsy 전체, 안전 변환 |
| `004_type.py` | type() | 타입조회+동적클래스생성, MRO, 메타클래스 입문 |
| `005_bool.py` | bool | int 서브클래스, 단락평가, __bool__/__len__ |
| `006_int.py` | int | 무제한정밀도, 비트연산, floor vs truncate |
| `007_float.py` | float | IEEE754 함정, decimal, math.isclose |
| `008_str.py` | str | 불변성, f-string 전체, join vs +, 인코딩 |
| `009_input.py` | input() | 항상 str 반환, 검증 패턴, argparse 대안 |
| `010_eval.py` | eval/exec | 보안위험, ast.literal_eval, 제한 네임스페이스 |
| `011_operator.py` | 연산자 | 체이닝비교, operator 모듈, 오버로딩 예고 |
| `012_comparison.py` | 비교 | @total_ordering, __eq__+__hash__ 짝꿍 |
| `013_if.py` | 조건문 | 가드클로즈, 딕셔너리 디스패치, match/case |
| `014_for.py` | for 루프 | 이터러블 프로토콜, for-else, enumerate/zip |
| `015_while.py` | while 루프 | while-else, retry/backoff 패턴, 타임아웃 |
| `016_range.py` | range() | 게으른 시퀀스, O(1) in, 배치처리 패턴 |
| `017_nested_loop.py` | 중첩 루프 | break 범위, 외부탈출 3가지, product |
| `018_function.py` | 함수 | 1급객체, 다중반환, docstring, 순수함수 |
| `019_default_argument.py` | 기본값 인수 | mutable 함정, None 패턴, sentinel |
| `020_variadic_argument.py` | *args/**kwargs | 선언순서, 언패킹, 범용 래퍼/데코레이터 |
| `021_keyword_argument.py` | 키워드 인수 | * 키워드전용, / 위치전용, inspect 분석 |
| `022_namespace.py` | 네임스페이스 | LEGB 규칙, global/nonlocal, 플러그인 패턴 |
| `023_local_variable.py` | 지역 변수 | 스택 프레임, late binding 함정, 최적화 |
| `024_global_variable.py` | 전역 변수 | 문제점, 클래스 캡슐화, 스레드안전 |
| `025_main_function.py` | __name__ | import vs 실행, main() 설계, sys.exit() |

---

## 🔑 Java 개발자 필수 체크포인트

### 1. 변수 모델의 차이
```python
# Java: int x = 10;  → x 상자에 값 10 저장
# Python: x = 10     → 정수 객체 10에 x 이름표 붙임

a = [1, 2, 3]
b = a           # 같은 리스트를 두 이름이 참조
b.append(4)
print(a)        # [1, 2, 3, 4] ← a도 변경!
```

### 2. is vs == 구분
```python
# is: 동일 객체 (같은 메모리 주소)
# ==: 값이 같음

a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)    # True  (값 같음)
print(a is b)    # False (다른 객체)

# None은 반드시 is 비교!
result = None
print(result is None)    # ✓ 올바름
print(result == None)    # 작동하지만 비권장
```

### 3. 동적 타이핑과 Falsy
```python
# Java: 0은 false가 아님, ""은 false가 아님
# Python: 0, "", [], {}, None 모두 False!

if []:
    print("실행 안 됨")   # 빈 리스트는 Falsy

if "hello":
    print("실행됨")       # 비어있지 않은 문자열 Truthy

# 단락 평가 활용
name = user_input or "Guest"   # None/""/"0" 모두 처리
```

### 4. 나눗셈 차이
```python
# Java: 7 / 2 = 3  (정수 나눗셈, truncate)
# Python: 7 / 2 = 3.5 (항상 float!)
# Python: 7 // 2 = 3  (정수 원하면 //)

# 음수 차이:
# Java:  -7 / 2 = -3  (truncate toward 0)
# Python: -7 // 2 = -4 (floor toward -∞)
```

### 5. mutable 기본값 함정
```python
# Java: void f(List<String> lst) { } → 매번 새 리스트를 인자로 전달
# Python에서 절대 하지 말 것:
def bad(lst=[]):     # 모든 호출이 같은 리스트 공유!
    lst.append(1)
    return lst

bad()  # [1]
bad()  # [1, 1] ← 예상은 [1] 이었는데!

# 올바른 방법:
def good(lst=None):
    if lst is None:
        lst = []
    lst.append(1)
    return lst
```

### 6. for 루프 차이
```python
# Java: for(int i=0; i<list.size(); i++) — 인덱스 기반
# Python: for item in list — 항상 for-each!

# Python에서 인덱스 필요시:
for i, item in enumerate(items):   # ← range(len(items)) 대신!
    print(f"{i}: {item}")
```

### 7. 함수는 1급 객체
```python
# Java: 메서드는 클래스 내에만 존재 (Java 8+ 람다 제외)
# Python: 함수는 변수에 저장, 인자로 전달, 반환 가능

def double(x): return x * 2

funcs = [double, str, abs]      # 리스트에 저장
result = map(double, [1,2,3])   # 인자로 전달
```

---

## ⚡ 핵심 패턴 30개

```python
# 1. 스왑 (임시 변수 불필요)
a, b = b, a

# 2. 다중 할당
x = y = z = 0

# 3. 언패킹
first, *rest = [1, 2, 3, 4, 5]

# 4. 삼항 표현식
label = "양수" if x > 0 else "음수"

# 5. None 안전 기본값 (falsy 전체)
val = user_input or "default"

# 6. None만 체크
val = x if x is not None else default

# 7. 여러 타입 isinstance
isinstance(x, (int, float))

# 8. 안전한 타입 변환
def safe_int(v, d=0):
    try: return int(v)
    except: return d

# 9. in으로 멤버십 (O(1) set)
if status in {"active", "pending"}:

# 10. 체이닝 비교
if 0 < x <= 100:

# 11. for-else 검색
for item in collection:
    if condition(item): break
else:
    handle_not_found()

# 12. enumerate
for i, item in enumerate(items, start=1):

# 13. zip 병렬 순회
for name, score in zip(names, scores):

# 14. 딕셔너리 안전 접근
val = d.get("key", "default")

# 15. 단락 평가 체인 (None guard)
name = user and user.get("profile") and user["profile"].get("name")

# 16. all/any
all(x > 0 for x in nums)
any(x > 100 for x in nums)

# 17. *args 래퍼
def wrapper(*args, **kwargs):
    return original(*args, **kwargs)

# 18. ** 딕셔너리 병합
merged = {**defaults, **overrides}

# 19. * 리스트 병합
combined = [*list1, *list2]

# 20. 가드 클로즈
def process(data):
    if not data: return "없음"
    if not data.get("id"): return "ID 없음"
    # 핵심 로직

# 21. 딕셔너리 디스패치
handlers = {"cmd1": fn1, "cmd2": fn2}
result = handlers.get(cmd, default_fn)(args)

# 22. 함수 팩토리 (클로저)
def make_multiplier(n):
    return lambda x: x * n
double = make_multiplier(2)

# 23. 데코레이터 기본 구조
def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# 24. mutable 기본값 None 패턴
def f(lst=None):
    if lst is None: lst = []

# 25. sentinel 패턴
_MISSING = object()
def f(key, default=_MISSING):
    if default is _MISSING: raise KeyError(key)
    return default

# 26. 비트 플래그
READ, WRITE, EXEC = 1, 2, 4
has_read = bool(perms & READ)
add_write = perms | WRITE
del_exec  = perms & ~EXEC

# 27. global 카운터 대신 클래스
class Counter:
    def __init__(self): self._n = 0
    def inc(self): self._n += 1; return self._n

# 28. while True + break 서버 루프
while True:
    event = queue.get()
    if event.type == "SHUTDOWN": break
    process(event)

# 29. main() 설계
def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        run(args)
        return 0
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())

# 30. late binding 함정 해결
funcs = [lambda x, i=i: x + i for i in range(5)]
```

---

## 🧪 실습 문제

### 기초 (LEVEL 1~2)

1. `sum_stats(*nums)` 함수를 작성하라 — 임의 개수의 숫자를 받아 (합계, 평균, 최솟값, 최댓값)를 반환한다.

2. 아래 코드의 문제를 찾고 수정하라:
   ```python
   def add_tag(item, tags=[]):
       tags.append(item)
       return tags
   ```

3. `safe_divide(a, b, default=None)` 함수를 작성하라 — 0으로 나누면 default를 반환한다.

4. LEGB 규칙을 확인하는 예제 코드를 작성하라 (전역, 외부함수, 내부함수, 내장 모두 포함).

### 실전 (LEVEL 3~4)

5. `retry_decorator(max=3, delay=0.1, exceptions=(Exception,))` 데코레이터를 구현하라.

6. `make_counter(start=0, step=1)` 클로저를 구현하라 — increment(), decrement(), reset(), value() 반환.

7. 딕셔너리 디스패치로 간단한 계산기를 구현하라 — `calc("add", 10, 5)` 형태.

8. `process_order(order)` 함수를 가드 클로즈 패턴으로 구현하라.

### 리팩토링 (LEVEL 5)

9. 아래를 Pythonic하게 리팩토링하라:
   ```python
   result = []
   for i in range(len(items)):
       if items[i] % 2 == 0:
           result.append(items[i] * 2)
   ```

10. 클로저 루프 함정이 있는 코드를 찾아 3가지 방법으로 수정하라:
    ```python
    handlers = []
    for i in range(5):
        handlers.append(lambda: print(i))
    ```

---

## 🔧 미니 프로젝트: 타입 안전 설정 관리자

```python
# 요구사항:
# 1. 타입 힌트 + 검증을 포함한 설정 클래스
# 2. 환경변수에서 설정 로드 (os.environ)
# 3. 기본값 + 타입 강제 변환
# 4. 설정 변경 이벤트 콜백 지원
# 5. 커맨드라인 인수 오버라이드

class Config:
    _schema = {
        "debug":   (bool,  False),
        "host":    (str,   "localhost"),
        "port":    (int,   8080),
        "workers": (int,   4),
    }
    # ... 구현
```

---

## 📚 다음 단계

**→ PART 02: Sequence & Collection**
- `list`, `tuple`, `str`, `set`, `dict` 심화
- `enumerate`, `zip`, `sorted`, `reversed`
- 내장 함수 `max`, `min`, `sum`, `any`, `all`
- 이전 PART와의 연결: 변수/타입 → 컬렉션 조작
