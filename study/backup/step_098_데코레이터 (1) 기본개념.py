# 데코레이터 : 기존에 있는 함수에 새로운 기능을 추가/보강할 수 있는 기술

def deco(func):
    def df():  # nested 함수
        print("emotiocon!!")  # 새로 추가된 기능
        func()  # 원래 가지고 있는 기능
        print("emotiocon!!")  # 새로 추가된 기능

    return df


def smile():  # 데코레이터를 통과하는 용도로 사용되었다. 데코레이터가 만드는 새로운 객체가 이것을 참조하게 된다.
    print("^_^")


def main():
    smile1 = deco(smile)
    smile1()


main()
