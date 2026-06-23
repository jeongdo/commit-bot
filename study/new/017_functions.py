"""
017 ~ 018: 함수(functions)와 매개변수(arguments)
코드를 모듈화하여 재사용성을 높입니다.
"""

print("=== 1. 기본 함수 정의와 호출 ===")
def greet(name):
    """이 함수는 이름을 받아 인사말을 반환합니다. (Docstring)"""
    return f"안녕하세요, {name}님!"

print(greet("개발자"))

print("\n=== 2. [심화] 여러 값을 반환하는 함수 (Tuple Packing) ===")
# 타 언어는 함수가 무조건 1개의 값만 반환하지만, 파이썬은 여러 개를 쉼표로 던질 수 있습니다.
# 사실 이는 여러 개를 반환하는 게 아니라, 하나의 '튜플(Tuple)'로 묶어서(Packing) 반환하는 것입니다.

def get_user_info():
    name = "Alice"
    age = 30
    return name, age  # 실제로는 (name, age) 라는 하나의 튜플이 반환됨

# 받을 때도 여러 변수로 쪼개서(Unpacking) 받을 수 있습니다.
user_name, user_age = get_user_info()
print(f"이름: {user_name}, 나이: {user_age}")

print("\n=== 3. 위치 인수(Positional)와 키워드 인수(Keyword) ===")
def divide(a, b):
    return a / b

print(f"위치 인수: {divide(10, 2)}")           # 순서대로 a=10, b=2
print(f"키워드 인수: {divide(b=2, a=10)}")     # 순서 상관없이 이름으로 지정 가능
# print(divide(b=2, 10)) # 오류 발생! 키워드 인수는 항상 위치 인수보다 뒤에 와야 합니다.