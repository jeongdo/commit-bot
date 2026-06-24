# ============================================================================
# 004 - type() 심화
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. type()의 두 가지 역할을 완전히 이해한다
#      - 역할 1: type(obj)  → 객체의 타입(클래스) 반환
#      - 역할 2: type(name, bases, dict) → 동적 클래스 생성
#   2. Python 타입 시스템의 계층 구조를 파악한다
#   3. MRO(Method Resolution Order) 기초를 안다
#
# [왜 필요한가]
#   - type()은 Python 메타프로그래밍의 출발점
#   - Django ORM, SQLAlchemy 모델은 메타클래스로 구현됨
#   - PART 19 메타프로그래밍 심화의 필수 기반
#
# [Java 비교]
#   Java  : obj.getClass()               → Class 객체 반환
#           Class.forName("ClassName")   → 동적 클래스 로드
#   Python: type(obj)                    → 클래스 반환
#           type("Name", (Base,), {...}) → 런타임 클래스 생성
# ============================================================================

# ── LEVEL 1: type() 역할 1 — 타입 조회 ──────────────────────────────────────

print("=" * 50)
print("LEVEL 1: type() 타입 조회")
print("=" * 50)

samples = [42, 3.14, "hello", [1,2], (1,2), {1,2}, {"a":1}, True, None]
for obj in samples:
    t = type(obj)
    print(f"  type({repr(obj):<15}) = {t}")

# type()으로 타입 비교 (정확히 해당 클래스인지)
print(f"\ntype(True) is bool : {type(True) is bool}")    # True
print(f"type(True) is int  : {type(True) is int}")       # False (isinstance와 차이!)

# ── LEVEL 2: type() 역할 2 — 동적 클래스 생성 ───────────────────────────────

print("\nLEVEL 2: type()로 클래스 동적 생성")
print("-" * 40)

# type(이름, (부모클래스,...), {속성딕셔너리})
# 아래 두 코드는 완전히 동일

# 방법 A: 일반 class 정의
class PointA:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# 방법 B: type()으로 동적 생성 (완전히 동일한 결과!)
def point_init(self, x, y):
    self.x = x
    self.y = y

def point_distance(self):
    return (self.x ** 2 + self.y ** 2) ** 0.5

def point_repr(self):
    return f"Point({self.x}, {self.y})"

PointB = type("PointB", (object,), {
    "__init__": point_init,
    "distance": point_distance,
    "__repr__": point_repr,
    "origin":   (0, 0),     # 클래스 변수
})

pa = PointA(3, 4)
pb = PointB(3, 4)
print(f"PointA: {pa}, distance={pa.distance()}")
print(f"PointB: {pb}, distance={pb.distance()}")
print(f"같은 동작? {pa.distance() == pb.distance()}")

# ── LEVEL 2: __name__, __qualname__, __bases__, __dict__ ────────────────────

print("\nLEVEL 2: 클래스 메타데이터 속성")
print("-" * 40)

class Outer:
    class Inner:
        pass

print(f"Outer.__name__     = {Outer.__name__}")
print(f"Inner.__qualname__ = {Outer.Inner.__qualname__}")  # Outer.Inner
print(f"Outer.__bases__    = {Outer.__bases__}")           # (object,)
print(f"Outer.__module__   = {Outer.__module__}")

obj = Outer.Inner()
print(f"obj.__class__      = {obj.__class__}")
print(f"obj.__class__.__name__ = {obj.__class__.__name__}")

# ── LEVEL 3: 타입 계층 — type이 type의 인스턴스 ──────────────────────────────

print("\nLEVEL 3: Python 타입 계층 구조")
print("-" * 40)

#  object  ← 모든 클래스의 최상위
#    └── int, str, list, dict, ...
#    └── type    ← 모든 클래스(타입)의 타입
#         └── type(type) == type  (자기 자신!)

print(f"type(int)      = {type(int)}")       # <class 'type'>
print(f"type(str)      = {type(str)}")       # <class 'type'>
print(f"type(type)     = {type(type)}")      # <class 'type'> ← 재귀!
print(f"type(object)   = {type(object)}")    # <class 'type'>

