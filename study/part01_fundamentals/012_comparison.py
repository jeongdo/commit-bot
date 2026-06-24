# ============================================================================
# 012 - comparison (비교 심화)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. Python 비교 연산자의 내부 동작 (__eq__, __lt__ 등)을 이해한다
#   2. @total_ordering으로 완전한 정렬 가능 객체를 구현한다
#   3. __eq__ 재정의 시 __hash__도 함께 정의해야 하는 이유를 안다
#   4. 다중 키 정렬의 모든 패턴을 익힌다
#
# [왜 필요한가]
#   - 사용자 정의 클래스를 sorted(), max(), min()에서 사용하려면 비교 메서드 필요
#   - __eq__만 정의하고 __hash__ 안 하면 dict 키/set 원소 불가
#   - @total_ordering 없이 6개 메서드 모두 구현하는 실수 방지
#
# [Java 비교]
#   Java  : Comparable<T> 인터페이스 — compareTo() 구현
#           Comparator<T> 인터페이스 — compare() 구현
#   Python: __lt__, __le__, __eq__, __ge__, __gt__ + @total_ordering
#           functools.cmp_to_key()로 Java식 비교 함수 변환
# ============================================================================

from functools import total_ordering, cmp_to_key
import operator

# ── LEVEL 1: 기본 비교 ──────────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 기본 비교")
print("=" * 50)

# 숫자 비교 — 자명
print(f"3 < 5:     {3 < 5}")
print(f"3 > 5:     {3 > 5}")
print(f"5 >= 5:    {5 >= 5}")

# 문자열 — 사전순 (유니코드 코드포인트)
print(f"\n문자열 비교 (사전순):")
print(f"'apple' < 'banana': {'apple' < 'banana'}")     # True
print(f"'B' < 'a':          {'B' < 'a'}")              # True (대문자 < 소문자)
print(f"'가' < '나':        {'가' < '나'}")             # True (유니코드 순)

# 리스트/튜플 — 원소별 비교 (첫 번째 다른 원소 기준)
print(f"\n리스트/튜플 비교:")
print(f"[1,2,3] < [1,2,4]: {[1,2,3] < [1,2,4]}")      # True
print(f"[1,3] > [1,2,9]:   {[1,3] > [1,2,9]}")        # True (두 번째 원소 비교)
print(f"(1,2) == (1,2):    {(1,2) == (1,2)}")         # True

# None 비교: == 만 가능, < > 불가
print(f"\nNone == None: {None == None}")   # True
print(f"None is None: {None is None}")      # True

# ── LEVEL 2: @total_ordering — 정렬 가능 클래스 ─────────────────────────────

print("\nLEVEL 2: @total_ordering")
print("-" * 40)

@total_ordering
class Temperature:
    """온도 비교 — @total_ordering으로 __eq__ + __lt__ 만으로 모두 구현"""

    UNITS = ("C", "F", "K")

    def __init__(self, value, unit="C"):
        if unit not in self.UNITS:
            raise ValueError(f"단위는 {self.UNITS} 중 하나")
        self.value = value
        self.unit  = unit

    def to_celsius(self):
        if self.unit == "C": return self.value
        if self.unit == "F": return (self.value - 32) * 5 / 9
        if self.unit == "K": return self.value - 273.15

    def __eq__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return abs(self.to_celsius() - other.to_celsius()) < 1e-9

    def __lt__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_celsius() < other.to_celsius()

    def __repr__(self):
        return f"{self.value}{self.unit}"

# __le__, __gt__, __ge__는 @total_ordering이 자동 생성
temps = [
    Temperature(100, "C"),
    Temperature(0, "C"),
    Temperature(37, "C"),
    Temperature(212, "F"),   # = 100C
    Temperature(373.15, "K"), # = 100C
]

print("온도 비교:")
t_c = Temperature(37, "C")
t_f = Temperature(98.6, "F")  # = 37C
print(f"  37°C == 98.6°F: {t_c == t_f}")    # True
print(f"  37°C <  100°C : {t_c < Temperature(100,'C')}")  # True
print(f"  37°C >  0°C   : {t_c > Temperature(0,'C')}")    # True (자동!)
print(f"  37°C >= 37°C  : {t_c >= t_f}")    # True (자동!)

print(f"\n정렬:")
sorted_temps = sorted(temps)
for t in sorted_temps:
    print(f"  {t!r:12} ({t.to_celsius():.2f}°C)")

print(f"최고온도: {max(temps)}")
print(f"최저온도: {min(temps)}")

# ── LEVEL 3: __eq__와 __hash__의 관계 ────────────────────────────────────────

