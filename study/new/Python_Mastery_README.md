# 🐍 Python Mastery Curriculum

> **대상**: Java/Spring 백엔드 개발자 → Python 언어 완전 정복  
> **목표**: 단순 문법 암기가 아닌 **Pythonic Thinking** + 오픈소스 코드 리딩 능력  
> **구성**: 25 PART · 286 파일 · LEVEL 1~5 단계별 심화  

---

## 📐 예제 작성 형식 (전 파일 공통)

모든 `.py` 파일은 아래 10개 섹션으로 구성됩니다.

| # | 섹션 | 설명 |
|---|------|------|
| 1 | **제목** | 파일 주제 |
| 2 | **학습 목표** | 이 파일에서 얻어야 할 것 |
| 3 | **왜 필요한가** | 이 문법이 존재하는 이유 |
| 4 | **Java와 비교** | Java 개발자 관점 대조 |
| 5 | **실무 사용 사례** | 실제 코드베이스 활용 |
| 6 | **전체 코드** | LEVEL 1~5 단계별 예제 |
| 7 | **실행 결과** | 주석으로 모든 출력 명시 |
| 8 | **내부 동작** | CPython 수준 설명 |
| 9 | **주의사항** | 흔한 실수 · 함정 |
| 10 | **다음 단계** | 연결 파일 안내 |

---

## 🎯 난이도 체계

| LEVEL | 의미 |
|-------|------|
| **LEVEL 1** | 기초 문법 — 동작 확인 |
| **LEVEL 2** | 실전 사용 — 조합 패턴 |
| **LEVEL 3** | 내부 동작 원리 — CPython 관점 |
| **LEVEL 4** | 실무 예제 — 프로덕션 패턴 |
| **LEVEL 5** | 오픈소스 코드에서 발견되는 형태 |

---

## 📁 전체 커리큘럼 구조

```
python_mastery/
├── part01_fundamentals/          # 001~025
├── part02_sequence_collection/   # 026~050
├── part03_collection_mastery/    # 051~070
├── part04_comprehension_functional/ # 071~080
├── part05_object_memory/         # 081~090
├── part06_function_advanced/     # 091~098
├── part07_oop/                   # 099~114
├── part08_encapsulation/         # 115~122
├── part09_special_methods/       # 123~139
├── part10_iterator_generator_async/ # 140~153
├── part11_exception/             # 154~159
├── part12_module_package/        # 160~167
├── part13_file_path/             # 168~176
├── part14_data_processing/       # 177~183
├── part15_collections_module/    # 184~189
├── part16_itertools/             # 190~197
├── part17_type_hint/             # 198~206
├── part18_concurrency/           # 207~216
├── part19_metaprogramming/       # 217~226
├── part20_modern_python/         # 227~232
├── part21_numpy/                 # 233~244
├── part22_pandas/                # 245~252
├── part23_pytorch_reading/       # 253~265
├── part24_cpython_internals/     # 266~276
└── part25_projects/              # 277~286
```

---

## PART 01 · Python Fundamentals

> **개념 흐름**: 출력 → 변수/타입 → 연산자 → 제어문 → 함수 → 스코프  
> **선수 지식**: 없음  
> **Java 개발자 핵심 체크**: 동적 타이핑, Falsy/Truthy, mutable 기본값 함정, LEGB 규칙

---

### `001_print.py`
**핵심**: `print()`는 `sys.stdout.write()` + 포맷의 wrapper  
- `sep`, `end`, `file`, `flush` 4개 파라미터 완전 제어  
- `flush=True`로 실시간 프로그레스 출력 (버퍼 즉시 비우기)  
- `file=sys.stderr`로 에러 스트림 분리, `StringIO`로 출력 캡처  
- ANSI 컬러 코드 적용, 테이블 포맷 출력  
- **실무 전환**: 실무에서는 `print()` → `logging` 모듈 권장

---

### `002_variable.py`
**핵심**: Python 변수 = 이름표(label), 상자(box)가 아님  
- 동적 타이핑: 같은 변수명이 다른 타입을 가리킬 수 있음  
- `id()` = CPython에서 메모리 주소, `is` = 동일 객체 비교  
- 다중 할당 `a, b = 1, 2`, 스왑 `a, b = b, a` (Java는 temp 필요)  
- 소형 정수 캐싱(-5~256), 문자열 intern → `is` 함정  
- PEP 8: `snake_case` 변수, `UPPER_SNAKE` 상수

---

### `003_data_type.py`
**핵심**: Python은 모든 것이 객체, primitive 타입 없음  
- `int`, `float`, `complex`, `bool`, `str`, `bytes`, `list`, `tuple`, `set`, `frozenset`, `dict`, `None`  
- `type()` = 정확한 클래스 반환, `isinstance()` = 상속 고려 (권장)  
- Falsy 값 전체: `0, 0.0, 0j, "", [], (), {}, set(), None, False`  
- 명시적 변환: `int("42")`, `float("3.14")`, `list("abc")` → `['a','b','c']`  
- `bool`은 `int`의 서브클래스 → `True + True == 2`

---

### `004_type.py`
**핵심**: `type()`의 두 얼굴 — 타입 조회 + 동적 클래스 생성  
- `type(obj)` → 클래스 반환  
- `type(이름, 부모, 속성dict)` → 런타임 클래스 생성 (메타프로그래밍 시작점)  
- `__name__`, `__qualname__`, `__mro__` 속성  
- `issubclass(bool, int)` True, `isinstance(int, type)` True  
- `functools.singledispatch`로 타입 기반 함수 오버로딩

---

### `005_bool.py`
**핵심**: `bool`은 `int` 서브클래스, `True==1`, `False==0`  
- 단락 평가(short-circuit): `and`는 첫 Falsy 반환, `or`는 첫 Truthy 반환  
- `x or "default"` 패턴 vs `x if x is not None else "default"` 차이  
- `all()`, `any()`로 이터러블 조건 검사  
- `__bool__` 없으면 `__len__` 사용, 둘 다 없으면 항상 `True`  
- **함정**: `"" or "default"`는 빈 문자열도 잡아버림

---

### `006_int.py`
**핵심**: Python int = 무제한 정밀도 (오버플로우 없음)  
- `2**1000` 정확히 계산, `math.factorial(100)` 완전 출력  
- 진수 리터럴: `0xFF`, `0o377`, `0b11111111` / 변환: `hex()`, `bin()`, `oct()`  
- 비트 연산: `&`, `|`, `^`, `~`, `<<`, `>>` — 권한 플래그 패턴  
- `1_000_000_000` 언더스코어 가독성, `divmod(17,5)` → `(3,2)`  
- **Java 차이**: `-7 // 2 == -4` (floor), Java는 `-3` (truncate)

---

