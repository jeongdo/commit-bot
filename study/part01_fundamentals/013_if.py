# ============================================================================
# 013 - if (조건문)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. if/elif/else 구조와 조건 표현식을 완전히 익힌다
#   2. 가드 클로즈(Guard Clause) 패턴으로 중첩을 줄인다
#   3. 딕셔너리 디스패치로 switch-case를 대체한다
#   4. 조건문 최적화와 가독성 패턴을 체화한다
#
# [왜 필요한가]
#   - 모든 프로그램의 제어 흐름 기반
#   - Python에는 switch/case가 없었음 (3.10+에 match/case 추가)
#   - 가드 클로즈 패턴은 프로덕션 코드 가독성의 핵심
#
# [Java 비교]
#   Java  : if/else, switch/case, 삼항연산자 condition ? a : b
#   Python: if/elif/else, match/case(3.10+), 삼항 value_if_true if cond else value_if_false
# ============================================================================

# ── LEVEL 1: 기본 if/elif/else ───────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 기본 조건문")
print("=" * 50)

def grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

for s in [95, 83, 72, 61, 45]:
    print(f"  {s}점 → {grade(s)}")

# ── LEVEL 2: 삼항 표현식 ────────────────────────────────────────────────────

print("\nLEVEL 2: 삼항 표현식 (조건 표현식)")
print("-" * 40)

# Python 삼항: value_if_true if condition else value_if_false
# Java  삼항: condition ? value_if_true : value_if_false

x = 10
label = "양수" if x > 0 else "0 이하"
print(f"x={x}: {label}")

# 중첩 삼항 (가독성 주의 — 3단 이상은 함수로 분리 권장)
def classify(n):
    return "양수" if n > 0 else ("음수" if n < 0 else "영")

for n in [5, -3, 0]:
    print(f"  classify({n:3d}) = {classify(n)}")

# 삼항을 리스트 컴프리헨션과 결합
nums = [-3, 0, 5, -1, 4]
abs_nums = [abs(n) if n < 0 else n for n in nums]
labels   = ["neg" if n < 0 else ("zero" if n == 0 else "pos") for n in nums]
print(f"\n절댓값: {abs_nums}")
print(f"레이블: {labels}")

# None 안전 접근
data = {"user": {"name": "Alice"}}
name = data["user"]["name"] if data and data.get("user") else "Unknown"
print(f"name = {name!r}")

# ── LEVEL 3: 딕셔너리 디스패치 — switch-case 대체 ───────────────────────────

print("\nLEVEL 3: 딕셔너리 디스패치 (switch-case 대체)")
print("-" * 40)

# 나쁜 방법: elif 연속
def get_day_bad(num):
    if   num == 1: return "월"
    elif num == 2: return "화"
    elif num == 3: return "수"
    elif num == 4: return "목"
    elif num == 5: return "금"
    elif num == 6: return "토"
    elif num == 7: return "일"
    else:          return "?"

# 좋은 방법: 딕셔너리
DAYS = {1:"월", 2:"화", 3:"수", 4:"목", 5:"금", 6:"토", 7:"일"}
def get_day(num):
    return DAYS.get(num, "?")

for i in [1, 3, 7, 9]:
    print(f"  day({i}) = {get_day(i)}")

# 함수 테이블 패턴 (Strategy 패턴)
def cmd_create(args): return f"생성: {args}"
def cmd_read(args):   return f"조회: {args}"
def cmd_update(args): return f"수정: {args}"
def cmd_delete(args): return f"삭제: {args}"

HANDLERS = {
    "create": cmd_create,
    "read":   cmd_read,
    "update": cmd_update,
    "delete": cmd_delete,
}

for cmd in ["read", "update", "invalid"]:
    handler = HANDLERS.get(cmd, lambda a: f"알 수 없는 명령: {cmd}")
    print(f"  {cmd!r:10} → {handler('id=1')}")

# ── LEVEL 4: 가드 클로즈 (Guard Clause) ─────────────────────────────────────

print("\nLEVEL 4: 가드 클로즈 패턴")
print("-" * 40)

