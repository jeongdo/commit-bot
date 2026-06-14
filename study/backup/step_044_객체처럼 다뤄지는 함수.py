# 변수도 객체이다.

x = 3.0
print(type(x))
print(x.is_integer())


# 함수도 객체이다.
def func1(n):
    return n


def func2():
    print("Hello")


print(type(func1))  # 함수이름은 function 클래스의 객체이름이다.


def caller(fct):    # 함수도 객체이기 때문에 파라미터로 전달가능하다.
    fct()


caller(func2)


def fct_fac(n):
    def exp(x1):
        return x1 ** n

    return exp


f2 = fct_fac(2)

f3 = fct_fac(3)

print(f2(4))

print(f3(6))
