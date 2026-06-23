"""
007: float (실수)와 부동소수점 오차 해결
"""

print("=== 1. 기본 실수와 지수 표기법 ===")
print(f"1.5e-3 = {1.5e-3} (1.5 * 10^-3)")

print("\n=== 2. 부동소수점 오차 (주의) ===")
result = 0.1 + 0.2
print(f"0.1 + 0.2 = {result}")
print(f"0.1 + 0.2 == 0.3 결과: {result == 0.3}") # False!

print("\n=== 3. [심화] 완벽한 소수점 계산 (Decimal) ===")
# 금융/퀀트 데이터 등 정확한 소수점 계산이 필요할 때 필수
from decimal import Decimal

# 반드시 '문자열'로 초기화해야 정확도가 유지됨
dec_a = Decimal('0.1')
dec_b = Decimal('0.2')
print(f"Decimal 연산: {dec_a + dec_b == Decimal('0.3')}") # True