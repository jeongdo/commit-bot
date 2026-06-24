# ============================================================================
# 011 - operator (연산자 완전 정복)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. Python의 모든 연산자와 우선순위를 이해한다
#   2. 체이닝 비교 (1 < x < 10) 를 활용한다
#   3. operator 모듈로 연산자를 함수로 사용하는 패턴을 익힌다
#   4. 연산자 오버로딩의 개념을 미리 파악한다
#
# [Java 비교]
#   Java  : ==는 참조 비교(객체) / 값 비교(primitive)
#           비교 체이닝 불가: 1 < x && x < 10 필요
#   Python: ==는 항상 값 비교 (__eq__ 호출)
#           비교 체이닝 가능: 1 < x < 10
# ============================================================================

import operator
from functools import reduce

# ── LEVEL 1: 산술 연산자 ─────────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 산술 / 비교 / 논리 연산자")
print("=" * 50)

a, b = 17, 5
print(f"a={a}, b={b}")
print(f"  +  : {a + b}")       # 22
print(f"  -  : {a - b}")       # 12
print(f"  *  : {a * b}")       # 85
print(f"  /  : {a / b}")       # 3.4  (항상 float!)
print(f"  // : {a // b}")      # 3    (정수 나눗셈, floor)
print(f"  %  : {a % b}")       # 2    (나머지)
print(f"  ** : {a ** b}")      # 1419857
print(f"  -a : {-a}")          # -17  (단항 음수)

# 문자열/리스트에서의 산술 연산자
print(f"\n문자열: 'A' * 5 = {'A' * 5}")
print(f"리스트: [0] * 3  = {[0] * 3}")
print(f"문자열: 'ab'+'cd' = {'ab'+'cd'}")
print(f"리스트: [1,2]+[3,4] = {[1,2]+[3,4]}")

# ── LEVEL 1: 비교 연산자 ─────────────────────────────────────────────────────

print("\n비교 연산자:")
x = 5
print(f"  x=={x}: x==5={x==5}, x!=5={x!=5}")
print(f"  x=={x}: x>3={x>3},   x<10={x<10}")
print(f"  x=={x}: x>=5={x>=5}, x<=5={x<=5}")

# Python 체이닝 비교 (Java 불가!)
print(f"\n체이닝 비교 (Python만 가능!):")
print(f"  1 < x < 10  = {1 < x < 10}")      # True
print(f"  0 < x < 5   = {0 < x < 5}")       # False (5는 5 미만 아님)
print(f"  0 < x <= 5  = {0 < x <= 5}")      # True
print(f"  1 < 3 < 5 < 10 = {1 < 3 < 5 < 10}") # True (여러 개 가능)
print(f"  # Java: 0 < x && x < 10 처럼 써야 함")

# ── LEVEL 2: 멤버십 / 동일성 연산자 ─────────────────────────────────────────

print("\nLEVEL 2: 멤버십 / 동일성 연산자")
print("-" * 40)

# in / not in
fruits = ["apple", "banana", "cherry"]
print(f"'apple' in fruits      = {'apple' in fruits}")      # True
print(f"'grape' not in fruits  = {'grape' not in fruits}")  # True

# 딕셔너리: in은 키 체크
d = {"a": 1, "b": 2}
print(f"'a' in dict            = {'a' in d}")               # True
print(f"1 in dict.values()     = {1 in d.values()}")        # True

# 문자열: in은 부분 문자열
print(f"'ello' in 'hello'      = {'ello' in 'hello'}")      # True

# is / is not (동일 객체 비교)
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(f"\na == b  = {a == b}")    # True  (값 같음)
print(f"a is b  = {a is b}")      # False (다른 객체)
print(f"a is c  = {a is c}")      # True  (같은 객체)

# None은 반드시 is / is not
result = None
print(f"\nresult is None     = {result is None}")     # True  ✓
print(f"result is not None = {result is not None}") # False ✓
# print(f"result == None  = {result == None}")   # 작동하나 비권장

# ── LEVEL 3: 비트 연산자 ─────────────────────────────────────────────────────

print("\nLEVEL 3: 비트 연산자")
print("-" * 40)

a, b = 0b1010, 0b1100   # 10, 12
print(f"a = {a:4d} ({bin(a)})")
print(f"b = {b:4d} ({bin(b)})")

print(f"  a & b  = {a & b:4d} ({bin(a & b):<12}) # AND")
print(f"  a | b  = {a | b:4d} ({bin(a | b):<12}) # OR")
print(f"  a ^ b  = {a ^ b:4d} ({bin(a ^ b):<12}) # XOR")
print(f"  ~a     = {~a:4d} ({bin(~a):<12}) # NOT (2의 보수)")
print(f"  a << 2 = {a << 2:4d} ({bin(a<<2):<12}) # 왼쪽 시프트 (×4)")
print(f"  a >> 1 = {a >> 1:4d} ({bin(a>>1):<12}) # 오른쪽 시프트 (÷2)")