# Bad: 깊은 중첩 (Arrow Anti-Pattern)
def process_order_bad(order):
    if order:
        if order.get("user_id"):
            if order.get("items"):
                if order.get("total", 0) > 0:
                    return f"처리완료: {order}"
                else:
                    return "금액 오류"
            else:
                return "상품 없음"
        else:
            return "사용자 없음"
    else:
        return "주문 없음"

# Good: 가드 클로즈로 평탄화 (조기 return)
def process_order(order):
    if not order:
        return "주문 없음"
    if not order.get("user_id"):
        return "사용자 없음"
    if not order.get("items"):
        return "상품 없음"
    if order.get("total", 0) <= 0:
        return "금액 오류"
    # 핵심 로직 — 들여쓰기 없이 깔끔
    return f"처리완료: order_id={order.get('id')}, total={order.get('total')}"

orders = [
    None,
    {},
    {"user_id": 1},
    {"user_id": 1, "items": []},
    {"user_id": 1, "items": [1], "total": -1},
    {"id": 101, "user_id": 1, "items": [1,2], "total": 50000},
]
for o in orders:
    print(f"  {str(o)[:40]:<42} → {process_order(o)}")

# ── LEVEL 4: 조건 최적화 패턴 ───────────────────────────────────────────────

print("\nLEVEL 4: 조건 최적화")
print("-" * 40)

# 패턴 1: 조기 반환으로 else 제거
def find_first_positive(nums):
    for n in nums:
        if n > 0:
            return n   # 찾으면 바로 반환
    return None        # else 없어도 됨

print(f"첫 양수: {find_first_positive([-1, -2, 3, 4])}")   # 3

# 패턴 2: in 연산자로 여러 값 비교
status = "active"
# Bad:  if status == "active" or status == "pending" or status == "review":
# Good:
if status in {"active", "pending", "review"}:   # set이 list보다 O(1) 탐색
    print(f"status={status!r}: 처리 가능")

# 패턴 3: 조건 압축
def is_valid_age(age):
    return isinstance(age, int) and 0 <= age <= 150

for age in [-1, 0, 25, 150, 151, "25", None]:
    print(f"  is_valid_age({age!r}): {is_valid_age(age)}")

# 패턴 4: any/all로 복합 조건 가독성 향상
def can_submit(user):
    conditions = [
        user.get("verified"),
        user.get("age", 0) >= 18,
        user.get("balance", 0) >= 0,
        not user.get("banned"),
    ]
    return all(conditions)

users = [
    {"verified": True,  "age": 25, "balance": 1000, "banned": False},
    {"verified": False, "age": 25, "balance": 1000, "banned": False},
    {"verified": True,  "age": 15, "balance": 1000, "banned": False},
    {"verified": True,  "age": 25, "balance": 1000, "banned": True},
]
for u in users:
    print(f"  can_submit: {can_submit(u)} | {u}")

# ── LEVEL 5: match/case (Python 3.10+) ──────────────────────────────────────

print("\nLEVEL 5: match/case (Python 3.10+)")
print("-" * 40)

import sys
if sys.version_info >= (3, 10):
    def handle_command(command):
        match command.split():
            case ["quit"]:
                return "종료"
            case ["go", direction] if direction in ("north","south","east","west"):
                return f"{direction} 방향으로 이동"
            case ["get", item]:
                return f"{item} 획득"
            case ["get", item, "from", container]:
                return f"{container}에서 {item} 획득"
            case ["drop", *items]:
                return f"버림: {items}"
            case _:
                return f"알 수 없는 명령: {command!r}"

    for cmd in ["go north", "get sword", "get key from chest",
                "drop sword shield", "quit", "fly"]:
        print(f"  {cmd!r:<30} → {handle_command(cmd)}")
else:
    print(f"  Python {sys.version_info[:2]} — match/case는 3.10+에서 지원")

# ============================================================================
# [주의사항]
#   1. elif 연속 6개 이상 → 딕셔너리 or match/case 고려
#   2. 중첩 3단 이상 → 가드 클로즈 또는 함수 분리
#   3. 삼항 중첩 → 가독성 급감, 함수로 분리
#   4. 딕셔너리 값이 함수일 때: HANDLERS[cmd] 호출 시 키 없으면 KeyError
#      → .get(cmd, default_handler) 사용
#
# [다음 단계]
#   → 014_for.py: for 루프 — 이터러블 프로토콜과 활용 패턴
# ============================================================================
