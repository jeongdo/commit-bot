# ============================================================================
# 003 - data_type (데이터 타입)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. Python 내장 타입 전체를 조감한다
#   2. type() vs isinstance() 차이를 완전히 이해한다
#   3. 타입 변환(형변환)의 성공/실패 패턴을 안다
#   4. Falsy/Truthy 규칙을 완전히 암기한다
#
# [왜 필요한가]
#   - Python은 "모든 것이 객체" — 타입 = 클래스
#   - 동적 타이핑 언어에서 타입 체크는 개발자 책임
#   - 잘못된 타입 → TypeError, ValueError 런타임 오류
#
# [Java 비교]
#   Java  : int, long, double, char, boolean (primitive)
#           Integer, Long, Double (Wrapper class)
#   Python: 모두 객체. primitive 없음
#           int → 무제한 정밀도, bool → int 서브클래스
#
# [실무 사용 사례]
#   - API 응답 검증: isinstance(data, dict)
#   - 타입 안전 변환: safe_int(value, default=0)
#   - 다형성 처리: isinstance(x, (list, tuple))
# ============================================================================

import sys

# ── LEVEL 1: Python 내장 타입 전체 ──────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 내장 타입 전체")
print("=" * 50)

# 숫자형
i  = 42             # int   — 무제한 정밀도 (오버플로우 없음!)
f  = 3.14           # float — IEEE 754 배정밀도
c  = 2 + 3j         # complex — 복소수
b  = True           # bool  — int 서브클래스 (True==1, False==0)

# 텍스트
s  = "hello"        # str   — 유니코드, 불변

# 이진
bs = b"bytes"       # bytes — 불변 바이트 시퀀스
ba = bytearray(b"mutable")  # bytearray — 가변 바이트

# 컨테이너
lst = [1, 2, 3]              # list   — 가변, 순서 O
tup = (1, 2, 3)              # tuple  — 불변, 순서 O
st  = {1, 2, 3}              # set    — 가변, 순서 X, 중복 X
fs  = frozenset({1, 2})      # frozenset — 불변 set
dct = {"a": 1, "b": 2}      # dict   — 가변, Python3.7+ 순서 보장

# 특수
n  = None                    # NoneType — 싱글톤

for name, obj in [("int",i),("float",f),("complex",c),("bool",b),
                  ("str",s),("bytes",bs),("list",lst),("tuple",tup),
                  ("set",st),("dict",dct),("None",n)]:
    print(f"  {name:<12}: {type(obj).__name__:<12} | {repr(obj)}")

# ── LEVEL 2: type() vs isinstance() ─────────────────────────────────────────

print("\nLEVEL 2: type() vs isinstance()")
print("-" * 40)

# type(): 정확한 클래스만 (상속 미고려)
print(f"type(True) == bool : {type(True) == bool}")   # True
print(f"type(True) == int  : {type(True) == int}")    # False! (bool은 int 서브클래스)

# isinstance(): 상속 고려 (권장)
print(f"isinstance(True, bool): {isinstance(True, bool)}")  # True
print(f"isinstance(True, int) : {isinstance(True, int)}")   # True ← 상속 반영

# 여러 타입 동시 체크
data = 3.14
print(f"isinstance(3.14, (int, float)): {isinstance(data, (int, float))}")  # True

# ── LEVEL 2: 타입 변환 (형변환) ──────────────────────────────────────────────

print("\nLEVEL 2: 타입 변환")
print("-" * 40)

# 성공 케이스
print(f"int('42')      = {int('42')}")        # 42
print(f"int(3.9)       = {int(3.9)}")         # 3 (버림! 반올림 아님)
print(f"int(True)      = {int(True)}")        # 1
print(f"float('3.14')  = {float('3.14')}")    # 3.14
print(f"str(100)       = {str(100)!r}")       # '100'
print(f"bool(0)        = {bool(0)}")          # False
print(f"bool('hello')  = {bool('hello')}")    # True
print(f"list('abc')    = {list('abc')}")      # ['a','b','c']
print(f"tuple([1,2,3]) = {tuple([1,2,3])}")   # (1,2,3)
print(f"set([1,2,2,3]) = {set([1,2,2,3])}")   # {1,2,3}

# 실패 케이스
conversions = [
    ("int('abc')",   int, "abc"),
    ("int('3.14')",  int, "3.14"),   # float str은 int() 직접 불가
    ("float('abc')", float, "abc"),
]
for expr, func, val in conversions:
    try:
        result = func(val)
        print(f"{expr} = {result}")
    except (ValueError, TypeError) as e:
        print(f"{expr} → {type(e).__name__}: {e}")