# ── LEVEL 3: 연산자 우선순위 ─────────────────────────────────────────────────

print("\nLEVEL 3: 연산자 우선순위 (높음 → 낮음)")
print("-" * 40)
print("  ()           괄호")
print("  **           거듭제곱 (오른쪽 결합!)")
print("  +x, -x, ~x  단항 연산")
print("  *, /, //, %  곱셈/나눗셈")
print("  +, -         덧셈/뺄셈")
print("  <<, >>       비트 시프트")
print("  &            비트 AND")
print("  ^            비트 XOR")
print("  |            비트 OR")
print("  in, not in, is, is not, <, <=, >, >=, ==, !=  비교")
print("  not          논리 NOT")
print("  and          논리 AND")
print("  or           논리 OR")

# 우선순위 예시
print(f"\n우선순위 예시:")
print(f"  2 + 3 * 4       = {2 + 3 * 4}")       # 14 (*우선)
print(f"  (2 + 3) * 4     = {(2 + 3) * 4}")     # 20
print(f"  2 ** 3 ** 2     = {2 ** 3 ** 2}")     # 512 (3**2=9, 2**9=512, 오른쪽부터!)
print(f"  (2 ** 3) ** 2   = {(2 ** 3) ** 2}")   # 64
print(f"  not 1 == 1      = {not 1 == 1}")       # False (==가 not보다 우선)
print(f"  (not 1) == 1    = {(not 1) == 1}")     # False

# ── LEVEL 4: operator 모듈 ───────────────────────────────────────────────────

print("\nLEVEL 4: operator 모듈 — 연산자를 함수로")
print("-" * 40)

# 연산자를 인수로 전달할 때 operator 모듈 사용
nums = [3, 1, 4, 1, 5, 9, 2, 6]

# reduce로 누적 연산
print(f"합계 : {reduce(operator.add, nums)}")      # 31
print(f"곱셈 : {reduce(operator.mul, [1,2,3,4,5])}") # 120
print(f"최댓값: {reduce(operator.gt, nums)}")      # 오류처럼 보이지만 비교 반환

# 정렬용 키 함수
records = [
    {"name": "Alice", "score": 92, "age": 30},
    {"name": "Bob",   "score": 85, "age": 25},
    {"name": "Carol", "score": 92, "age": 28},
]

# operator.itemgetter: lambda보다 빠르고 간결
by_score = sorted(records, key=operator.itemgetter("score"), reverse=True)
print(f"\n점수순: {[r['name'] for r in by_score]}")

# 다중 키 정렬
by_score_age = sorted(records, key=operator.itemgetter("score", "age"), reverse=True)
print(f"점수+나이: {[(r['name'],r['score'],r['age']) for r in by_score_age]}")

# operator.attrgetter: 객체 속성 접근
class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa
    def __repr__(self):
        return f"Student({self.name}, {self.gpa})"

students = [Student("Alice", 3.9), Student("Bob", 3.7), Student("Carol", 3.85)]
by_gpa = sorted(students, key=operator.attrgetter("gpa"), reverse=True)
print(f"\nGPA순: {[s.name for s in by_gpa]}")

# operator.methodcaller: 메서드 호출
words = ["hello", "WORLD", "Python"]
upper_words = list(map(operator.methodcaller("upper"), words))
print(f"대문자: {upper_words}")

# ── LEVEL 5: 연산자 오버로딩 예고 ────────────────────────────────────────────

print("\nLEVEL 5: 연산자 오버로딩 예고")
print("-" * 40)

class Vector:
    """2D 벡터 — 연산자 오버로딩 예시"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):      # +
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):      # -
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):     # v * scalar
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):    # scalar * v
        return self.__mul__(scalar)

    def __abs__(self):             # abs(v) = 길이
        return (self.x**2 + self.y**2) ** 0.5

    def __eq__(self, other):       # ==
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(f"v1 + v2   = {v1 + v2}")    # Vector(4, 6)
print(f"v1 - v2   = {v1 - v2}")    # Vector(-2, -2)
print(f"v1 * 3    = {v1 * 3}")     # Vector(3, 6)
print(f"2 * v1    = {2 * v1}")     # Vector(2, 4)
print(f"|v2|      = {abs(v2)}")    # 5.0
print(f"v1 == v1  = {v1 == v1}")   # True

# ============================================================================
# [주의사항]
#   1. ** 는 오른쪽 결합: 2**3**2 = 2**(3**2) = 512 (Java 연산자 없음)
#   2. is 는 동일성, == 는 동등성 — None/True/False만 is 사용
#   3. 체이닝 비교: 1 < x < 10 은 (1<x) and (x<10) 과 동일
#   4. 음수 //: -7//2=-4 (floor), Java -7/2=-3 (truncate)
#   5. operator 모듈은 lambda보다 빠름 (C 레벨 구현)
#
# [다음 단계]
#   → 012_comparison.py: 비교 심화 — __eq__, __hash__, total_ordering
# ============================================================================
