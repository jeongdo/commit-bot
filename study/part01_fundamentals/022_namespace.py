# ============================================================================
# 022 - namespace (네임스페이스와 LEGB 규칙)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. Python 네임스페이스의 4가지 범위(LEGB)를 완전히 이해한다
#   2. globals(), locals(), vars()로 네임스페이스를 직접 관찰한다
#   3. global, nonlocal 키워드의 동작을 정확히 안다
#   4. 스코프 체인과 이름 탐색 순서를 그림으로 그릴 수 있다
#
# [왜 필요한가]
#   - 변수 탐색 순서를 모르면 UnboundLocalError의 원인을 못 찾음
#   - 클로저 구현의 기반 개념
#   - LEGB 이해 없이는 데코레이터/메타프로그래밍 불가
#
# [Java 비교]
#   Java  : 블록 스코프 (중괄호 기준), 명시적 접근 제어(public/private)
#   Python: 함수 스코프 (들여쓰기 기준), 모듈/클래스/함수 3계층
# ============================================================================

import builtins

# ── LEVEL 1: LEGB 규칙 기초 ─────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: LEGB 규칙")
print("=" * 50)

# L: Local   — 현재 함수 내부
# E: Enclosing — 중첩 함수의 바깥 함수
# G: Global  — 모듈 최상위 (현재 파일)
# B: Builtins — Python 내장 (len, print, ...)

x = "Global"  # G

def outer():
    x = "Enclosing"  # E

    def inner():
        x = "Local"  # L
        print(f"  inner():     x = {x!r}")   # L에서 발견

    def enclosing_only():
        # x = "Local" 없음 → E에서 탐색
        print(f"  enclosing(): x = {x!r}")   # E에서 발견

    inner()
    enclosing_only()

outer()
print(f"  global:      x = {x!r}")   # G에서 발견

# B: 내장 이름
print(f"  builtins:    len = {len}")   # B에서 발견

# ── LEVEL 2: 이름 탐색 과정 시각화 ─────────────────────────────────────────

print("\nLEVEL 2: 이름 탐색 순서 시각화")
print("-" * 40)

# B: 내장 len
print(f"len (B): {len}")

# G: 전역 len이 있으면 B를 가림
len_backup = len   # 백업

# 전역에서 내장 이름 가리기 (비권장!)
# len = "전역이 내장을 가림"
# def test(): print(len)   # 전역 len 출력 (B 가림)
# del len  # 복원

# 각 스코프의 네임스페이스 관찰
GLOBAL_VAR = "나는 전역 변수"

def scope_demo():
    local_var = "나는 지역 변수"

    print(f"  locals()  = {list(locals().keys())}")
    print(f"  globals() 키 일부 = {list(globals().keys())[:5]}")

    # 전역 변수 접근 (읽기는 선언 없이 가능)
    print(f"  전역 접근: {GLOBAL_VAR!r}")

scope_demo()

# ── LEVEL 3: global / nonlocal 키워드 ───────────────────────────────────────

print("\nLEVEL 3: global / nonlocal")
print("-" * 40)

# global: 함수 내에서 전역 변수 수정
page_count = 0

def render_page(content):
    global page_count
    page_count += 1    # global 없으면 UnboundLocalError!
    return f"페이지 {page_count}: {content}"

print(render_page("홈"))
print(render_page("소개"))
print(render_page("문의"))
print(f"총 {page_count}페이지 렌더링")

# nonlocal: 중첩 함수에서 바깥 함수 변수 수정
def make_counter(start=0, step=1):
    """클로저 카운터 — nonlocal로 상태 유지"""
    count = start

    def increment(by=None):
        nonlocal count
        count += by if by is not None else step
        return count

    def reset():
        nonlocal count
        count = start

    def get():
        return count   # 읽기는 nonlocal 불필요

    return increment, reset, get

inc, reset, get = make_counter(start=10, step=5)
print(f"\n카운터: {get()}")
print(f"증가: {inc()}, {inc()}, {inc()}")
print(f"by=2: {inc(by=2)}")
reset()
print(f"리셋 후: {get()}")

