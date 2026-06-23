# class 메소드 : class 메소드도 static 메소드처럼 클래스에 속하는 메소드


class Simple:
    count = 0  # 생성된 객체의 수

    def __init__(self):
        Simple.count += 1

    @classmethod
    def get_count(cls):
        return cls.count  # cls에 전달되는 것은 Simple 클래스


def main():
    print(Simple.get_count())
    s = Simple()  # 객체의 생성
    print(Simple.get_count())


main()
