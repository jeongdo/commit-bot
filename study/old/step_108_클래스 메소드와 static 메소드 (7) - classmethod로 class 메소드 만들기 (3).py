# class 메소드 : class 메소드도 static 메소드처럼 클래스에 속하는 메소드


class Natural:
    def __init__(self, n):
        self.n = n

    def getn(self):
        return self.n

    @classmethod
    def add(cls, n1, n2):
        return cls(n1.getn() + n2.getn())  # Natural 객체 생성 후 반환


def main():
    n1 = Natural(1)
    n2 = Natural(2)
    n3 = Natural.add(n1, n2)    # 반한되는 객체를 n3에 저장

    print('{0} + {1} = {2}'.format(n1.getn(), n2.getn(), n3.getn()))


main()
