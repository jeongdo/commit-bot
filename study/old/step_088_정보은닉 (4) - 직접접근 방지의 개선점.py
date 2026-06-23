# __가 스페셜 메소드에서도 사용되는데 혼동발생과 코드 오류 확률이 높아진다. 다르게 해보자. 그냥 관례로 하나만 붙히자. 우리의 약속!!

class Person4:
    def __init__(self, name, age):
        self._name = name  # __를 멤버변수에 붙히면, 직접접근을 막는다.
        self._age = age

    def add_age(self, age):
        if (age < 0):  # 나이를 먹는건 - 로 먹을 수 없다.
            print("나이 정보 오류")
        else:
            self._age += age

    def __str__(self):
        return '{0}: {1}'.format(self._name, self._age)


def main():
    p = Person4('James', 22)
    print(p)
    p.add_age(1)  # 간접 접근 또는 정보 은닉(기능 제공이 추가되는 것이 아니라, 코드의 안정성을 향상 시키는데 그 의미가 있다.)
    print(p)
    p._age += 1  # 이 문장을 실행은 되지만, 약속으로 이건 하지 말자고 규칙이다.
    print(p)


main()
