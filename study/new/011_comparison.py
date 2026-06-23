"""
011: comparison (비교 연산자)
값 비교(==)와 식별 비교(is)의 명확한 차이를 다룹니다.
"""

print("=== 1. 비교 연산자 체이닝 ===")
# 파이썬은 수학 기호처럼 연속해서 쓸 수 있습니다.
age = 25
print(f"20대인가요? (20 <= age < 30) : {20 <= age < 30}")

print("\n=== 2. [심화] 값 비교(==) vs 객체 식별(is) ===")
# == : 두 객체의 '값(내용물)'이 같은지 비교
# is : 두 객체가 메모리상 '완전히 동일한 객체'인지 비교
list1 = [1, 2, 3]
list2 = [1, 2, 3]
list3 = list1

print(f"list1 == list2 : {list1 == list2}") # True (내용물 같음)
print(f"list1 is list2 : {list1 is list2}") # False (다른 메모리 객체)
print(f"list1 is list3 : {list1 is list3}") # True (같은 메모리 객체)

print("\n=== 3. [심화] 정수 캐싱과 None 비교 ===")
# -5 ~ 256 까지의 자주 쓰이는 정수는 파이썬이 미리 만들어두고 공유함
x, y = 100, 100
print(f"100 is 100 : {x is y}") # True

# None은 시스템 전체에 1개뿐인 싱글톤이므로 무조건 'is'로 비교 (PEP 8 규약)
my_val = None
if my_val is None:
    print("my_val은 안전하게 None으로 판별되었습니다.")