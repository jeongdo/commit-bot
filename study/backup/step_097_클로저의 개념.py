# 클로저 : 안쪽에 위치한 네스티드 함수(객체)가 자신이 필요한 변수의 값을 어딘가에 저장해 두는 기술

def maker(m):
    def inner(n):  # nested 함수
        return m * n

    return inner


def main():
    m1 = maker(2)
    m2 = maker(22)
    print(m1(7))
    print(m1(5))
    print(m1.__closure__[0].cell_contents)  # 클로저 변수값의 저장 위치와 값 확인
    print(m2(7))
    print(m2(5))
    print(m2.__closure__[0].cell_contents)  # 클로저 변수값의 저장 위치와 값 확인


main()
