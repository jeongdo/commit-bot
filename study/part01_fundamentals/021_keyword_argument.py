# ============================================================================
# 021 - keyword_argument (키워드 인수)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. 위치 인수 / 키워드 인수 / 키워드전용 / 위치전용의 차이를 완전히 안다
#   2. * 구분자로 키워드 전용 강제, / 구분자로 위치 전용 강제
#   3. inspect로 파라미터 종류를 프로그래밍적으로 분석한다
#   4. API 설계에서 각 파라미터 종류를 언제 쓰는지 판단한다
#
# [왜 필요한가]
#   - 키워드 전용 인수: 인수 순서 실수 방지 (함수 호출 안전성)
#   - 위치 전용 인수: 파라미터명 변경의 자유 (API 안정성)
#   - 실무 라이브러리 API는 대부분 이 구분을 명시적으로 설계
#
# [Java 비교]
#   Java  : 위치 기반만 (키워드 인수 없음, 오버로딩으로 대체)
#   Python: 위치 / 키워드 / 키워드전용(* 이후) / 위치전용(/ 이전)
# ============================================================================

import inspect

# ── LEVEL 1: 위치 인수 vs 키워드 인수 ──────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 위치 vs 키워드 인수")
print("=" * 50)

def send_email(to: str, subject: str, body: str) -> str:
    return f"To:{to} | Sub:{subject} | Body:{body[:20]}"

# 위치 인수: 순서가 중요
r1 = send_email("alice@test.com", "Hello", "본문 내용입니다")
print(f"위치: {r1}")

# 키워드 인수: 순서 무관, 명확성 향상
r2 = send_email(subject="Meeting", to="bob@test.com", body="회의 내용")
print(f"키워드: {r2}")

# 혼합: 위치 인수는 앞에, 키워드 인수는 뒤에
r3 = send_email("carol@test.com", body="내용", subject="제목")
print(f"혼합: {r3}")

# ── LEVEL 2: * 로 키워드 전용 강제 ─────────────────────────────────────────

print("\nLEVEL 2: 키워드 전용 인수 (*)")
print("-" * 40)

# * 이후의 파라미터는 반드시 키워드로 전달
def create_connection(
    host: str,
    port: int,
    *,              # ← 이 이후는 모두 키워드 전용
    timeout: int = 30,
    ssl: bool = False,
    retry: int = 3,
):
    return f"{host}:{port} (timeout={timeout}, ssl={ssl}, retry={retry})"

# 올바른 호출
print(create_connection("localhost", 5432))
print(create_connection("db.server.com", 5432, timeout=10, ssl=True))
print(create_connection("localhost", 3306, retry=5, timeout=60, ssl=False))

# 잘못된 호출: timeout을 위치 인수로 전달 → TypeError
try:
    create_connection("localhost", 5432, 10)  # timeout을 3번째 위치로
except TypeError as e:
    print(f"TypeError: {e}")

# 왜 키워드 전용으로 강제하는가?
# create_connection("host", 5432, 10, True, 3)  → 어떤 값이 뭔지 불명확
# create_connection("host", 5432, timeout=10, ssl=True)  → 명확!

# ── LEVEL 2: / 로 위치 전용 강제 (Python 3.8+) ─────────────────────────────

print("\nLEVEL 2: 위치 전용 인수 (/)")
print("-" * 40)

# / 이전의 파라미터는 반드시 위치 인수로 전달
def rectangle_area(width: float, height: float, /) -> float:
    """
    width, height는 위치 전용 (파라미터명으로 호출 불가)
    이유: 파라미터명을 내부 구현 상세로 취급,
          나중에 w, h로 이름 바꿔도 API 깨지지 않음
    """
    return width * height

print(f"area(10, 5) = {rectangle_area(10, 5)}")

try:
    rectangle_area(width=10, height=5)   # TypeError!
except TypeError as e:
    print(f"키워드 전달 불가: {e}")

# Python 내장 함수들이 이 방식 사용
# abs(-5) → 가능, abs(x=-5) → TypeError
# len([]) → 가능, len(obj=[]) → TypeError

# ── LEVEL 2: 완전한 시그니처 — 위치전용 + 일반 + 키워드전용 ────────────────

print("\nLEVEL 2: 완전한 시그니처")
print("-" * 40)

def complex_func(
    pos_only1,           # 위치 전용
    pos_only2,           # 위치 전용
    /,                   # ← 이전은 위치 전용
    normal_pos_or_kw,    # 위치 또는 키워드 모두 가능
    *,                   # ← 이후는 키워드 전용
    kw_only1,
    kw_only2 = "default",
) -> str:
    return f"pos:{pos_only1},{pos_only2} | normal:{normal_pos_or_kw} | kw:{kw_only1},{kw_only2}"

