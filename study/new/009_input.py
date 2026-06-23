"""
009: input (입력)
반환값은 항상 문자열(str)이므로 계산 시 형변환이 필수입니다.
"""

print("=== 1. 기본 입력 및 형변환 ===")
# 실제 사용 시: str_val = input("숫자를 입력하세요: ")
str_val = "50"
num = int(str_val)
print(f"입력값의 2배: {num * 2}")

print("\n=== 2. 한 번에 여러 값 입력받기 (split) ===")
# 실제 사용 시: user_input = input("두 숫자를 공백으로 띄워 입력: ")
user_input = "10 20"

# 공백 기준으로 쪼개서 각각 변수에 할당
a_str, b_str = user_input.split()
print(f"합계: {int(a_str) + int(b_str)}")

# (참고) map을 사용한 우아한 방식
x, y = map(int, user_input.split())