class Person2:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def add_age(self, age):
        if (age < 0):       # 나이를 먹는건 - 로 먹을 수 없다.
            print("나이 정보 오류")
        else:
            self.age += age

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.age)


def main():
    p = Person2('James', 22)
    print(p)
    p.add_age(1)    # 간접 접근 또는 정보 은닉(기능 제공이 추가되는 것이 아니라, 코드의 안정성을 향상 시키는데 그 의미가 있다.)
    print(p)


main()