# ── LEVEL 3: Falsy / Truthy — Python의 핵심 ──────────────────────────────────

print("\nLEVEL 3: Falsy / Truthy 규칙")
print("-" * 40)

# Falsy 값 (bool() → False가 되는 값들)
falsy_values = [
    (False,     "bool False"),
    (0,         "int 0"),
    (0.0,       "float 0.0"),
    (0j,        "complex 0j"),
    ("",        "빈 문자열"),
    ([],        "빈 리스트"),
    ((),        "빈 튜플"),
    ({},        "빈 딕셔너리"),
    (set(),     "빈 집합"),
    (None,      "None"),
]
print("  Falsy 값:")
for val, desc in falsy_values:
    assert not bool(val), f"{val!r} should be falsy"
    print(f"    bool({val!r:<12}) = False  ({desc})")

# Truthy 값 (나머지 모든 값)
truthy_values = [True, 1, -1, 0.001, "0", " ", [0], (False,), {"key":0}]
print(f"  Truthy 예시: {truthy_values}")

# ── LEVEL 3: 타입 계층 구조 ─────────────────────────────────────────────────

print("\nLEVEL 3: 타입 계층 구조")
print("-" * 40)

# Python 타입 계층: object → int → bool
print(f"bool.__bases__   = {bool.__bases__}")    # (<class 'int'>,)
print(f"int.__bases__    = {int.__bases__}")     # (<class 'object'>,)
print(f"type(bool)       = {type(bool)}")        # <class 'type'>
print(f"type(type)       = {type(type)}")        # <class 'type'> (자기 자신!)

# 모든 것은 object의 인스턴스
for obj in [42, "hi", [], None, print, int]:
    print(f"  isinstance({repr(obj):<10}, object) = {isinstance(obj, object)}")

# ── LEVEL 4: 실무 패턴 ───────────────────────────────────────────────────────

print("\nLEVEL 4: 실무 패턴")
print("-" * 40)

# 패턴 1: 안전한 타입 변환 함수
def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

print(f"safe_int('42')   = {safe_int('42')}")    # 42
print(f"safe_int('abc')  = {safe_int('abc')}")   # 0
print(f"safe_int(None)   = {safe_int(None)}")    # 0
print(f"safe_float('3x') = {safe_float('3x')}")  # 0.0

# 패턴 2: 다형성 처리 (여러 타입 수용)
def flatten(data):
    """리스트/튜플을 재귀적으로 평탄화"""
    result = []
    for item in data:
        if isinstance(item, (list, tuple)):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

nested = [1, [2, 3, [4, 5]], (6, [7, 8])]
print(f"flatten({nested}) = {flatten(nested)}")

# 패턴 3: JSON 역직렬화 후 타입 검증
import json

raw = '{"name": "Alice", "age": 30, "scores": [90, 85, 92]}'
data = json.loads(raw)

assert isinstance(data, dict), "최상위는 dict여야 함"
assert isinstance(data["name"], str), "name은 str이어야 함"
assert isinstance(data["age"], int), "age는 int여야 함"
assert isinstance(data["scores"], list), "scores는 list여야 함"
print(f"JSON 검증 통과: {data}")

# ── LEVEL 5: 오픈소스 패턴 ──────────────────────────────────────────────────

print("\nLEVEL 5: 오픈소스 패턴")
print("-" * 40)

# Django ORM, SQLAlchemy 등에서 자주 보이는 타입 디스패치 패턴
from functools import singledispatch

@singledispatch
def serialize(obj):
    raise TypeError(f"직렬화 불가: {type(obj).__name__}")

@serialize.register(int)
@serialize.register(float)
def _(obj):
    return obj

@serialize.register(str)
def _(obj):
    return obj

@serialize.register(list)
def _(obj):
    return [serialize(item) for item in obj]

@serialize.register(dict)
def _(obj):
    return {k: serialize(v) for k, v in obj.items()}

data = {"nums": [1, 2.5, 3], "text": "hello", "nested": {"x": 1}}
print(f"serialize: {serialize(data)}")

# ============================================================================
# [주의사항]
#   1. int("3.14") → ValueError: float str은 int()에 직접 못 넣음
#      → int(float("3.14")) 으로 2단계 변환
#   2. bool은 int 서브클래스 → True+True=2, sum([True,False,True])=2
#   3. type(x) == int 보다 isinstance(x, int) 권장 (상속 고려)
#   4. 빈 컬렉션 모두 Falsy → if data: 로 간결하게 체크 가능
#
# [다음 단계]
#   → 004_type.py: type() 심화 — 동적 클래스 생성과 메타클래스 입문
# ============================================================================
