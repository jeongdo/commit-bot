class Person3:
    def __init__(self, name, age):
        self.__name = name      # __를 멤버변수에 붙히면, 직접접근을 막는다.
        self.__age = age

    def add_age(self, age):
        if (age < 0):       # 나이를 먹는건 - 로 먹을 수 없다.
            print("나이 정보 오류")
        else:
            self.__age += age

    def __str__(self):
        return '{0}: {1}'.format(self.__name, self.__age)


def main():
    p = Person3('James', 22)
    print(p)
    p.add_age(1)    # 간접 접근 또는 정보 은닉(기능 제공이 추가되는 것이 아니라, 코드의 안정성을 향상 시키는데 그 의미가 있다.)
    print(p)
    #  p.__age += 1     # 이 문장을 실행하면 오류 발생, 파이참에서는 멤버변수가 아예 보이지도 않는다.


main()