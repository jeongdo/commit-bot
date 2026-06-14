# static 메소드 : 클래스에 속하는 메소드


class Simple:
    count = 0  # Simple의 클래스 변수, 생성된 객체 수를 저장하는 것이 목적

    def __init__(self):
        Simple.count += 1  # 클래스 변수 count 값 1 증가

    def get_count():        # static 메소드는 첫 번째 인자로 self가 없다!! - 주의, self롤 통해서는 객체가 참조되는데, 여기서는 대상 객체가 없기 때문이다.
        return Simple.count  # 클래스 변수 count 값 반환

    get_count = staticmethod(get_count)     # get_count 메소드를 static 메소드로 만드는 방법


def main():
    Simple.get_count()             # static 메소드는 클래스 이름을 통해 호출 가능
    s = Simple()
    print(s.get_count())           # static 메소드는 객체를 통해서도 호출 가능


main()