print("\nLEVEL 3: __eq__와 __hash__ 관계")
print("-" * 40)

# __eq__를 정의하면 __hash__는 자동으로 None이 됨
class BadPoint:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    # __hash__ 없음!

p1 = BadPoint(1, 2)
p2 = BadPoint(1, 2)
print(f"BadPoint: p1 == p2 = {p1 == p2}")     # True
try:
    s = {p1, p2}   # TypeError: unhashable type
    print(f"set 가능: {s}")
except TypeError as e:
    print(f"set 불가: {e}")

# __hash__도 함께 구현 (올바른 방법)
class GoodPoint:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        if not isinstance(other, GoodPoint):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        # 불변 속성을 튜플로 묶어 해시 → (x, y)가 같으면 해시도 같음
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p1 = GoodPoint(1, 2)
p2 = GoodPoint(1, 2)
p3 = GoodPoint(3, 4)

print(f"\nGoodPoint: p1 == p2 = {p1 == p2}")   # True
print(f"set: {{{p1}, {p2}, {p3}}}")             # {Point(1,2), Point(3,4)} — 중복 제거
print(f"dict 키: {{ p1: 'origin' }}: { {p1: 'P1', p3: 'P3'}[p2] }")  # 'P1' (같은 해시)

# ── LEVEL 4: 다중 키 정렬 ────────────────────────────────────────────────────

print("\nLEVEL 4: 다중 키 정렬 패턴")
print("-" * 40)

students = [
    {"name": "Alice",  "grade": "A", "score": 92, "age": 30},
    {"name": "Bob",    "grade": "B", "score": 85, "age": 25},
    {"name": "Carol",  "grade": "A", "score": 88, "age": 28},
    {"name": "Dave",   "grade": "B", "score": 92, "age": 22},
    {"name": "Eve",    "grade": "A", "score": 92, "age": 25},
]

# 단일 키
by_score = sorted(students, key=lambda s: s["score"], reverse=True)
print("점수 내림차순:")
for s in by_score:
    print(f"  {s['name']:<8} {s['grade']} {s['score']}")

# 다중 키: 등급 오름차순 + 점수 내림차순
by_grade_score = sorted(students,
    key=lambda s: (s["grade"], -s["score"]))
print("\n등급↑ + 점수↓:")
for s in by_grade_score:
    print(f"  {s['name']:<8} {s['grade']} {s['score']}")

# operator.itemgetter — lambda보다 빠름
by_age = sorted(students, key=operator.itemgetter("age"))
print(f"\n나이 오름차순: {[s['name'] for s in by_age]}")

# ── LEVEL 5: cmp_to_key — Java식 compare 함수 변환 ──────────────────────────

print("\nLEVEL 5: cmp_to_key (Java style compareTo)")
print("-" * 40)

# Java: compareTo() 반환 < 0: 앞, 0: 같음, > 0: 뒤
def version_compare(v1, v2):
    """버전 문자열 비교 (예: '1.10.2' vs '1.9.1')"""
    parts1 = list(map(int, v1.split(".")))
    parts2 = list(map(int, v2.split(".")))
    # 길이 맞추기
    max_len = max(len(parts1), len(parts2))
    parts1 += [0] * (max_len - len(parts1))
    parts2 += [0] * (max_len - len(parts2))

    for a, b in zip(parts1, parts2):
        if a < b: return -1
        if a > b: return  1
    return 0

versions = ["1.9.1", "1.10.2", "2.0.0", "1.9.10", "1.10.0"]
sorted_versions = sorted(versions, key=cmp_to_key(version_compare))
print(f"버전 정렬: {sorted_versions}")
# ['1.9.1', '1.9.10', '1.10.0', '1.10.2', '2.0.0']
# 단순 문자열 정렬은 '1.10.0' < '1.9.1' (틀림!)
print(f"문자열 정렬 (틀림): {sorted(versions)}")

# ============================================================================
# [주의사항]
#   1. @total_ordering: __eq__ + (__lt__ 중 하나) 만 필요 — 나머지 자동
#   2. NotImplemented 반환: 비교 불가 타입 대응 — None 반환과 다름
#   3. __eq__ 재정의 시 반드시 __hash__도 정의 (불변 속성 기반)
#   4. 가변 객체(list 등)은 __hash__ 구현 금지 (값이 바뀌면 해시 무효)
#   5. cmp_to_key: Python 3에서 cmp 함수가 제거됨 → 이 래퍼 사용
#
# [다음 단계]
#   → 013_if.py: 조건문 — 가드 클로즈, 딕셔너리 디스패치
# ============================================================================
