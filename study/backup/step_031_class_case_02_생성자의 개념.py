from clazz.ageinfo_02 import AgeInfoInit


def main():
    fa = AgeInfoInit(39, 1)     # fa 이름의 AgeInfo 객체 생성, fa.age = 39 # 인스턴스 변수
    print("나이", fa.get_age())
    fa.up_age()
    print("나이", fa.get_age())
    print("나이", AgeInfoInit.get_age(fa))
    fa.get_sex()

    mom = AgeInfoInit(30, 2)
    # mom.age= 30
    print("어머니 나이", mom.get_age())
    mom.set_age(44)
    print("어머니 나이", mom.get_age())
    mom.get_sex()


main()