### `007_float.py`
**핵심**: IEEE 754 64비트 배정밀도 — 정밀도 한계 이해  
- `0.1 + 0.2 != 0.3` 이유: 이진 부동소수점 표현 불가  
- 올바른 비교: `math.isclose(a, b, rel_tol=1e-9)`  
- **금융 계산은 무조건** `decimal.Decimal("0.1")` — str로 초기화  
- `float('inf')`, `float('nan')`, `math.isinf()`, `math.isnan()`  
- `round(2.5) == 2` (Banker's rounding), `fractions.Fraction(1,3)`

---

### `008_str.py`
**핵심**: `str`은 유니코드 불변 시퀀스  
- f-string `f"{name!r}"`, `f"{n:#x}"`, `f"{x=}"` (3.8+ 디버깅)  
- 이스케이프, raw string `r"C:\path"`, 멀티라인 `"""`  
- 불변이므로 `s[0] = "H"` → TypeError, 수정 = 새 객체 반환  
- 대용량 연결은 `+` 금지 → `"".join(parts)` (O(n) vs O(n²))  
- 인코딩: `str.encode("utf-8")` → `bytes`, `bytes.decode("utf-8")` → `str`

---

### `009_input.py`
**핵심**: `input()`은 **항상 str 반환** — 타입 변환 필수  
- `int(input())`, `map(int, input().split())` 패턴  
- `a, b = map(int, input().split())` 다중 변수 언패킹  
- 입력 검증: while + try/except 루프 패턴  
- **실무 대안**: `argparse`, `os.environ`, `json` 설정 파일  
- `EOFError` 처리 (Ctrl+D / 파이프 입력 끝)

---

### `010_eval.py`
**핵심**: `eval()`의 강력함과 위험성  
- `eval("1+2*3")` → 7, 표현식만 평가  
- `exec("x=10")` → None, 문(statement) 실행  
- **보안**: 사용자 입력을 eval에 절대 넣지 말 것 (임의 코드 실행)  
- **안전 대안**: `ast.literal_eval()` — 파이썬 리터럴만 허용  
- 제한된 네임스페이스로 `eval` 샌드박싱, `compile()`로 코드 캐싱

---

### `011_operator.py`
**핵심**: Python 연산자 완전 정복  
- `//` 정수 나눗셈, `**` 거듭제곱, `%` 나머지  
- **체이닝 비교**: `1 < x < 10` (Java 불가!)  
- `is` / `is not` = 동일 객체, `==` = 값 비교 — `None`은 반드시 `is`  
- `in` / `not in` 멤버십 연산 (리스트 O(n), set O(1))  
- `operator` 모듈: `operator.add`, `operator.itemgetter` → `reduce`, `sorted`에 전달

---

### `012_comparison.py`
**핵심**: 비교 연산자 심화 + 사용자 정의 클래스 정렬  
- `@total_ordering` — `__eq__` + `__lt__` 하나만 정의 → 나머지 자동  
- `__eq__` 재정의 시 `__hash__` 도 함께 정의 (set/dict 키 사용)  
- `NotImplemented` 반환 — 비교 불가 타입에 대한 올바른 처리  
- 다중 키 정렬: `key=lambda s: (s["grade"], -s["score"])`  
- 문자열 비교는 사전순, 리스트/튜플 비교는 원소별

---

### `013_if.py`
**핵심**: 조건문과 분기 패턴  
- 삼항 표현식: `value_if_true if condition else value_if_false`  
- 딕셔너리로 switch-case 대체: `handlers.get(action, default)()`  
- **가드 클로즈(Guard Clause)**: 중첩 if → 조기 return으로 평탄화  
- 컴프리헨션 내 조건: `[abs(n) if n < 0 else n for n in nums]`  
- 함수 테이블 패턴 (Strategy): `handlers = {"add": add_func, ...}`

---

### `014_for.py`
**핵심**: `for`문은 항상 for-each — 이터러블 프로토콜 기반  
- 내부 동작: `iter(iterable)` → `next()` 반복 → `StopIteration` 종료  
- `for-else`: `break` 없이 정상 완료 시 `else` 실행 — 검색 패턴  
- `enumerate()`, `zip()` 미리 보기  
- **Java 차이**: `for i in range(n)` vs `for(int i=0; i<n; i++)`  
- 루프 내 리스트 수정 금지 → 복사본 또는 컴프리헨션 사용

---

### `015_while.py`
**핵심**: `while True + break` 서버/이벤트 루프 패턴  
- `do-while` 없음 → `while True: ... if condition: break`  
- `while-else`: 조건이 `False`로 자연 종료 시 실행  
- 재시도(retry) 메커니즘: `while attempt < max_attempts`  
- `deque`를 큐로: `while queue:` (큐가 비면 False)  
- 무한 루프 탈출 조건 명확히 설계할 것

---

### `016_range.py`
**핵심**: `range`는 리스트가 아닌 **게으른(lazy) 시퀀스 객체**  
- `sys.getsizeof(range(1_000_000)) == 48` (항상 고정 크기!)  
- `in` 연산 O(1): `5 in range(1_000_000)` 즉시 계산  
- `range.start`, `range.stop`, `range.step` 속성  
- 배치 처리: `range(0, len(data), batch_size)`  
- 역순: `range(len(items)-1, -1, -1)` / 스텝 슬라이싱: `range[::2]`

---

### `017_nested_loop.py`
**핵심**: 중첩 루프와 외부 루프 탈출 전략  
- `break`는 가장 안쪽 루프만 탈출 (Java `레이블 break` 없음)  
- 외부 탈출 방법 3가지: 플래그 변수, **함수+return(권장)**, `itertools.product`  
- `itertools.product(range(5), range(5))` → 중첩 루프 단일화  
- 행렬 전치: 리스트 컴프리헨션 이중 중첩  
- 복잡도 주의: O(n²) 이상 루프는 알고리즘 재검토

---

### `018_function.py`
**핵심**: 함수는 **1급 객체(first-class citizen)**  
- 변수에 할당, 리스트에 저장, 인자로 전달, 반환값으로 사용 가능  
- 다중 반환값 = 사실 **튜플 반환** → 언패킹  
- `docstring`: `"""` 삼중 따옴표, `__doc__` 속성, `help()` 연동  
- 타입 힌트: `def add(a: int, b: int) -> int:` (실행에 영향 없음)  
- 클로저 예고: 내부 함수가 외부 변수 캡처

---

### `019_default_argument.py`
**핵심**: mutable 기본값은 모든 호출이 공유 — 가장 유명한 함정  
- `def f(lst=[])` → 모든 호출이 같은 리스트 사용!  
- **정답**: `def f(lst=None): if lst is None: lst = []`  
- 기본값은 **함수 정의 시 단 한 번** 평가됨  
- `_MISSING = object()` sentinel 패턴 — `None`과 구분이 필요할 때  
- `time.time()` 기본값 함정 → `None` 후 함수 내에서 호출

---

### `020_variadic_argument.py`
**핵심**: `*args` (튜플) + `**kwargs` (딕셔너리)  
- 파라미터 순서: `일반 → *args → 키워드전용 → **kwargs`  
- 언패킹 전달: `func(*list)`, `func(**dict)`  
- 범용 래퍼: `def wrapper(*args, **kwargs): return func(*args, **kwargs)`  
- `functools.wraps`로 원본 함수 메타데이터 보존  
- `*` 만 사용: 이후 파라미터를 키워드 전용으로 강제

---

### `021_keyword_argument.py`
**핵심**: API 설계에서 실수 방지를 위한 키워드 전용 인수  
- `*` 이후 파라미터: 반드시 키워드로 전달 → `create_conn(host, *, timeout=30)`  
- `/` 이전 파라미터: 위치 인수만 허용 (Python 3.8+) → `area(w, h, /)`  
- 완전한 시그니처: `def f(pos_only, /, normal, *, kw_only)`  
- `inspect.signature()`로 파라미터 종류 프로그래밍적 조회  
- `kind`: `POSITIONAL_ONLY`, `POSITIONAL_OR_KEYWORD`, `KEYWORD_ONLY`

---

### `022_namespace.py`
**핵심**: LEGB 규칙 — 이름 조회 순서  
- **L**ocal → **E**nclosing → **G**lobal → **B**uiltins  
- `locals()`, `globals()`, `vars(module)` 로 네임스페이스 딕셔너리 확인  
- `__dict__`: 객체/모듈/클래스의 속성 딕셔너리  
- 전역 수정: `global x` 선언 필수, 없으면 `UnboundLocalError`  
- `nonlocal`: 클로저에서 외부 함수 변수 수정

---

### `023_local_variable.py`
**핵심**: 지역 변수와 `UnboundLocalError` 원인  
- 함수 내 어디서든 `x = ...` 있으면 Python이 `x`를 지역으로 취급  
- **함정**: 같은 함수에서 전역 읽기 전에 할당 → `UnboundLocalError`  
- 스택 프레임: 함수 호출마다 새 로컬 네임스페이스 생성  
- 전역 변수 남용 대안: 클래스, 클로저, 함수 파라미터  
- `locals()`는 현재 스택 프레임의 지역 변수 딕셔너리 (복사본)

---

### `024_global_variable.py`
**핵심**: `global`, `nonlocal` 키워드와 전역 상태 관리  
- `global x`: 함수 내에서 전역 변수 수정 선언  
- `nonlocal x`: 중첩 함수에서 바로 바깥 함수의 변수 수정  
- 전역 변수의 단점: 테스트 어려움, 스레드 안전 문제, 가독성 저하  
- 대안: 모듈 수준 상수(변경 안 함), 클래스로 상태 캡슐화, 파라미터 전달  
- `make_counter()` → `nonlocal`로 상태 유지 클로저

---

### `025_main_function.py`
**핵심**: `__name__ == "__main__"` — 실행 파일과 모듈의 이중 역할  
- 직접 실행: `__name__ == "__main__"`, import 시: `__name__ == 모듈명`  
- `main()` 함수로 진입점 분리 → 단위 테스트 가능  
- `sys.exit(main())` — OS에 종료 코드 전달  
- `argparse`로 CLI 인수 처리  
- **Java 비교**: `public static void main(String[] args)` vs 규칙 기반

---

## PART 02 · Sequence & Collection

> **개념 흐름**: list → tuple → str → set → dict → 내장 함수들  
> **핵심 주제**: 각 자료구조의 특성(가변/불변, 순서/무순서, 해시 가능 여부)  
> **Java 비교**: `ArrayList`, `LinkedList`, `HashSet`, `HashMap` 대응

---

### `026_list.py`
**핵심**: Python 가장 기본 가변 시퀀스  
- 동적 배열 내부 구조: `append` O(1) 분할상환, `insert(0)` O(n)  
- 생성: `[]`, `list()`, `list(range(n))`, `[0]*n`  
- 동종/이종 혼합 가능: `[1, "hello", 3.14, [1,2]]`  
- `id()` 로 리스트 vs 원소 객체 구분  
- **Java**: `ArrayList<Object>` 대응 (제네릭 없음)

---

### `027_list_indexing.py`
**핵심**: 양수/음수 인덱싱과 IndexError  
- `lst[0]` 첫 번째, `lst[-1]` 마지막, `lst[-2]` 끝에서 두 번째  
- `IndexError` vs `list.get(idx, default)` 없음 → try/except 또는 조건 체크  
- `lst[len(lst)//2]` 중간값  
- 2D 리스트: `matrix[row][col]`  
- 안전 인덱싱: `lst[idx] if 0 <= idx < len(lst) else default`

---

### `028_list_slicing.py`
**핵심**: 슬라이싱 = 새 리스트 반환 (얕은 복사)  
- `lst[start:stop:step]` — 셋 다 생략 가능  
- `lst[:]` 전체 복사, `lst[::-1]` 역순  
- 슬라이스 할당: `lst[1:3] = [10, 20, 30]` (길이 변경 가능)  
- `del lst[2:5]` 구간 삭제  
- `slice` 객체: `s = slice(1, 5, 2)` → `lst[s]`

---

### `029_list_method.py`
**핵심**: 자주 쓰는 리스트 메서드 전체  
- 추가: `append(x)`, `extend(iter)`, `insert(i, x)`  
- 제거: `remove(x)` (값 기준, 첫 번째), `pop(i=-1)`, `del lst[i]`, `clear()`  
- 검색: `index(x)`, `count(x)` — O(n)  
- 정렬: `sort()` (in-place), `sorted()` (새 리스트) — **key 파라미터**  
- 기타: `reverse()`, `copy()`, `list.copy()` vs `[:]`

---

### `030_tuple.py`
**핵심**: 불변 시퀀스 — 언제 list 대신 tuple을 쓰는가  
- 불변이므로 딕셔너리 키, set 원소로 사용 가능  
- 단일 원소: `(42,)` — 쉼표 필수, `(42)` 는 그냥 int  
- 생성: `()`, `tuple()`, `(1,)`, `1, 2, 3` (괄호 없이도 튜플)  
- 성능: 생성/순회 속도 list보다 빠름 (불변이라 최적화 가능)  
- 용도: 함수 다중 반환값, 레코드, 딕셔너리 키, 설정값

---

### `031_tuple_packing.py`
**핵심**: 튜플 패킹 — 여러 값을 자동으로 튜플로 묶음  
- `t = 1, 2, 3` ← 괄호 없어도 튜플  
- 함수 반환: `return x, y` → 자동 패킹 → `a, b = func()` 언패킹  
- 패킹된 값의 순회, 인덱싱  
- `*args`에서 위치 인수 패킹  
- 네임드 튜플 예고 (PART 15)

---

### `032_tuple_unpacking.py`
**핵심**: 튜플 언패킹 — Python 핵심 문법 중 하나  
- `a, b = (1, 2)`, `a, b, c = [10, 20, 30]`  
- 스왑: `a, b = b, a` (임시 변수 불필요)  
- `*rest`: `first, *rest = [1, 2, 3, 4]` → `first=1, rest=[2,3,4]`  
- `_`: 무시할 값 관례 표현 `_, important, _ = triple`  
- 중첩 언패킹: `(a, b), c = (1, 2), 3`

---

### `033_string.py`
**핵심**: `str`을 시퀀스로 다루기  
- `str`은 문자(길이 1인 str)의 불변 시퀀스  
- 인덱싱, 슬라이싱, `in` 연산자 모두 사용 가능  
- `for char in "hello":` 문자 순회  
- `str.join(iterable)` / `str.split(sep)` 핵심 쌍  
- 멀티라인, raw, f-string, bytes 비교

---

### `034_string_slicing.py`
**핵심**: 문자열 슬라이싱 패턴  
- `s[1:4]`, `s[::2]`, `s[::-1]` (문자열 역순)  
- 접두사/접미사 제거: `s[2:]`, `s[:-3]`  
- 고정 길이 필드 파싱: `line[0:10].strip()`, `line[10:20].strip()`  
- 문자열은 불변 → 슬라이싱은 항상 새 str 반환  
- `textwrap.wrap()`, `textwrap.dedent()` 실무 활용

---

### `035_string_method.py`
**핵심**: 자주 쓰는 str 메서드 총망라  
- 변환: `upper()`, `lower()`, `title()`, `swapcase()`  
- 검색: `find()`, `index()`, `count()`, `startswith()`, `endswith()`  
- 정리: `strip()`, `lstrip()`, `rstrip()`, `replace()`  
- 분리/결합: `split()`, `rsplit()`, `splitlines()`, `join()`  
- 판별: `isdigit()`, `isalpha()`, `isalnum()`, `isspace()`  
- 포맷: `zfill()`, `center()`, `ljust()`, `rjust()`

---

### `036_set.py`
**핵심**: 해시 기반 중복 없는 집합 — O(1) 검색  
- 생성: `{1, 2, 3}`, `set()`, `set(iterable)` — `{}` 는 빈 dict!  
- 집합 연산: `|` 합집합, `&` 교집합, `-` 차집합, `^` 대칭차  
- `in` 연산: O(1) — 리스트의 O(n)과 비교  
- 중복 제거: `list(set(lst))` (순서 보장 안 됨, `dict.fromkeys()` 대안)  
- 원소는 반드시 hashable (리스트 불가, 튜플 가능)

---

### `037_frozenset.py`
**핵심**: 불변 집합 — 딕셔너리 키, 중첩 집합 가능  
- `frozenset({1, 2, 3})` — 생성 후 변경 불가  
- 딕셔너리 키: `{frozenset({1,2}): "value"}`  
- `set`의 원소: `{frozenset({1,2}), frozenset({3,4})}`  
- 메서드: 변경 메서드(`add`, `remove`) 없음, 집합 연산은 동일  
- 권한 그룹, 태그 집합 등 불변 집합이 필요한 경우

---

### `038_dict.py`
**핵심**: Python 3.7+ 딕셔너리는 삽입 순서 보장  
- 생성: `{}`, `dict()`, `dict(a=1, b=2)`, `{k:v for k,v in pairs}`  
- 접근: `d[key]` (KeyError 가능), `d.get(key, default)` (안전)  
- 수정: `d[key] = value`, `d.update(other)`, `d |= other` (3.9+)  
- 내부: 해시 테이블 → 평균 O(1) 조회, 충돌 시 O(n)  
- **Java**: `LinkedHashMap` (순서 보장) 대응

---

### `039_dict_method.py`
**핵심**: 딕셔너리 메서드 완전 정복  
- `keys()`, `values()`, `items()` → 뷰(view) 객체 반환  
- `get(k, default)`, `setdefault(k, default)`, `pop(k, default)`  
- `update(other)`: 덮어쓰기 병합  
- `copy()` 얕은 복사, `dict(**d1, **d2)` 병합 (3.5+)  
- `fromkeys(iterable, value)`: 키 목록으로 딕셔너리 생성

---

### `040_dict_view.py`
**핵심**: `keys()`, `values()`, `items()` 는 뷰 — 실시간 반영  
- 뷰는 딕셔너리 변경을 실시간 반영 (리스트 복사 아님)  
- `list(d.keys())` → 실제 리스트로 변환  
- 뷰를 이용한 키 존재 확인: `key in d.keys()` vs `key in d` (동일)  
- `d.items()` → `(key, value)` 튜플 쌍 언패킹  
- 뷰 간 집합 연산: `d1.keys() & d2.keys()` (공통 키)

---

### `041_dict_comprehension.py`
**핵심**: 딕셔너리 컴프리헨션  
- `{k: v for k, v in items}` 기본 형식  
- 조건 필터: `{k: v for k, v in d.items() if v > 0}`  
- 키/값 변환: `{k.upper(): v*2 for k, v in d.items()}`  
- `zip`과 결합: `{k: v for k, v in zip(keys, values)}`  
- 역방향 딕셔너리: `{v: k for k, v in d.items()}`

---

### `042_enumerate.py`
**핵심**: 인덱스 + 값을 동시에 — `range(len())` 대체  
- `for i, item in enumerate(iterable, start=0):`  
- `start` 파라미터로 시작 번호 조정  
- `enumerate` 반환값은 `(index, value)` 튜플 이터레이터  
- **Java 비교**: 인덱스용 `for(int i=0; ...)` 불필요  
- 번호 매기기, 진행도 표시, 조건부 인덱스 사용

---

### `043_zip.py`
**핵심**: 여러 이터러블을 병렬 순회  
- `zip(a, b)` → `(a[0],b[0])`, `(a[1],b[1])`, ... 이터레이터  
- 길이가 다르면 **짧은 쪽** 기준으로 종료  
- `dict(zip(keys, values))` → 딕셔너리 생성  
- `zip(*matrix)` → 행렬 전치  
- 3개 이상: `zip(a, b, c)` / `zip_longest` 비교

---

### `044_sorted.py`
**핵심**: `sorted()` vs `.sort()` — 새 리스트 vs in-place  
- `sorted(iterable, key=None, reverse=False)` → 새 리스트  
- `.sort()` → in-place, `None` 반환  
- `key` 함수: `key=len`, `key=str.lower`, `key=lambda x: x[1]`  
- 안정 정렬(stable sort) — 같은 키는 원래 순서 유지  
- 복잡한 정렬: `key=lambda x: (x.grade, -x.score)`

---

### `045_max.py` · `046_min.py`
**핵심**: `max()`, `min()` — `key` 파라미터 활용  
- `max(iterable)`, `max(a, b, c)` 두 가지 호출 방식  
- `key=len` → 가장 긴 문자열, `key=lambda x: x["score"]` → 최고점  
- `max(iterable, default=value)` → 빈 이터러블 처리  
- `min/max` + 딕셔너리: `max(d, key=d.get)` → 가장 큰 값의 키  
- `heapq.nlargest(n, iterable, key=)` → 상위 n개

---

### `047_sum.py`
**핵심**: `sum()` 과 누적 패턴  
- `sum(iterable, start=0)` — start로 초기값 지정  
- `sum([[1,2],[3,4]], [])` → `[1,2,3,4]` 리스트 평탄화 (소규모만)  
- 제너레이터 표현식과 결합: `sum(x**2 for x in range(10))`  
- `math.fsum()` → 부동소수점 정확 합계  
- `functools.reduce(operator.add, lst)` 일반화

---

### `048_any.py` · `049_all.py`
**핵심**: `any()`, `all()` — 단락 평가 이터러블 검사  
- `any(iterable)`: 하나라도 Truthy → True, 빈 이터러블 → False  
- `all(iterable)`: 모두 Truthy → True, 빈 이터러블 → True  
- 제너레이터 표현식과 결합: `all(x > 0 for x in nums)`  
- **단락 평가**: 조건 확정 즉시 나머지 평가 중단 → 효율적  
- 권한 체크: `all(perm in user_perms for perm in required)`

---

### `050_reversed.py`
**핵심**: `reversed()` — 역순 이터레이터  
- `reversed(sequence)` → 이터레이터 반환 (새 리스트 안 만듦)  
- 시퀀스만 가능 (`__reversed__` 또는 `__len__` + `__getitem__` 필요)  
- `lst[::-1]` vs `reversed(lst)`: 전자는 새 리스트, 후자는 이터레이터  
- 사용자 정의 클래스에 `__reversed__` 구현  
- `deque` 역순 순회

---

## PART 03 · Collection Mastery

> **개념 흐름**: 튜플/리스트 비교 → 패킹/언패킹 심화 → 중첩 구조 → enumerate/zip 고급 → 정렬 마스터  
> **실무 패턴 30개 이상** 수록  
> **핵심**: "어떤 자료구조를 언제 쓰는가"

---

### `051_tuple_vs_list.py`
**핵심**: 튜플과 리스트의 선택 기준  
- 불변 필요 → tuple (딕셔너리 키, set 원소, 반환값 레코드)  
- 가변 필요 → list (추가/삭제, 정렬 필요 시)  
- 성능: 튜플 생성, 언패킹이 리스트보다 빠름  
- 명시적 의도: 고정 레코드=tuple, 동적 컬렉션=list  
- `sys.getsizeof`: 같은 원소 개수에서 튜플 < 리스트 메모리

---

### `052_packing.py`
**핵심**: 묵시적 튜플 패킹 완전 이해  
- `t = 1, 2, 3` → `(1, 2, 3)` 괄호 없이도 튜플  
- 함수 반환 `return a, b` → 자동 패킹  
- `for` 루프: `for pair in [(1,"a"),(2,"b")]:`  
- 딕셔너리 `items()`: 각 쌍이 튜플로 패킹  
- 패킹 vs 컨테이너 생성 구분

---

### `053_unpacking.py`
**핵심**: 언패킹의 모든 형태  
- 기본: `a, b = (1, 2)`  
- `*rest` 확장 언패킹: `first, *rest = [1,2,3,4]`, `*init, last = lst`  
- 중첩: `(a, b), c = (1, 2), 3`  
- 함수 호출 시: `func(*args)`, `func(**kwargs)`  
- 리스트 컴프리헨션에서: `[a+b for a, b in pairs]`

---

### `054_nested_tuple.py`
**핵심**: 중첩 튜플 — 트리 구조, 레코드 표현  
- `((1,2),(3,4))`, `(("Alice",30,("Seoul","Korea")),)`  
- 재귀 언패킹: `name, age, (city, country) = record`  
- 딕셔너리 키로 중첩 튜플: `{(0,0): "origin", (1,0): "x"}`  
- 좌표계, 그래프 엣지 표현: `(from_node, to_node, weight)`  
- 정렬: `sorted(points, key=lambda p: p[0]**2 + p[1]**2)`

---

### `055_nested_list.py`
**핵심**: 중첩 리스트 — 행렬, 2D 배열  
- 2D 행렬: `[[0]*cols for _ in range(rows)]` ← `[[0]*cols]*rows` 함정!  
- 행/열 접근, 서브행렬 슬라이싱  
- 평탄화: `[x for row in matrix for x in row]`, `itertools.chain.from_iterable`  
- 전치: `list(zip(*matrix))`  
- **함정**: `[[0]*3]*3` 모든 행이 같은 객체 공유

---

### `056_list_of_tuple.py`
**핵심**: `[(key, value), ...]` — DB 결과, CSV 행 패턴  
- `[(id, name, score), ...]` DB 쿼리 결과 표현  
- `sorted(records, key=lambda r: r[2], reverse=True)` 정렬  
- `dict([(k,v) for k,v in items])` 딕셔너리 변환  
- `operator.itemgetter(1)` — lambda보다 빠른 키 함수  
- 네임드 튜플로 업그레이드 (PART 15 연결)

---

### `057_tuple_of_list.py`
**핵심**: `([...], [...], ...)` — 병렬 배열, 언집 패턴  
- `(ids, names, scores)` — 열 기반 데이터 표현  
- 언집(unzip): `ids, names = zip(*[(1,"A"),(2,"B")])` 분리  
- 컬럼 처리: 특정 열만 추출  
- NumPy 열 기반 배열과의 연결  
- 가변 내부(list), 불변 외부(tuple) 의도 표현

---

### `058_dict_of_list.py`
**핵심**: `{key: [val1, val2, ...]}` — 그룹핑 패턴  
- 수동 그룹핑, `defaultdict(list)` 자동 그룹핑  
- `setdefault(key, []).append(val)` 패턴  
- `itertools.groupby` 연결  
- 역 인덱스(inverted index) 구현  
- 그래프 인접 리스트: `{node: [neighbors]}`

---

### `059_list_of_dict.py`
**핵심**: `[{}, {}, ...]` — JSON 배열, ORM 결과 패턴  
- `[{"id": 1, "name": "Alice"}, ...]` REST API 응답 표현  
- 정렬: `sorted(users, key=lambda u: u["age"])`  
- 필터: `[u for u in users if u["active"]]`  
- 그룹핑: `defaultdict(list)`로 특정 키 기준 분류  
- `operator.itemgetter("name")` 성능 최적화

---

### `060_unpacking_in_loop.py`
**핵심**: 루프에서의 언패킹 — Pythonic 코드의 핵심  
- `for key, value in d.items():` 딕셔너리 순회  
- `for i, (name, score) in enumerate(pairs):` 중첩 언패킹  
- `for (x1,y1), (x2,y2) in zip(points_a, points_b):`  
- `for first, *rest in [[1,2,3],[4,5,6]]:` 확장 언패킹  
- 반환값 즉시 언패킹: `min_val, max_val = min_max(data)`

---

### `061_multiple_assignment.py`
**핵심**: 다중 할당의 모든 패턴  
- `a = b = c = 0` 연쇄 할당 (같은 객체 참조 주의)  
- `a, b = b, a` 스왑 (오른쪽 먼저 평가)  
- 증강 할당 `+=`, `-=`, `*=`, `//=`, `**=`, `%=`  
- `a, *b, c = range(10)` → 확장 다중 할당  
- **함정**: `a = b = []` → 같은 리스트 공유

---

### `062_starred_expression.py`
**핵심**: `*` 확장 표현식 — Python 3.5+  
- 언패킹: `first, *middle, last = iterable`  
- 리스트 병합: `[*list1, *list2, *list3]`  
- 딕셔너리 병합: `{**d1, **d2}` (우측이 우선)  
- 함수 호출: `func(*args, **kwargs)` 전달  
- 제너레이터 소비: `[*generator]`

---

### `063_enumerate_advanced.py`
**핵심**: `enumerate` 고급 패턴  
- `start` 파라미터: 1부터 시작 `enumerate(items, 1)`  
- 역방향: `enumerate(reversed(items))`  
- 필터 후 enumerate: `enumerate(x for x in items if cond)`  
- 인덱스 기반 수정 (컴프리헨션 vs 직접 수정)  
- `tqdm(enumerate(items))` 프로그레스 바 패턴

---

### `064_zip_advanced.py`
**핵심**: `zip` 고급 조합 패턴  
- `dict(zip(keys, values))` 딕셔너리 생성  
- 행렬 전치: `list(zip(*matrix))`  
- 슬라이딩 윈도우: `zip(lst, lst[1:])` 인접 쌍  
- 3개 이상 zip: `zip(a, b, c)`  
- `zip` 이터레이터는 소진(exhausted) 주의

---

### `065_zip_longest.py`
**핵심**: `itertools.zip_longest` — 긴 쪽 기준  
- `zip_longest(a, b, fillvalue=None)` 짧은 쪽 채움  
- 긴 zip vs 짧은 zip 선택 기준  
- 데이터 정렬 맞추기: 누락 데이터 `None`으로 표시  
- 병렬 다운로드 결과 합치기 패턴  
- `zip_longest` + `defaultdict` 조합

---

### `066_sorted.py` (심화)
**핵심**: `sorted` 내부 — Timsort 알고리즘  
- Timsort: 안정 정렬, O(n log n), 실제 데이터에 최적화  
- `key` 함수는 각 원소당 1회만 호출 (Schwartzian transform)  
- `(primary_key, secondary_key)` 튜플로 다중 정렬  
- `functools.cmp_to_key` — 구식 비교 함수 변환  
- CPython `list.sort()` vs `sorted()` 내부 차이

---

### `067_key_function.py`
**핵심**: `key` 함수 패턴 모음  
- `key=str.lower` 대소문자 무시 정렬  
- `key=len` 길이 기준  
- `key=operator.itemgetter(n)` 리스트/튜플 n번째 원소  
- `key=operator.attrgetter("attr")` 객체 속성  
- 복합: `key=lambda x: (x.priority, -x.timestamp)`

---

### `068_lambda_sort.py`
**핵심**: lambda와 정렬의 조합  
- `sorted(items, key=lambda x: x["score"])`  
- lambda는 단일 표현식만 가능, 복잡하면 함수로  
- `lambda x: (x.type, -x.value)` 다중 키  
- **실무 조언**: lambda보다 `operator.itemgetter`, `attrgetter` 가 더 빠름  
- `key=None` 시 기본 비교 (`__lt__`) 사용

---

### `069_custom_sort.py`
**핵심**: 커스텀 정렬 완전 정복  
- `@total_ordering` + `__lt__`, `__eq__` 구현  
- `functools.cmp_to_key`로 3방향 비교 함수 변환  
- 한글/멀티바이트 정렬: `locale.strxfrm`, `natsort`  
- 위상 정렬 예고 (의존성 순서)  
- 안정 정렬 활용: 1차 정렬 후 2차 정렬

---

### `070_practical_collection_exercises.py`
**핵심**: 실무 컬렉션 패턴 30개 종합  
- 빈도 카운팅, Top-N 추출, 그룹핑  
- 조인(두 리스트를 키로 병합), 중복 제거 (순서 보존)  
- 슬라이딩 윈도우, 청크 분할, 페이지네이션  
- 딕셔너리 역전, 중첩 병합, 깊은 get  
- 미니 프로젝트: 성적 처리 시스템

---

## PART 04 · Comprehension & Functional

> **개념 흐름**: list comprehension → dict/set → generator expression → lambda → map/filter/reduce  
> **핵심**: Pythonic 한 줄 표현의 원리와 한계  
> **Java 비교**: Stream API(`.filter().map().collect()`) 대응

---

### `071_list_comprehension.py`
**핵심**: `[expression for item in iterable if condition]`  
- 3부분: 표현식 / 순회 / 조건(선택)  
- 중첩: `[x for row in matrix for x in row]` 평탄화  
- 조건부 표현식: `[f(x) if cond else g(x) for x in lst]`  
- **성능**: 동등 for 루프보다 빠름 (최적화된 바이트코드)  
- **함정**: 복잡한 컴프리헨션은 가독성 ↓ → 함수 분리

---

### `072_dict_comprehension.py`
**핵심**: `{k: v for k, v in iterable if condition}`  
- `zip` + dict 컴프리헨션: `{k: v for k, v in zip(keys, vals)}`  
- 역방향 딕셔너리: `{v: k for k, v in d.items()}`  
- 필터링: `{k: v for k, v in d.items() if v is not None}`  
- 변환: `{k.lower(): str(v) for k, v in d.items()}`  
- 중첩: `{outer: {inner: val} for outer, inner, val in triples}`

---

### `073_set_comprehension.py`
**핵심**: `{expression for item in iterable if condition}`  
- `{}` 는 빈 dict, `set()` 이 빈 set  
- 중복 자동 제거: `{x % 3 for x in range(10)}`  
- 합집합/교집합 후 조건 필터  
- frozenset 컴프리헨션: `frozenset(x for x in ...)`  
- 고유 값 추출: `{row["category"] for row in data}`

---

### `074_generator_expression.py`
**핵심**: `(expression for item in iterable)` — 게으른 평가  
- 리스트 컴프리헨션 `[]` vs 제너레이터 `()` 메모리 비교  
- `sum(x**2 for x in range(10**6))` — 리스트 생성 없이 합계  
- `next(x for x in items if condition)` — 첫 번째 일치 즉시 반환  
- 파이프라이닝: `sum(len(s) for s in (s.strip() for s in lines))`  
- 제너레이터는 한 번만 순회 가능 (소진 주의)

---

### `075_lambda.py`
**핵심**: 익명 함수 — 단일 표현식만 가능  
- `lambda 파라미터: 표현식` — return 없음  
- `sorted(items, key=lambda x: x[1])`  
- `map(lambda x: x*2, lst)`, `filter(lambda x: x>0, lst)`  
- **한계**: 문(statement) 불가, 여러 줄 불가  
- **실무 조언**: 재사용 시 def, 한 번만 쓸 때 lambda

---

### `076_map.py`
**핵심**: `map(func, iterable)` — 변환 이터레이터  
- `list(map(int, ["1","2","3"]))` 타입 변환  
- `map(str.upper, words)` 메서드 전달  
- `map(func, a, b)` 두 이터러블 병렬 처리  
- 리스트 컴프리헨션 vs map: `[f(x) for x in lst]` 대부분 가독성 우위  
- 게으른 평가: `list()` 로 강제 소비해야 결과 확인

---

### `077_filter.py`
**핵심**: `filter(func, iterable)` — 조건 필터 이터레이터  
- `list(filter(None, lst))` → Falsy 제거  
- `filter(str.isdigit, chars)` 메서드 전달  
- 리스트 컴프리헨션: `[x for x in lst if pred(x)]` 비교  
- `filter` + `map` 체이닝: 파이프라인  
- `itertools.filterfalse` — 조건 반전

---

### `078_reduce.py`
**핵심**: `functools.reduce(func, iterable, initial)` — 누적 연산  
- `reduce(operator.add, [1,2,3,4])` → 10  
- `reduce(lambda acc, x: acc + x, lst, 0)` 초기값  
- 팩토리얼: `reduce(operator.mul, range(1, n+1))`  
- 딕셔너리 병합: `reduce(lambda d1, d2: {**d1, **d2}, dicts)`  
- **Python 철학**: 명시적 루프나 `sum/max/min`이 더 Pythonic한 경우 많음

---

### `079_sorted_key.py`
**핵심**: key 함수 심화 — Schwartzian Transform  
- 내부: `(key(x), x)` 쌍으로 만들어 비교 → 결과 추출  
- `key` 함수는 원소당 1회만 호출 → 비용 큰 계산에 효율적  
- `operator.itemgetter` vs `lambda`: 성능과 가독성  
- 다단계 정렬: `key=attrgetter("dept", "name")`  
- 정렬 안정성: 같은 key는 원래 순서 유지

---

### `080_custom_sort.py`
**핵심**: 복잡한 비즈니스 정렬 로직 구현  
- 도메인 특화 정렬: 상태 우선순위, 날짜 기준  
- 정렬 불가 타입 혼합: `key=lambda x: (type(x).__name__, x)`  
- 부분 정렬: `heapq.nsmallest(n, iterable, key=)`  
- 사전순 vs 자연어 정렬: `"file9" < "file10"` 문제  
- PART 03 종합 미니 프로젝트: 학점 계산기

---

## PART 05 · Object & Memory

> **개념 흐름**: 객체 → 가변/불변 → id/is → 복사 → GC  
> **핵심**: Python 메모리 모델 이해 → 모든 버그의 근원  
> **Java 비교**: JVM 참조 모델과 유사하나 차이점 존재

---

### `081_object_concept.py`
**핵심**: Python에서 모든 것은 객체  
- 정수, 함수, 클래스, 모듈 모두 `object`의 인스턴스  
- 객체 3요소: **정체성**(id), **타입**(type), **값**(value)  
- `id()` = CPython에서 메모리 주소  
- `object.__repr__`, `object.__str__` 기반  
- 모든 객체에 공통: `__class__`, `__doc__`, `__hash__`

---

### `082_mutable.py`
**핵심**: 가변(mutable) 객체 — `list`, `dict`, `set`, 사용자 클래스  
- 가변 객체 수정 시 **같은 id 유지**  
- 같은 객체를 두 이름이 참조 → 한쪽 수정 → 양쪽 반영  
- 함수 인자: 가변 객체 전달 = 참조 전달 (Java와 동일)  
- `append` vs `+= [x]` vs `= lst + [x]` 차이  
- **실무 함정**: 함수 내 리스트 수정이 외부에 반영되는 케이스

---

### `083_immutable.py`
**핵심**: 불변(immutable) 객체 — `int`, `str`, `tuple`, `frozenset`, `bytes`  
- 불변 객체 "수정" = 사실 새 객체 생성  
- `s = s.upper()` → 새 str 객체, 원본 `s`가 가리키던 것은 참조 해제  
- 불변이라서 가능한 것: 딕셔너리 키, set 원소, 캐싱, 멀티스레드 안전  
- `str`의 `+=` 연산: 반복 시 O(n²) → `join` 사용  
- `tuple` vs `frozenset` 불변 컨테이너 비교

---

### `084_id.py`
**핵심**: `id()` 함수 — 객체 정체성  
- CPython: `id(x)` = 메모리 주소 (다른 구현체는 다를 수 있음)  
- 소형 정수(-5~256), 짧은 문자열 intern → 같은 id  
- `is` 연산자 = `id(a) == id(b)` 와 동일  
- 델리케이트: `id` 재사용 가능 (가비지 수집 후)  
- `ctypes`로 id를 주소로 역참조 (CPython 내부 학습용)

---

### `085_hex.py`
**핵심**: `hex()`, 메모리 주소 표현  
- `hex(id(obj))` → 메모리 주소 16진수 표현  
- `hex(255)` → `'0xff'`, `format(255, '#010x')` 패딩  
- `bytes.hex()` → 바이트 배열을 16진수 문자열로  
- `int.from_bytes`, `int.to_bytes` — 바이트 직렬화  
- 해시값: `hex(hash(obj))` — `__hash__` 이해

---

### `086_shallow_copy.py`
**핵심**: 얕은 복사 — 외부 컨테이너만 복사, 원소는 공유  
- `lst[:]`, `list(lst)`, `lst.copy()`, `copy.copy(obj)`  
- 외부 리스트는 다른 객체, 내부 원소는 같은 객체  
- 중첩 구조에서 함정: `copy.copy([[1,2],[3,4]])` → 내부 리스트 공유  
- `dict.copy()` 얕은 복사  
- 언제 얕은 복사로 충분한가 vs 깊은 복사가 필요한가

---

### `087_deep_copy.py`
**핵심**: 깊은 복사 — 재귀적으로 모든 중첩 객체 복사  
- `copy.deepcopy(obj)` — 완전 독립 복사  
- 순환 참조 처리: `deepcopy`는 내부적으로 메모ID 기록  
- **성능 주의**: 복잡한 객체 그래프에서 느림  
- `__copy__`, `__deepcopy__` 커스터마이즈  
- JSON 직렬화/역직렬화를 이용한 딥 카피 (단순 데이터)

---

### `088_gc.py`
**핵심**: Python 가비지 컬렉터  
- 1차: 참조 카운팅 (ref count = 0 → 즉시 해제)  
- 2차: 세대별 GC (순환 참조 처리) — `gc` 모듈  
- `gc.collect()` 강제 실행, `gc.get_count()` 세대 카운터  
- 순환 참조 예시: `a.ref = b; b.ref = a` → ref count 0 안 됨  
- `__del__` — 소멸자, 언제 호출될지 보장 없음

---

### `089_del.py`
**핵심**: `del` — 이름 바인딩 해제 (객체 삭제가 아님)  
- `del x` → 이름 `x`와 객체의 바인딩 해제 (ref count -1)  
- ref count → 0이 될 때 비로소 객체 메모리 해제  
- `del lst[2]`, `del lst[1:4]`, `del d["key"]`  
- `__del__` 소멸자 vs `del` 문 혼동 금지  
- 컨텍스트 매니저(`with`)가 더 안전한 자원 해제

---

### `090_weakref.py`
**핵심**: 약한 참조 — 참조 카운트에 영향 안 주는 참조  
- `import weakref; ref = weakref.ref(obj)`  
- 캐시 구현: `WeakValueDictionary` — 값 GC 허용  
- 순환 참조 회피: 부모↔자식 관계에서 자식이 부모를 weakref로  
- `ref()` 호출 시 객체가 GC되었으면 `None` 반환  
- 이벤트 리스너, 옵저버 패턴에서 활용

---

## PART 06 · Function Advanced

> **개념 흐름**: 1급 객체 → 클로저 → 데코레이터 → partial/cache  
> **핵심**: 데코레이터는 고급 기능이 아닌 Python의 핵심 패턴  
> **Java 비교**: AOP(관점지향 프로그래밍)과 유사

---

### `091_first_class_function.py`
**핵심**: 함수를 값처럼 다루기  
- 함수 타입: `type(func)` → `<class 'function'>`  
- `func.__name__`, `func.__doc__`, `func.__code__`  
- 고차 함수: 함수를 받아 함수를 반환  
- 함수 리스트: `[abs, str, type]` 순회 실행  
- **Java**: 메서드 참조 `String::toUpperCase` 대응

---

### `092_closure.py`
**핵심**: 클로저 — 자유 변수를 캡처한 함수  
- 내부 함수가 외부 함수의 변수를 참조 → 외부 함수 종료 후도 유지  
- `func.__closure__` → 캡처된 셀(cell) 객체  
- `nonlocal`로 캡처 변수 수정  
- 카운터, 누적기, 설정 팩토리 패턴  
- **함정**: 루프 변수 캡처 → `lambda x=x: x` 패턴

---

### `093_nested_function.py`
**핵심**: 중첩 함수 — 헬퍼 함수 캡슐화  
- 내부 함수는 외부에서 접근 불가 (private 헬퍼)  
- LEGB 스코프에서 E(Enclosing) 이해  
- 팩토리 패턴: 내부 함수를 반환  
- 재귀 함수의 내부 헬퍼 분리  
- 테일 재귀 최적화 없음 (CPython) → 반복문 대체

---

### `094_decorator_basic.py`
**핵심**: 데코레이터 — 함수를 감싸는 함수  
- `@decorator` = `func = decorator(func)` 문법 설탕  
- 기본 구조: `wrapper(*args, **kwargs)` + `@functools.wraps(func)`  
- 로깅, 타이밍, 캐싱, 인증 패턴  
- `func.__wrapped__` 원본 함수 접근  
- **Java**: Spring AOP `@Around` 어드바이스 대응

---

### `095_decorator_argument.py`
**핵심**: 인수를 받는 데코레이터 — 3중 중첩 함수  
- `@retry(max=3)` → `retry(max=3)(func)(args)` 호출 순서  
- 데코레이터 팩토리 패턴  
- `@app.route("/path")` Flask/FastAPI 스타일  
- 클래스 기반 데코레이터: `__call__` 메서드  
- 선택적 인수: `@decorator` 또는 `@decorator()` 모두 지원

---

### `096_decorator_chaining.py`
**핵심**: 데코레이터 체이닝 — 적용 순서  
- `@d1 @d2 def f:` → `d1(d2(f))` 내부에서 바깥으로 적용  
- `@wraps` 없으면 체이닝 시 메타데이터 소실  
- 순서 중요: `@login_required @cache` vs `@cache @login_required`  
- 데코레이터 스택 디버깅: `func.__wrapped__` 체이닝  
- `inspect.unwrap(func)` 모든 래퍼 벗기기

---

### `097_partial.py`
**핵심**: `functools.partial` — 부분 적용 함수  
- `partial(func, *args, **kwargs)` → 일부 인수 고정 함수  
- `double = partial(multiply, b=2)` → `double(5) == 10`  
- `map(partial(pow, exp=2), nums)` 실무 패턴  
- 메서드를 일반 함수로: `partial(str.split, sep=",")`  
- **Java**: 커링(currying)과 유사

---

### `098_lru_cache.py`
**핵심**: `@functools.lru_cache` — 메모이제이션  
- `@lru_cache(maxsize=128)` 최근 128개 결과 캐시  
- `@cache` (Python 3.9+): 무제한 캐시 (= `maxsize=None`)  
- 피보나치: `O(2^n)` → `O(n)` (劇적 성능 개선)  
- **조건**: 인수가 hashable해야 함 (리스트 불가)  
- `cache_info()`, `cache_clear()` 캐시 관리

---

## PART 07 · OOP

> **개념 흐름**: 클래스 → 인스턴스 → 생성자 → 변수 → 메서드 → 상속 → MRO  
> **핵심**: Java OOP와 유사하나 `self`, `cls`, MRO 차이 이해  
> **파일**: 099 ~ 114

### 주요 파일 핵심 요약

| 파일 | 핵심 포인트 |
|------|------------|
| `099_class.py` | `class 이름(부모):` — 암묵적 `object` 상속 |
| `100_instance.py` | `obj = Class()` → `__new__` + `__init__` 호출 순서 |
| `101_constructor.py` | `__init__(self, ...)` — Java의 생성자 대응, `__new__` 분리 이해 |
| `102_self.py` | `self` = 인스턴스 자기 참조 — Java의 `this`, 생략 불가 |
| `103_class_variable.py` | 클래스 변수 공유 함정 — 수정 시 인스턴스 변수 생성 |
| `104_instance_variable.py` | `self.x` — `__init__`에서 초기화, `__dict__`에 저장 |
| `105_classmethod.py` | `@classmethod` → `cls` 첫 파라미터 — 팩토리 메서드 패턴 |
| `106_staticmethod.py` | `@staticmethod` → `self/cls` 없음 — 유틸리티 메서드 |
| `107_inheritance.py` | `class Child(Parent):` — `super().__init__()` 호출 필수 |
| `108_overriding.py` | 메서드 오버라이딩 — `super().method()` 부모 호출 |
| `109_super.py` | `super()` 내부 — MRO 순서대로 다음 클래스 탐색 |
| `110_isinstance.py` | `isinstance(obj, cls)` — 상속 체계 고려한 타입 체크 |
| `111_issubclass.py` | `issubclass(Child, Parent)` — 클래스 간 상속 관계 확인 |
| `112_abstract_class.py` | `abc.ABC`, `@abstractmethod` — Java `interface/abstract` 대응 |
| `113_multiple_inheritance.py` | `class D(B, C):` — 다중 상속, 다이아몬드 문제 |
| `114_MRO.py` | C3 선형화 알고리즘 — `__mro__`, `mro()` 메서드 |

---

## PART 08 · Encapsulation

> **개념 흐름**: 접근제어 → property → `__dict__`/`__slots__` → 디스크립터

| 파일 | 핵심 포인트 |
|------|------------|
| `115_private.py` | `__name` 네임 맹글링 → `_ClassName__name` 변환 |
| `116_protected.py` | `_name` 컨벤션 — Python은 강제 없음 (honor system) |
| `117_property.py` | `property(fget, fset, fdel)` — getter/setter 패턴 |
| `118_property_decorator.py` | `@property`, `@x.setter`, `@x.deleter` 데코레이터 체인 |
| `119_dict.py` | `__dict__` — 인스턴스 속성 딕셔너리, 동적 속성 추가 |
| `120_slots.py` | `__slots__` — 속성 고정, `__dict__` 미생성, 메모리 절약 |
| `121_descriptor.py` | 디스크립터 프로토콜: `__get__`, `__set__`, `__delete__` |
| `122_descriptor_advanced.py` | 데이터/비데이터 디스크립터, property 재구현 |

---

## PART 09 · Special Methods

> **개념 흐름**: 문자열 표현 → 길이/이터레이션 → 컨테이너 → 컨텍스트 → 산술  
> **핵심**: Python 데이터 모델 — 특수 메서드가 언어 자체와 통합되는 방식

| 파일 | 핵심 포인트 |
|------|------------|
| `123___str__.py` | `__str__` — `str(obj)`, `print(obj)` 시 호출 |
| `124___repr__.py` | `__repr__` — `repr(obj)`, 대화형 셸, 디버깅용 |
| `125___len__.py` | `__len__` — `len(obj)`, bool 평가에도 사용 |
| `126___iter__.py` | `__iter__` — `iter(obj)`, `for` 루프 지원 |
| `127___next__.py` | `__next__` — `next(it)`, `StopIteration` 시 루프 종료 |
| `128___call__.py` | `__call__` — `obj()` 함수처럼 호출 가능 객체 |
| `129___getitem__.py` | `__getitem__` — `obj[key]`, 슬라이싱 지원 |
| `130___setitem__.py` | `__setitem__` — `obj[key] = value` |
| `131___contains__.py` | `__contains__` — `x in obj` 연산자 |
| `132___enter__.py` | `__enter__` — `with` 문 진입 시 |
| `133___exit__.py` | `__exit__(exc_type, exc_val, tb)` — 예외 처리 포함 |
| `134___add__.py` | `__add__`, `__radd__` — `+` 연산자, 반사 메서드 |
| `135___sub__.py` | `__sub__` — `-` 연산자 |
| `136___mul__.py` | `__mul__`, `__rmul__` — `*` 연산자 |
| `137___iadd__.py` | `__iadd__` — `+=` 인플레이스 (list는 같은 객체, str은 새 객체) |
| `138___new__.py` | `__new__` — 객체 생성 전 단계, `__init__` 이전 |
| `139_singleton.py` | `__new__` 오버라이드로 싱글톤 구현 |

---

## PART 10 · Iterator Generator Async

> **개념 흐름**: iterable → iterator → generator → coroutine → async/await  
> **핵심 연쇄**: `list` → `iter(list)` → `yield` → `send()` → `async def` → `await`  
> **Java 비교**: `Iterable/Iterator` → `CompletableFuture` → Project Reactor

| 파일 | 핵심 포인트 |
|------|------------|
| `140_iterable.py` | `__iter__` 구현 객체 — `for`, `list()`, `zip()` 등 사용 가능 |
| `141_iterator.py` | `__iter__` + `__next__` — 상태 유지 1회성 객체 |
| `142_custom_iterator.py` | 클래스로 이터레이터 직접 구현 — 파일 청크 읽기 등 |
| `143_generator.py` | `yield`로 간단한 이터레이터 — 지연 평가(lazy evaluation) |
| `144_yield.py` | `yield` 일시 정지 + 값 생성 + 재개 원리 |
| `145_send.py` | `gen.send(value)` — 제너레이터에 값 전달 (코루틴 기초) |
| `146_coroutine.py` | `@asyncio.coroutine` (구식) vs `async def` 코루틴 개념 |
| `147_async.py` | `async def` — 코루틴 함수 정의 |
| `148_await.py` | `await expr` — 코루틴/Future/Task 일시 정지 |
| `149_asyncio.py` | `asyncio.run()`, 이벤트 루프 개념 |
| `150_task.py` | `asyncio.create_task()` — 동시 실행 |
| `151_gather.py` | `asyncio.gather(*coros)` — 여러 코루틴 병렬 대기 |
| `152_queue.py` | `asyncio.Queue` — 비동기 생산자/소비자 패턴 |
| `153_lock.py` | `asyncio.Lock` — 비동기 임계 영역 보호 |

---

## PART 11 · Exception

> **개념 흐름**: 예외 계층 → try/except → finally → raise → 사용자 정의 예외

| 파일 | 핵심 포인트 |
|------|------------|
| `154_exception.py` | 예외 계층: `BaseException` → `Exception` → 구체적 예외 |
| `155_try_except.py` | `except ExcType as e:`, 다중 except, 특정 vs 일반 순서 |
| `156_finally.py` | `finally`: 예외 여부 무관 항상 실행 — 자원 해제 |
| `157_raise.py` | `raise`, `raise from`, 예외 체이닝, `raise` 재발생 |
| `158_custom_exception.py` | `Exception` 상속, `__init__` 커스터마이즈, 속성 추가 |
| `159_exception_hierarchy.py` | 전체 예외 계층 구조 탐색, `except` 순서 전략 |

---

## PART 12 · Module & Package

| 파일 | 핵심 포인트 |
|------|------------|
| `160_import.py` | `import`, `from X import Y`, `import X as Y` 의미 차이 |
| `161_package.py` | `__init__.py` 역할, 패키지 구조 설계 |
| `162___name__.py` | `__name__` 속성 — 모듈 이름 확인 |
| `163___main__.py` | `if __name__ == "__main__":` 완전 이해 |
| `164_importlib.py` | `importlib.import_module("name")` 동적 import |
| `165_pip.py` | pip 사용법, `requirements.txt`, `pyproject.toml` |
| `166_virtualenv.py` | `venv`, `virtualenv`, `conda` 격리 환경 |
| `167_package_publish.py` | `setup.py`, `pyproject.toml`, PyPI 배포 |

---

## PART 13 · File & Path

| 파일 | 핵심 포인트 |
|------|------------|
| `168_open.py` | `open(path, mode, encoding)`, `with` 컨텍스트 매니저 필수 |
| `169_read.py` | `read()`, `readline()`, `readlines()`, 이터레이터 순회 |
| `170_write.py` | `write()`, `writelines()`, 버퍼 flush |
| `171_append.py` | `mode='a'` 추가 모드, 로그 파일 패턴 |
| `172_seek.py` | `seek(offset, whence)`, `tell()` — 파일 포인터 |
| `173_pathlib.py` | `Path` 객체 — `/` 연산자로 경로 조합, OOP 스타일 |
| `174_os.py` | `os.path`, `os.walk()`, `os.environ`, `os.makedirs()` |
| `175_shutil.py` | `shutil.copy()`, `copytree()`, `rmtree()`, `move()` |
| `176_tempfile.py` | `tempfile.NamedTemporaryFile()`, `TemporaryDirectory()` |

---

## PART 14 · Data Processing

| 파일 | 핵심 포인트 |
|------|------------|
| `177_json.py` | `json.loads()`, `json.dumps()`, `indent`, `ensure_ascii` |
| `178_csv.py` | `csv.reader`, `csv.DictReader`, `csv.writer` |
| `179_pickle.py` | 직렬화/역직렬화, 보안 위험, 대안 |
| `180_sqlite.py` | `sqlite3` 내장 DB — ORM 없이 SQL |
| `181_datetime.py` | `datetime`, `date`, `time`, `timedelta` 연산 |
| `182_timezone.py` | `pytz`, `zoneinfo` (3.9+), aware/naive datetime |
| `183_regex.py` | `re.match`, `re.search`, `re.findall`, 그룹, 컴파일 |

---

## PART 15 · Collections Module

| 파일 | 핵심 포인트 |
|------|------------|
| `184_Counter.py` | 빈도 계산, `most_common(n)`, 산술 연산 |
| `185_defaultdict.py` | 키 없을 때 기본값 자동 생성, `defaultdict(list)` |
| `186_OrderedDict.py` | 삽입 순서 보장 (3.7+ dict도 보장, 차이점) |
| `187_deque.py` | 양방향 큐, `O(1)` appendleft/popleft — `list` 와 비교 |
| `188_ChainMap.py` | 여러 딕셔너리 체이닝 — 설정 우선순위 패턴 |
| `189_namedtuple.py` | `namedtuple("Point", ["x","y"])` — 이름 있는 튜플 |

---

## PART 16 · itertools

| 파일 | 핵심 포인트 |
|------|------------|
| `190_count.py` | `count(start, step)` — 무한 카운터 |
| `191_cycle.py` | `cycle(iterable)` — 무한 반복 |
| `192_repeat.py` | `repeat(obj, times)` — 값 반복 |
| `193_chain.py` | `chain(*iterables)` — 이터러블 연결 |
| `194_product.py` | `product(*iterables)` — 카르테시안 곱 |
| `195_permutation.py` | `permutations(iterable, r)` — 순열 |
| `196_combination.py` | `combinations(iterable, r)` — 조합 |
| `197_groupby.py` | `groupby(iterable, key)` — 연속 그룹화 (정렬 후 사용!) |

---

## PART 17 · Type Hint

> **핵심**: 타입 힌트는 실행에 영향 없음 — 문서화 + IDE 지원 + mypy 정적 검사

| 파일 | 핵심 포인트 |
|------|------------|
| `198_annotation.py` | 변수/함수 어노테이션, `__annotations__` 딕셔너리 |
| `199_Optional.py` | `Optional[X]` = `Union[X, None]` — None 가능 표현 |
| `200_Union.py` | `Union[int, str]` (3.9: `int \| str`) |
| `201_Literal.py` | `Literal["GET", "POST"]` — 특정 값만 허용 |
| `202_Generic.py` | `Generic[T]` — 제네릭 클래스 정의 |
| `203_TypeVar.py` | `T = TypeVar("T")` — 타입 변수 |
| `204_Protocol.py` | 구조적 서브타이핑 — `isinstance` 없이 duck typing 타입화 |
| `205_TypedDict.py` | `TypedDict` — 딕셔너리 구조 타입화 |
| `206_dataclass.py` | `@dataclass` — `__init__/repr/eq` 자동 생성 |

**추가 타입 도구**:

| 도구 | 핵심 |
|------|------|
| `Annotated[X, metadata]` | 타입 + 메타데이터 (Pydantic 필드 설명) |
| `Self` | 자기 자신 타입 반환 (빌더 패턴) |
| `Callable[[int, str], bool]` | 함수 타입 표현 |
| `NewType("UserId", int)` | 의미론적 타입 생성 |
| `ParamSpec` | 데코레이터의 파라미터 타입 보존 |
| `TypeAlias` | 복잡한 타입에 별칭 |
| Forward Reference `"ClassName"` | 미정의 클래스 타입 힌트 |

---

## PART 18 · Concurrency

> **개념 흐름**: threading → 동기화 → multiprocessing → asyncio  
> **핵심**: GIL 때문에 CPU 바운드는 multiprocessing, IO 바운드는 asyncio/threading  
> **실제 IO 작업 예제 중심**

| 파일 | 핵심 포인트 |
|------|------------|
| `207_threading.py` | `Thread(target, args)`, `start()`, `join()`, 데몬 스레드 |
| `208_Lock.py` | `Lock()`, `with lock:` — 임계 영역, 경쟁 조건 예방 |
| `209_RLock.py` | `RLock()` — 재진입 잠금, 같은 스레드 중복 획득 가능 |
| `210_Semaphore.py` | `Semaphore(n)` — 동시 접근 개수 제한 (DB 커넥션 풀) |
| `211_Event.py` | `Event()` — 스레드 간 신호 전달 |
| `212_Condition.py` | `Condition()` — `wait()`, `notify()`, `notify_all()` |
| `213_Queue.py` | `queue.Queue` — 스레드 안전 FIFO 큐 |
| `214_multiprocessing.py` | `Process`, `Pool.map()` — GIL 우회, CPU 바운드 |
| `215_ProcessPool.py` | `ProcessPoolExecutor`, `ThreadPoolExecutor` |
| `216_Future.py` | `concurrent.futures.Future` — 비동기 결과 핸들 |

---

## PART 19 · Metaprogramming

> **핵심**: 코드가 코드를 생성/수정 — Django ORM, SQLAlchemy, FastAPI의 비밀  
> **실제 프레임워크 활용 사례 포함**

| 파일 | 핵심 포인트 |
|------|------------|
| `217_metaclass.py` | 클래스의 클래스 — `type`이 기본 메타클래스 |
| `218_type().py` | `type(name, bases, dict)` 동적 클래스 생성 |
| `219_custom_metaclass.py` | `class Meta(type):` — `__new__`, `__init__` 오버라이드 |
| `220_inspect.py` | `inspect.signature`, `getmembers`, `getsource` |
| `221_ast.py` | `ast.parse()`, AST 노드 방문, 코드 분석/변환 |
| `222_dis.py` | `dis.dis(func)` — 바이트코드 디스어셈블 |
| `223_compile.py` | `compile(source, filename, mode)` — 코드 객체 생성 |
| `224_exec.py` | `exec(code, globals, locals)` — 동적 코드 실행 |
| `225_eval.py` | `eval(expr, globals, locals)` 심화 |
| `226_dynamic_class_creation.py` | ORM 모델 동적 생성, 플러그인 시스템 |

---

## PART 20 · Modern Python

> **Python 3.8~3.12 주요 문법 신기능**

| 파일 | 핵심 포인트 |
|------|------------|
| `227_f_string.py` | `f"{x=}"` 디버깅, `f"{val:{width}.{prec}f}"` 중첩 |
| `228_walrus_operator.py` | `:=` 대입식 — `while chunk := f.read(8192):` |
| `229_positional_only.py` | `/` 위치 전용 파라미터 (3.8+) |
| `230_keyword_only.py` | `*` 키워드 전용 파라미터 심화 |
| `231_match_case.py` | `match/case` 구조적 패턴 매칭 (3.10+) |
| `232_pattern_matching_advanced.py` | 클래스 패턴, 가드, OR 패턴, 캡처 패턴 |

---

## PART 21 · NumPy

> **목표**: NumPy 소스 코드 읽기 + 벡터화 연산 이해  
> **핵심**: 루프 없이 C 속도로 배열 연산

| 파일 | 핵심 포인트 |
|------|------------|
| `233_ndarray.py` | `np.array()`, Python list vs ndarray 구조 차이 |
| `234_shape.py` | `arr.shape` — `(rows, cols, depth)` 차원 구조 |
| `235_reshape.py` | `reshape()`, `ravel()`, `-1` 자동 계산 |
| `236_dtype.py` | `int32`, `float64`, `bool_` — 메모리 레이아웃 영향 |
| `237_slicing.py` | `arr[1:3, ::2]` — 다차원 슬라이싱, 뷰 반환 |
| `238_indexing.py` | 팬시 인덱싱 `arr[[0,2,4]]`, 정수 배열 인덱싱 |
| `239_broadcasting.py` | shape `(3,1)` + `(1,4)` → `(3,4)` 자동 확장 규칙 |
| `240_vectorization.py` | `for` 루프 vs ufunc 속도 비교 |
| `241_axis.py` | `axis=0` (열방향), `axis=1` (행방향) 집계 |
| `242_aggregation.py` | `sum`, `mean`, `std`, `min`, `max`, `argmax` |
| `243_random.py` | `np.random.seed()`, `randn`, `randint`, `choice` |
| `244_memory_model.py` | C/Fortran 메모리 배치, view vs copy, strides |

---

## PART 22 · Pandas

> **목표**: 데이터 분석 코드 읽기 + 기본 조작 능력

| 파일 | 핵심 포인트 |
|------|------------|
| `245_Series.py` | 1D 레이블 배열 — 인덱스+값, `NaN` 처리 |
| `246_DataFrame.py` | 2D 표 구조 — 생성, 정보 확인, 컬럼 선택 |
| `247_loc.py` | `loc[label, cols]` — 레이블 기반 선택 |
| `248_iloc.py` | `iloc[pos, cols]` — 정수 위치 기반 선택 |
| `249_groupby.py` | `groupby("col").agg({"val": "sum"})` |
| `250_merge.py` | `pd.merge(left, right, on="key", how="inner")` |
| `251_pivot.py` | `pivot_table(values, index, columns, aggfunc)` |
| `252_apply.py` | `df.apply(func, axis=)`, `df["col"].map(func)` |

---

## PART 23 · PyTorch Reading

> **목표**: PyTorch 소스 코드 읽기 — 모델 작성이 아님  
> **핵심**: `nn.Module`, autograd, hook 메커니즘 이해

| 파일 | 핵심 포인트 |
|------|------------|
| `253_tensor.py` | `torch.Tensor` — ndarray와 비교, device, dtype |
| `254_autograd.py` | `requires_grad=True`, `.grad` 속성 |
| `255_computational_graph.py` | 동적 계산 그래프 — 순전파 시 구축 |
| `256_nn_Module.py` | `__init__`, `forward`, `parameters()` |
| `257_Parameter.py` | `nn.Parameter` — 자동 등록되는 텐서 |
| `258_forward.py` | `model(x)` → `__call__` → hooks → `forward()` |
| `259_backward.py` | `loss.backward()` — gradient 계산 |
| `260_optimizer.py` | `optimizer.zero_grad()`, `step()` |
| `261_Dataset.py` | `__len__`, `__getitem__` 구현 |
| `262_DataLoader.py` | 배치, 셔플, worker, collate_fn |
| `263_training_loop.py` | 전체 학습 루프 패턴 분석 |
| `264_custom_layer.py` | `nn.Module` 상속 커스텀 레이어 |
| `265_custom_loss.py` | 손실 함수 구현, `reduction` 파라미터 |

**추가 심화**:
- `register_buffer` vs `register_parameter` 차이
- `ModuleList`, `Sequential` 구조
- `state_dict()`, `load_state_dict()` 저장/복원
- `hook` — forward/backward 중간값 추출
- custom autograd Function (`Function.apply`)

---

## PART 24 · CPython Internals

> **목표**: Python이 어떻게 동작하는지 내부 구조 이해  
> **도구**: `dis`, `sys`, `gc`, `ctypes`

| 파일 | 핵심 포인트 |
|------|------------|
| `266_memory_model.py` | 힙 할당, PyObject 구조, obmalloc |
| `267_reference_count.py` | `sys.getrefcount()`, 참조 추가/제거 추적 |
| `268_garbage_collector.py` | 세대별 GC, `gc.collect()`, 순환 참조 |
| `269_descriptor_internals.py` | `__get__` 호출 순서 — 클래스 vs 인스턴스 딕셔너리 |
| `270_function_object.py` | `func.__code__`, `func.__globals__`, `func.__closure__` |
| `271_code_object.py` | `co_varnames`, `co_consts`, `co_bytecode` |
| `272_frame_object.py` | `sys._getframe()` — 실행 컨텍스트, 로컬 변수 |
| `273_import_system.py` | `sys.modules` 캐시, `__import__`, `importlib` |
| `274_bytecode.py` | `dis.dis()` 출력 해석 — LOAD_FAST, CALL_FUNCTION |
| `275_cpython_execution.py` | 인터프리터 루프 — ceval.c 흐름 |
| `276_GIL.py` | Global Interpreter Lock — 스레드 전환, GIL 우회 |

---

## PART 25 · Projects

> **목표**: 앞서 배운 모든 것을 통합 — 실전 프로젝트  
> **각 프로젝트는 최소 1개 이상의 PART 17~24 기술 사용**

| 파일 | 사용 기술 |
|------|-----------|
| `277_CLI.py` | argparse, dataclass, pathlib |
| `278_crawler.py` | asyncio, aiohttp, BeautifulSoup |
| `279_phonebook.py` | dataclass, json, pathlib, TypedDict |
| `280_file_searcher.py` | os.walk, regex, generator, asyncio |
| `281_log_analyzer.py` | regex, Counter, groupby, pandas |
| `282_REST_API_server.py` | FastAPI, Pydantic, async, SQLAlchemy |
| `283_ORM.py` | 메타클래스, 디스크립터, SQLite |
| `284_mini_framework.py` | 데코레이터, 메타클래스, WSGI |
| `285_mini_async_framework.py` | asyncio, 이벤트 루프, 소켓 |
| `286_mini_interpreter.py` | ast, 렉서, 파서, 트리 워커 |

---

## 📊 학습 로드맵

```
[PART 01-02] ───── 기초 다지기 (2주)
     ↓
[PART 03-04] ───── Pythonic Thinking 체화 (2주)
     ↓
[PART 05-06] ───── 메모리/함수 심화 (1주)
     ↓
[PART 07-09] ───── OOP 완성 (2주)
     ↓
[PART 10] ──────── Iterator/Generator/Async (2주) ← 가장 중요
     ↓
[PART 11-14] ───── 실무 기반 (1주)
     ↓
[PART 15-16] ───── 표준 라이브러리 (1주)
     ↓
[PART 17] ──────── 타입 시스템 (1주)
     ↓
[PART 18-19] ───── 동시성/메타프로그래밍 (2주)
     ↓
[PART 20] ──────── 모던 Python 문법 (3일)
     ↓
[PART 21-23] ───── 데이터/ML 라이브러리 읽기 (2주)
     ↓
[PART 24] ──────── CPython 내부 (1주)
     ↓
[PART 25] ──────── 프로젝트 통합 (2주)
```

**총 예상 기간**: 약 20주 (집중 학습 기준)

---

## ⚡ Java 개발자 핵심 체크리스트

- [ ] 변수 = 이름표 (상자 아님) → `is` vs `==` 구분
- [ ] `int`는 무제한 정밀도, 오버플로우 없음
- [ ] `/` 나눗셈은 항상 `float`, 정수 원하면 `//`
- [ ] 음수 floor division: `-7//2 == -4` (Java: `-3`)
- [ ] mutable 기본값 함정: `def f(lst=[])` 절대 금지
- [ ] `for`는 항상 for-each, 인덱스는 `range(len())`
- [ ] `bool`은 `int` 서브클래스: `True+True==2`
- [ ] `None` 비교는 `is None` (== 금지)
- [ ] `str`은 불변 — 수정 = 새 객체
- [ ] Falsy: `0`, `""`, `[]`, `{}`, `None` 모두 False
- [ ] 함수는 1급 객체 — 변수에 할당, 인자로 전달 가능
- [ ] `self`는 Java의 `this`이나 **명시적 선언 필수**
- [ ] `__init__`은 생성자이나 `__new__`가 더 앞에 실행
- [ ] GIL: Python 스레드는 CPU 바운드에 효과 없음
- [ ] `async def` + `await` = 협력적 멀티태스킹

---

## 🔗 참고 자료

| 자료 | 링크 |
|------|------|
| 공식 문서 | https://docs.python.org/3/ |
| PEP 8 스타일 | https://pep8.org |
| CPython 소스 | https://github.com/python/cpython |
| 파이썬 데이터 모델 | https://docs.python.org/3/reference/datamodel.html |
| 추천 도서 | *Fluent Python 2nd Ed.* (Luciano Ramalho) |
| 추천 도서 | *Python Cookbook 3rd Ed.* |
