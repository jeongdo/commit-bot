class Coll2:                             # 저장소 역할을 하는 클래스를 표현한 결과
    def __init__(self, d):
        self.ds = d                     # 인자로 전달된 값을 저장한다.

    def __next__(self):
        if len(self.ds) <= self.cc:     # 더 이상 반환할 값이 없으면 예외 발생!
            raise StopIteration
        self.cc += 1                    # __next__ 호출 횟수 증가
        return self.ds[self.cc - 1]     # 값을 하나씩 반환

    def __iter__(self):
        self.cc = 0                     # next 호출횟수 초기화
        return self                     # 이 객체를 그대로 반환함


def main():
    co = Coll2([1, 2, 3, 4, 5])          # 튜플 및 문자열도 전달할 수 있음
    for i in co:                         # for 루프에서 이제 구동을 할 수 있다. iterator 객체이기 때문에
        print(i)

    for i in co:
        print(i)

    co1 = Coll2('hello')
    itr = iter(co1)
    print(itr is co1)                   # 동일한 객체인지 확인, self를 반환하니 동일한 객체이다,


main()
