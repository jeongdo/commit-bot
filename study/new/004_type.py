"""
004: type() 함수와 isinstance()를 활용한 타입 검증
"""

print("=== 1. type() 기본 사용 ===")
print(type(100))          # <class 'int'>
print(type([1, 2, 3]))    # <class 'list'>

print("\n=== 2. isinstance() 활용 (실무 권장) ===")
# 상속 관계까지 고려하여 더 안전하게 타입을 검사합니다.
number = 42

# 튜플로 여러 타입을 동시에 검사할 수 있습니다.
if isinstance(number, (int, float)):
    print(f"{number}는 숫자형 데이터입니다.")

print(isinstance("테스트", str))  # True