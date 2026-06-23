def greet():  # : 다음줄에 이어진다는 의미?
    print("반갑습니다.")
    print("파이썬의 세계로 오신 것을 환영합니다.")
    print("abc", 1, 2, 3, 4)
    print('\n')


greet()


def greet_who(name):
    print("반갑습니다. ", name)
    print("파이썬의 세계로 오신 것을 환영합니다.")
    print("abc", 1, 2, 3, 4)
    print('\n')


greet_who("정도")


def gt2(n1, n2):
    print("반갑습니다. ", n1, n2)
    print('\n')


gt2('나', '허정도')


def add(n1, n2):
    print("합 : ", n1 + n2)
    return n1 + n2


result = add(1, 39)

print(result)

print(add(2, 4))

# 파이썬은 대소문자를 구분할 수 있다.
# 파이썬의 변수나 함수는 숫자로 시작하는 것이 불가한다.
# 키워드를 변수명이나 함수명 등으로 사용할 수 없다.
# 둘이상의 단어를 연결하는 경우는 언더바를 이용한다.


# 파이썬은 전역변수와 함수내의 지역변수가 확실히 나눠진다.

cnt = 200


def var1(t):
    cnt = 0
    t += 1
    cnt += 30  # local variable 'cnt' referenced before assignment
    print(t)


var1(cnt)  # 201

# print(t)  # name 't' is not defined
print(cnt)  # 200
