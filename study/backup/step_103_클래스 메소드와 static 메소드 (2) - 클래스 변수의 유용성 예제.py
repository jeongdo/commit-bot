class Simple:
    count = 0  # Simple의 클래스 변수, 생성된 객체 수를 저장하는 것이 목적

    def __init__(self):
        Simple.count += 1  # 클래스 변수 count 값 1 증가

    def get_count(self):
        return Simple.count  # 클래스 변수 count 값 반환


def main():
    s1 = Simple()
    print(s1.get_count())
    s2 = Simple()
    print(s2.get_count())
    s3 = Simple()
    print(s3.get_count())


main()
