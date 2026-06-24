# ============================================================================
# 010 - eval() / exec() (동적 코드 실행)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. eval()과 exec()의 차이와 내부 동작을 이해한다
#   2. eval()의 보안 위험성과 절대 사용 금지 상황을 안다
#   3. ast.literal_eval()과 제한된 네임스페이스 패턴을 익힌다
#   4. compile()로 코드 객체를 캐싱하는 실무 패턴을 안다
#
# [왜 필요한가]
#   - 동적 설정 파싱, 공식(formula) 계산기, 플러그인 시스템에서 사용
#   - 잘못 쓰면 "코드 인젝션" — 보안 취약점 직결
#   - ast.literal_eval이 올바른 대안임을 알아야 함
#
# [Java 비교]
#   Java  : 런타임 동적 코드 실행은 매우 어려움 (Reflection, Scripting API)
#   Python: eval(), exec()로 쉽게 가능 → 강력하지만 위험
# ============================================================================

import ast
import sys
import io

# ── LEVEL 1: eval() 기초 ────────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: eval() 기초")
print("=" * 50)

# eval(): 표현식(expression) 문자열 → 평가 → 값 반환
print(eval("1 + 2 * 3"))           # 7
print(eval("len('hello')"))       # 5
print(eval("[1, 2, 3]"))           # [1, 2, 3]
print(eval("{'a': 1, 'b': 2}"))  # {'a': 1, 'b': 2}
print(eval("max(10, 20, 30)"))     # 30

# 변수 참조 가능
x = 10
print(eval("x * 2"))               # 20 (현재 globals/locals 참조)

# eval()과 exec()의 차이
# eval(): 표현식만, 값 반환
# exec(): 문(statement) 실행, None 반환
result = eval("3 ** 4")            # 표현식 → 81 반환
print(f"eval 반환값: {result}")

result = exec("y = 100\nprint(y)")  # 문 실행 → None 반환, 출력 발생
print(f"exec 반환값: {result}")     # None

# ── LEVEL 2: 보안 위험 — 사용자 입력을 eval에 절대 금지 ────────────────────

print("\nLEVEL 2: 보안 위험 — 절대 금지 패턴")
print("-" * 40)

# 아래는 실행하지 않지만, 이런 코드가 왜 위험한지 설명
dangerous_inputs = [
    "__import__('os').getcwd()",              # 파일시스템 접근
    "__import__('os').system('ls -la')",    # 시스템 명령 실행
    "open('/etc/passwd').read()",             # 파일 읽기
    "__import__('subprocess').run(['rm','-rf','/tmp'])",  # 파일 삭제
    "[x for x in ().__class__.__bases__[0].__subclasses__()]",  # 클래스 탐색
]

print("위험한 eval 입력 예시 (실행 안 함):")
for d in dangerous_inputs:
    print(f"  eval({d[:50]!r}...)")

print("\n→ 사용자로부터 받은 문자열을 eval()에 절대 넣지 말 것!")
print("→ 안전한 대안: ast.literal_eval()")

# ── LEVEL 3: ast.literal_eval — 안전한 대안 ─────────────────────────────────

print("\nLEVEL 3: ast.literal_eval — 안전한 대안")
print("-" * 40)

# ast.literal_eval: Python 리터럴(상수)만 평가 — 함수 호출, 변수 접근 불가
safe_inputs = [
    "42",
    "3.14",
    "'hello'",
    "[1, 2, 3]",
    "(1, 2, 3)",
    "{'key': 'value', 'num': 42}",
    "{1, 2, 3}",
    "True",
    "None",
]

print("안전하게 파싱 가능한 리터럴:")
for s in safe_inputs:
    result = ast.literal_eval(s)
    print(f"  {s:<35} → {result!r:<20} ({type(result).__name__})")

# 위험한 표현식은 안전하게 거부
unsafe_inputs = [
    "__import__('os')",
    "1 + 1",          # 연산도 거부!
    "len('hi')",    # 함수 호출 거부
    "x",              # 변수 참조 거부
]
print("\n거부되는 표현식:")
for s in unsafe_inputs:
    try:
        ast.literal_eval(s)
        print(f"  {s!r} → 통과 (주의!)")
    except (ValueError, SyntaxError) as e:
        print(f"  {s!r} → 안전하게 거부: {type(e).__name__}")

# 실무: 설정 파일 파싱
config_str = "{\'debug\': True, \'port\': 8080, \'hosts\': [\'localhost\', \'127.0.0.1\']}"
config_str2 = "{\"debug\": True, \"port\": 8080}"
# JSON은 json.loads, Python 딕셔너리 리터럴은 ast.literal_eval
import json
config = {"debug": True, "port": 8080, "hosts": ["localhost"]}
print(f"\njson.loads: {json.loads(json.dumps(config))}")

