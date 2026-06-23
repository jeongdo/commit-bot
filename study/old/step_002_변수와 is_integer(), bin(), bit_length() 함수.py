val = 40

print(val)
print(val.bit_length())  # 파이썬의 모든 값은 객체이다. 보아라 객체 함수가 있잖아!
# bit_length() : 부호와 선행 0을 제외하고, 이진수로 정수를 나타내는 데 필요한 비트 수를 돌려줍니다:

n = -37

print(n)
print(bin(n))
print(bin(val))
print(n.bit_length())

x, y = 0, 797.121
z = 797.0
print(y)
print(x, y.is_integer())
print(z.is_integer())  # 797.0 은 정수구나!!
