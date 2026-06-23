# __next__ 메소드 : next 함수 호출 시 불리는 스페셜 메소드
# 조건 1) 가지고 있는 값을 하나씩 반환한다.
# 조건 2) 더 이상 반환할 값이 없는 경우 StopIteration 예외를 발생시킨다.


# 저장소 역할을 하는 클래스를 표현한 결과
class Coll:
    def __init__(self, d):
        self.ds = d  # 인자로 전달된 값을 저장한다.
        self.cc = 0  # __next__ 메소드 호출 횟수

    def __next__(self):
        if len(self.ds) <= self.cc:  # 더 이상 반환할 값이 없으면 예외 발생!
            raise StopIteration
        self.cc += 1  # __next__ 호출 횟수 증가
        return self.ds[self.cc - 1]  # 값을 하나씩 반환


def main():
    co = Coll([1, 2, 3, 4, 5])  # 튜플 및 문자열도 전달할 수 있음
    while True:
        try:
            i = next(co)  # iterator 객체를 통해서 하나씩 꺼낸다.
            print(i)
        except StopIteration:  # 더 이상 꺼낼 값이 없으면,
            break  # 이 루프를 탈출한다.


main()
