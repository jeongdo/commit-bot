# class 메소드 : class 메소드도 static 메소드처럼 클래스에 속하는 메소드


class Simple:
    num = 5  # Simple의 클래스 변수

    @staticmethod
    def sm(i):  # static 메소드
        print('st~ 5 + {0} = {1}'.format(i, Simple.num + i))

    @classmethod
    def cm(cls, i):  # class 메소드, cls 에는 Simple 클래스를 전달한다.
        print('cl~ 5 + {0} = {1}'.format(i, Simple.num + i))


def main():
    Simple.sm(3)  # 클래스 이름 기반의 static 메소드 호출
    Simple.cm(3)  # 클래스 이름 기반의 class 메소드 호출
    print("=======================")
    s = Simple()
    s.sm(4)         # 객체를 대상으로 한 static 메소드 호출
    s.cm(4)         # 객체를 대상으로 한 class 메소드 호출


main()
