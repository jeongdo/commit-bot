def deco1(func):  # 데코레이터 1
    def inner():
        print('deco1')
        func()

    return inner


def deco2(func):  # 테코레이터 2
    def inner():
        print('deco2')
        func()

    return inner


@deco1
@deco2  # simple 실행 및 반환하기 전에 deco2가 대신 실행 및 반환 해주네, 아~ 그런데 다시 보니 deco2 실행 및 반환 전에, deco1 이 deco2를 실행 및 반환 해주네의 순서이다.
def simple():
    print("simple")


def main():
    simple()


main()
