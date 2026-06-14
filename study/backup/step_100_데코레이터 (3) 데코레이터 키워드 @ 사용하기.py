def adder_deco(func):  # 데코레이터 함수
    def ad(*args):  # 전달인자를 튜플로 묶는다. 튜플 패킹 : 전달되는 모든 인자를 하나의 튜플로 묶는다.
        print(*args, sep=' + ', end=' ')  # 새로 추가된 기능
        print("= {0}".format(func(*args)))  # *args: 여기서는 튜플 언패킹, 분리되어 전달된다.

    return ad


@adder_deco  # 함수를 데코레이터 adder_deco 에 통과시켜라.
def add2(n1, n2):
    return n1 + n2


@adder_deco
def add3(n1, n2, n3):
    return n1 + n2 + n3


def main():
    add2(3, 4)  # 어차피 통과시킬 거니깐 더 줄여보자.
    add3(3, 4, 5)


main()