# 다양한 올바른 호출 방식
print(complex_func(1, 2, 3, kw_only1="a"))
print(complex_func(1, 2, normal_pos_or_kw=3, kw_only1="b", kw_only2="c"))

# 잘못된 호출들
for bad_call, expected_error in [
    (lambda: complex_func(1, pos_only2=2, normal_pos_or_kw=3, kw_only1="x"),
     "pos_only2는 위치전용"),
    (lambda: complex_func(1, 2, 3, 4, kw_only1="x"),
     "일반 인수 초과"),
]:
    try:
        bad_call()
        print(f"  오류 없음 (예상: {expected_error})")
    except TypeError as e:
        print(f"  TypeError ({expected_error}): {e}")

# ── LEVEL 3: inspect로 파라미터 분석 ────────────────────────────────────────

print("\nLEVEL 3: inspect.signature() 분석")
print("-" * 40)

def analyze_signature(func):
    sig = inspect.signature(func)
    print(f"  함수: {func.__name__}{sig}")
    for name, param in sig.parameters.items():
        kind_map = {
            inspect.Parameter.POSITIONAL_ONLY:          "위치전용    (/ 이전)",
            inspect.Parameter.POSITIONAL_OR_KEYWORD:    "위치또는키워드",
            inspect.Parameter.VAR_POSITIONAL:           "*args      ",
            inspect.Parameter.KEYWORD_ONLY:             "키워드전용  (* 이후)",
            inspect.Parameter.VAR_KEYWORD:              "**kwargs   ",
        }
        kind_str = kind_map.get(param.kind, str(param.kind))
        default = f" = {param.default!r}" if param.default is not inspect.Parameter.empty else ""
        print(f"    {name:<20} {kind_str}{default}")

analyze_signature(complex_func)
print()
analyze_signature(create_connection)
print()
# 내장 함수 분석
analyze_signature(sorted)

# ── LEVEL 4: API 설계 가이드 ────────────────────────────────────────────────

print("\nLEVEL 4: API 설계 가이드")
print("-" * 40)

# 실무 설계 원칙:
# 1. 필수 데이터 → 위치 인수 (짧고 명확)
# 2. 옵션/플래그 → 키워드 전용 (가독성, 실수 방지)
# 3. 내부 구현 상세명 → 위치 전용 (나중에 이름 변경 자유)

class DataProcessor:
    """실무 API 설계 예시"""

    def load(
        self,
        source,              # 필수: 데이터 소스
        /,                   # source는 위치전용 (구현 상세)
        *,                   # 이후 모두 키워드 전용
        encoding = "utf-8",
        skip_errors = False,
        max_rows = None,
        verbose = False,
    ):
        """
        source를 로드한다.

        Args:
            source: 파일 경로 또는 URL (위치 전용)
            encoding: 인코딩 (기본: utf-8)
            skip_errors: 오류 행 건너뜀 여부
            max_rows: 최대 행 수
            verbose: 진행 상황 출력
        """
        desc = f"load({source!r}, enc={encoding}, skip={skip_errors}"
        if max_rows: desc += f", max={max_rows}"
        desc += ")"
        if verbose: print(f"  [verbose] {desc}")
        return {"source": source, "rows": 100}

dp = DataProcessor()
dp.load("data.csv", verbose=True)
dp.load("db://prod/users", encoding="euc-kr", max_rows=1000, verbose=True)

# ── LEVEL 5: functools.partial로 파라미터 고정 ──────────────────────────────

print("\nLEVEL 5: partial로 API 특화 버전 생성")
print("-" * 40)

from functools import partial

def http_request(url, /, *, method="GET", timeout=30, headers=None, auth=None):
    headers = headers or {}
    return f"{method} {url} (timeout={timeout}, headers={headers})"

# partial로 공통 설정 고정
api_get  = partial(http_request, method="GET",  timeout=10)
api_post = partial(http_request, method="POST", timeout=30)
secure_get = partial(http_request, method="GET", auth="Bearer token123")

print(api_get("/api/users"))
print(api_post("/api/orders"))
print(secure_get("/api/admin/data"))
print(api_get("/api/items", headers={"Accept": "application/json"}))

# ============================================================================
# [주의사항]
#   1. * 단독: func(a, b, *, c) → c는 반드시 키워드
#   2. / 단독: func(a, b, /, c) → a,b는 반드시 위치
#   3. def func(a, /, *, b) → a: 위치전용, b: 키워드전용, 일반 파라미터 없음
#   4. *args 가 있으면 그 뒤는 자동으로 키워드전용 (별도 * 불필요)
#   5. inspect.Parameter.empty 로 기본값 없음 확인
#
# [다음 단계]
#   → 022_namespace.py: 네임스페이스와 LEGB 규칙
# ============================================================================