# ── LEVEL 3: UnboundLocalError 함정 ─────────────────────────────────────────

print("\nLEVEL 3: UnboundLocalError 함정")
print("-" * 40)

x = 100

def problem():
    # 이 함수 안에 x = ... 가 있으면 Python은 x를 지역 변수로 취급
    # print(x) 시점에 아직 할당 전 → UnboundLocalError
    try:
        print(f"x = {x}")   # 오류! x가 지역 변수인데 아직 할당 전
    except UnboundLocalError as e:
        print(f"  UnboundLocalError: {e}")
    x = 200   # 이 줄이 있어서 위에서 오류

problem()
print(f"전역 x = {x}")  # 100 (변경 없음)

# 해결 방법
def fixed():
    global x
    print(f"x before = {x}")
    x = 200

def fixed_no_global():
    local_x = x   # 전역을 지역에 복사
    # 이제 local_x를 수정해도 전역 영향 없음
    local_x = 300
    print(f"local_x = {local_x}")

fixed_no_global()
print(f"전역 x = {x}")  # 100 (변경 없음)

# ── LEVEL 4: 네임스페이스 딕셔너리 직접 조작 ────────────────────────────────

print("\nLEVEL 4: 네임스페이스 딕셔너리 직접 조작")
print("-" * 40)

# globals()는 실제 전역 딕셔너리 (수정 가능!)
globals()["DYNAMIC_VAR"] = "동적으로 추가된 전역 변수"
print(f"동적 전역 변수: {DYNAMIC_VAR}")

# vars(obj)는 객체의 __dict__ 반환
class Config:
    debug = False
    port  = 8080

cfg = Config()
cfg.name = "MyApp"

print(f"\nvars(Config) = {vars(Config)['debug']}")
print(f"vars(cfg)    = {vars(cfg)}")

# 동적 속성 설정
fields = {"host": "localhost", "db": "mydb", "user": "admin"}
for key, val in fields.items():
    setattr(cfg, key, val)
print(f"동적 설정 후: {vars(cfg)}")

# ── LEVEL 5: 오픈소스 패턴 — 플러그인 레지스트리 ────────────────────────────

print("\nLEVEL 5: 플러그인 레지스트리 (네임스페이스 활용)")
print("-" * 40)

# 전역 레지스트리를 사용한 플러그인 시스템
_REGISTRY = {}

def register(name):
    """함수를 플러그인으로 등록하는 데코레이터"""
    def decorator(func):
        _REGISTRY[name] = func
        return func
    return decorator

@register("hello")
def plugin_hello(args):
    return f"Hello, {args.get('name', 'World')}!"

@register("add")
def plugin_add(args):
    return args.get("a", 0) + args.get("b", 0)

@register("echo")
def plugin_echo(args):
    return args

# 플러그인 실행
for cmd, args in [
    ("hello", {"name": "Alice"}),
    ("add",   {"a": 10, "b": 32}),
    ("echo",  {"msg": "test"}),
    ("unknown", {}),
]:
    if cmd in _REGISTRY:
        result = _REGISTRY[cmd](args)
        print(f"  {cmd}({args}) = {result}")
    else:
        print(f"  {cmd}: 등록되지 않은 플러그인")

print(f"\n등록된 플러그인: {list(_REGISTRY.keys())}")

# ============================================================================
# [주의사항]
#   1. LEGB 탐색 중 L에서 같은 이름의 할당이 있으면 전역 가림 (shadowing)
#   2. global/nonlocal 없이는 함수 내 할당은 항상 지역 변수 생성
#   3. globals() 직접 수정 가능하지만 남용 시 추적 어려움
#   4. 클로저에서 루프 변수 캡처 함정 → late binding (022 연장선)
#   5. builtins(B) 이름을 전역(G)에서 가리는 것은 위험한 패턴
#
# [다음 단계]
#   → 023_local_variable.py: 지역 변수 심화 — 스택 프레임
# ============================================================================
