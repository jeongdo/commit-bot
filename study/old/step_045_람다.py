# 함수 이름이 존재하는 이유 : 함수를 호출하기 위해

def fct_fac(n):
    def exp(x1):  # 이 이름은 호출한 적이 없는데.. 그냥 반환 용도!
        return x1 ** n

    return exp


def show(s):
    print(s)


ref = show

ref('hi')

# 함수가 반환이라는 목적만 충실히 이행해 주면 함수의 이름이 불필요 하다. 람다의 시작
print("================================================")

ref2 = lambda s: print(s)  # 람다 기반의 함수 정의, 매개변수와 함수 몸체
ref2('hello')

ref3 = lambda n1, n2: n1 + n2  # 결과가 나오면 리턴하도록 약속
print(ref3(3, 4))

ref4 = lambda s: len(s)
print(ref4('simple'))

ref5 = lambda: print('yes')  # 매개변수가 없으면 비워두면 된다.
ref5()

print("================================================")


def fct_fac2(n):
    return lambda x1: x1 ** n


ref6 = fct_fac2(2)
ref7 = fct_fac2(4)

print(ref6(5))  # 5의 제곱
print(ref7(5))  # 5의 네제곱