# ── LEVEL 3: 제한된 네임스페이스로 eval 안전하게 사용 ──────────────────────

print("\nLEVEL 3: 제한된 네임스페이스 eval")
print("-" * 40)

# eval(expr, globals, locals)의 두 번째/세 번째 인자로 네임스페이스 제한
def safe_math_eval(expr, variables=None):
    """수식만 평가 — 함수, 변수 접근 제한"""
    allowed_globals = {
        "__builtins__": {},   # 내장 함수 완전 차단
        "abs": abs, "round": round,
        "max": max, "min": min,
        "sum": sum, "pow": pow,
        "int": int, "float": float,
    }
    allowed_locals = variables or {}
    try:
        return eval(expr, allowed_globals, allowed_locals)
    except Exception as e:
        raise ValueError(f"평가 실패: {e}")

# 안전한 수식 평가
for expr, vars_ in [
    ("x ** 2 + y ** 2", {"x": 3, "y": 4}),
    ("abs(a - b) + max(c, d)", {"a": -5, "b": 3, "c": 7, "d": 2}),
    ("round(3.14159, 2)", {}),
]:
    result = safe_math_eval(expr, vars_)
    print(f"  eval({expr!r}, {vars_}) = {result}")

# 차단 확인
for dangerous in ["__import__('os')", "open('/etc/passwd')"]:
    try:
        safe_math_eval(dangerous)
        print(f"  경고: {dangerous!r} 통과!")
    except ValueError as e:
        print(f"  차단됨: {dangerous!r}")

# ── LEVEL 4: exec() — 동적 코드 실행 ────────────────────────────────────────

print("\nLEVEL 4: exec() 활용")
print("-" * 40)

# exec()로 함수 동적 생성
template = """
def {name}(x, y):
    return x {op} y
"""
namespace = {}
for name, op in [("add", "+"), ("mul", "*"), ("mod", "%")]:
    exec(template.format(name=name, op=op), namespace)

print(f"add(3, 4) = {namespace['add'](3, 4)}")   # 7
print(f"mul(3, 4) = {namespace['mul'](3, 4)}")   # 12
print(f"mod(10,3) = {namespace['mod'](10, 3)}")  # 1

# compile() + exec() — 코드 재사용 (한 번만 컴파일)
code_str = """
result = 0
for i in range(1, n + 1):
    result += i
"""
code_obj = compile(code_str, "<sum_formula>", "exec")

for n in [10, 100, 1000]:
    env = {"n": n}
    exec(code_obj, env)   # 미리 컴파일된 코드 재사용
    print(f"  1~{n} 합: {env['result']}")

# ── LEVEL 5: AST 활용 — 코드 분석 ──────────────────────────────────────────

print("\nLEVEL 5: AST로 코드 안전 분석")
print("-" * 40)

import ast

def is_safe_expression(expr):
    """수식에 허용되지 않는 노드가 있는지 검사"""
    SAFE_NODES = {
        ast.Expression, ast.BinOp, ast.UnaryOp,
        ast.Num, ast.Constant,  # 상수
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.FloorDiv, ast.Mod, ast.Pow,
        ast.UAdd, ast.USub,
        ast.Compare, ast.Eq, ast.Lt, ast.Gt, ast.LtE, ast.GtE,
    }
    try:
        tree = ast.parse(expr, mode="eval")
        for node in ast.walk(tree):
            if type(node) not in SAFE_NODES:
                return False, type(node).__name__
        return True, None
    except SyntaxError:
        return False, "SyntaxError"

test_exprs = [
    "1 + 2 * 3",
    "x ** 2 + y ** 2",
    "__import__('os')",
    "len('hello')",
    "(1 + 2) * 3 - 4 / 2",
]
for expr in test_exprs:
    safe, reason = is_safe_expression(expr)
    status = "✓ 안전" if safe else f"✗ 위험({reason})"
    print(f"  {expr!r:<40} → {status}")

# ============================================================================
# [주의사항]
#   1. eval()에 사용자 입력 절대 금지 — 코드 인젝션 취약점
#   2. 설정 파일 파싱은 ast.literal_eval() 또는 json.loads()
#   3. compile()로 코드 객체 캐싱하면 반복 실행 시 성능 향상
#   4. exec()의 반환값은 항상 None
#   5. 제한된 네임스페이스로도 완벽한 차단 보장 못 함 → 설계 재검토 권장
#
# [다음 단계]
#   → 011_operator.py: 연산자 완전 정복
# ============================================================================
