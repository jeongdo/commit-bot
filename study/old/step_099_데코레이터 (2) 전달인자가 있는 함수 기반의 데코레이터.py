# 전달인자가 있는 함수 기반의 데코레이터

def add2(n1, n2):
    return n1 + n2


def add3(n1, n2, n3):
    return n1 + n2 + n3


def adder_deco(func):  # 데코레이터 함수
    def ad(*args):  # 전달인자를 튜플로 묶는다. 전달되는 모든 인자를 하나의 튜플로 묶는다.           튜플 패킹
        print(*args, sep=' + ', end=' ')  # 새로 추가된 기능
        print("= {0}".format(func(*args)))  # *args: * 붙혀 버리면, 내부로 분리되어 전달된다.   튜플 언패킹

    return ad


def main():
    adder2 = adder_deco(add2)
    adder2(3, 4)    # 파라미터를 튜플로 묶어 버리겠다.

    adder3 = adder_deco(add3)
    adder3(3, 4, 5)


main()
