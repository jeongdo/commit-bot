# 함수도 객체이다. 함수의 이름은 객체를 참조하는 변수이다.

def maker(m):
    def inner(n):  # nested 함수
        return m * n

    return inner


def main():
    m1 = maker(2)
    print(m1(7))


main()
