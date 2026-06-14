num1 = 10
num1 += 10  # 복합 대입 연산자도 그대로 적용
print(num1)
num1 -= 10
print(num1)
num1 *= 10
print(num1)

print("=========================")

num1 = float(num1)
print(num1)  # 100 -> 100.0 이 된다.
print(type(num1))

num2 = float("3.14")
print(type(num2))

print("=========================")

# num3 = int("4.15"); # error
num3 = int("4")
print(type(num3))

num4 = int(4.14)
print(num4)
print(type(num4))

# eval 은 정수 입력시 int, 실수 입력시 float 바꿔준다.

print("=========================")

num5 = "5"
# num5 = string("5") # error
print(type(num5))
