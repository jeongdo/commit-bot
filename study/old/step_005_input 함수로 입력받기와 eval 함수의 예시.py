age = input("몇 살이세요? ")  # 문자열로 반환된다.
print(age)

# print(eval(400)) : eval() arg 1 must be a string, bytes or code object,  eval 함수는 문자열을 파라미터로 받는다.

num = input("숫자를 입력하세요: ")
print(eval(num) + 4)

# eval - 문자열 사칙연산도 알아서 계산해준다.
print(eval("2-5+5"))


def ret():
    return 13


print(eval("ret()"))  # 사실 여기에 input 함수를 넣어서 ret() 문자열을 입력해도 결과는 동일

result = eval(input("뭐든 넣어요: "))


print(result)