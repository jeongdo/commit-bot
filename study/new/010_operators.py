"""
010: operators (산술 및 대입 연산자)
"""

print("=== 1. 산술 연산자 (독특한 나눗셈) ===")
a, b = 15, 4
print(f"일반 나눗셈 (/): {a} / {b} = {a / b}")   # 항상 float 반환
print(f"몫 (//): {a} // {b} = {a // b}")       # 내림 처리
print(f"나머지 (%): {a} % {b} = {a % b}")
print(f"거듭제곱 (**): 2 ** 3 = {2 ** 3}")

print("\n=== 2. 복합 대입 연산자 ===")
# 파이썬은 ++, -- 증감 연산자가 없습니다.
count = 10
count += 5   # count = count + 5
count *= 2
print(f"최종 count: {count}")