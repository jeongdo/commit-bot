"""
002: variables (변수)와 메모리 참조 개념
파이썬의 변수는 '값을 담는 상자'가 아니라 '객체에 붙이는 이름표(포스트잇)'입니다.
"""

print("=== 1. 기본 및 다중 할당 ===")
user_name = "Alice"
x, y, z = 10, 20, 30
score1 = score2 = 100

print("\n=== 2. 변수 값 교환 (Swap) ===")
a, b = 5, 10
a, b = b, a  # 임시 변수 없이 바로 교환
print(f"교환 후 -> a: {a}, b: {b}")

print("\n=== 3. [심화] 변수는 이름표다 (메모리 참조) ===")
list_a = [1, 2, 3]
list_b = list_a      # 복사가 아니라, 같은 리스트 객체에 이름표를 하나 더 붙임

list_b[0] = 99       # b를 통해 원본 객체를 수정
print(f"list_a: {list_a}") # [99, 2, 3] -> a도 변경되어 있음!

# id() 함수로 메모리 주소 확인 (완전히 동일함)
print(f"list_a의 주소: {id(list_a)}, list_b의 주소: {id(list_b)}")