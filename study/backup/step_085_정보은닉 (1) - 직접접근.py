class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.age)


def main():
    p = Person('James', 22)
    print(p)
    p.age -= 1      # 현재 직접 접근이 가능하다.
    print(p)


main()