print(f"\nisinstance(int, type)    = {isinstance(int, type)}")     # True
print(f"isinstance(int, object)  = {isinstance(int, object)}")    # True
print(f"issubclass(int, object)  = {issubclass(int, object)}")    # True
print(f"issubclass(type, object) = {issubclass(type, object)}")   # True

# ── LEVEL 3: MRO (Method Resolution Order) ──────────────────────────────────

print("\nLEVEL 3: MRO — C3 선형화")
print("-" * 40)

class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass   # 다중 상속

print("D의 MRO:")
for i, cls in enumerate(D.__mro__):
    print(f"  {i}: {cls}")
# D → B → C → A → object (C3 선형화 알고리즘)

# 실무적 의미: 메서드 탐색 순서
class Base:
    def greet(self): return "Base.greet"

class Left(Base):
    def greet(self): return "Left.greet"

class Right(Base):
    pass  # greet 미정의

class Child(Left, Right):
    pass

c = Child()
print(f"Child().greet() = {c.greet()!r}")  # Left.greet (MRO 순서)

# ── LEVEL 4: 실무 패턴 — 동적 클래스 생성 활용 ──────────────────────────────

print("\nLEVEL 4: 동적 클래스 생성 활용")
print("-" * 40)

# 패턴: 설정 기반 모델 동적 생성 (ORM에서 사용하는 방식)
def create_model(name, fields):
    """fields: {"field_name": default_value} 딕셔너리"""

    def init(self, **kwargs):
        for field, default in fields.items():
            setattr(self, field, kwargs.get(field, default))

    def repr_(self):
        attrs = ", ".join(f"{k}={getattr(self, k)!r}" for k in fields)
        return f"{self.__class__.__name__}({attrs})"

    return type(name, (object,), {
        "__init__": init,
        "__repr__": repr_,
        "_fields":  list(fields.keys()),
    })

# 런타임에 모델 클래스 생성
User    = create_model("User",    {"id": None, "name": "", "email": ""})
Product = create_model("Product", {"id": None, "name": "", "price": 0.0})

u = User(id=1, name="Alice", email="alice@example.com")
p = Product(id=1, name="Laptop", price=1299.99)
print(f"User   : {u}")
print(f"Product: {p}")
print(f"User fields: {u._fields}")

# ── LEVEL 5: 오픈소스 패턴 — namedtuple 내부 구현 방식 ──────────────────────

print("\nLEVEL 5: namedtuple 내부 방식 재현")
print("-" * 40)

def simple_namedtuple(typename, field_names):
    """collections.namedtuple의 단순화 버전"""
    if isinstance(field_names, str):
        field_names = field_names.replace(",", " ").split()

    def __init__(self, *args):
        for name, val in zip(field_names, args):
            object.__setattr__(self, name, val)

    def __repr__(self):
        vals = ", ".join(f"{n}={getattr(self, n)!r}" for n in field_names)
        return f"{typename}({vals})"

    def __setattr__(self, name, value):
        raise AttributeError("불변 객체: 수정 불가")

    ns = {
        "__init__":    __init__,
        "__repr__":    __repr__,
        "__setattr__": __setattr__,
    }
    for name in field_names:
        ns[name] = property(lambda self, n=name: object.__getattribute__(self, n))

    return type(typename, (object,), ns)

Point = simple_namedtuple("Point", "x y z")
p = Point(1, 2, 3)
print(f"Point: {p}")
print(f"x={p.x}, y={p.y}, z={p.z}")
try:
    p.x = 99
except AttributeError as e:
    print(f"수정 시도: {e}")

# ============================================================================
# [주의사항]
#   1. type(name, bases, dict) 에서 bases는 반드시 튜플 — (object,) 쉼표 주의
#   2. __mro__ 직접 수정 불가 — C3 알고리즘으로 자동 계산
#   3. 동적 클래스 생성 남용은 가독성/디버깅 어려움 → 필요한 경우만
#
# [다음 단계]
#   → 005_bool.py: Boolean 타입 — int 서브클래스, 단락 평가
# ============================================================================
