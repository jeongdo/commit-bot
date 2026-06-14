# iterable 객체 : iter 함수에 인자로 전달 가능한 객체, 그 결과로 'iterator 객체' 반환
# iterator 객체 : next 함수에 인자로 전달 가능한 객체

s1 = [1, 2, 3]  # s1이 iter() 함수로 전달가능하니, iterable 객체이다.
r1 = iter(s1)  # s1의 iter() 함수 반환으로 r1이 iterator 객체이다.


class Car:
    def __init__(self, id):
        self.id = id

    def __iter__(self):  # 스페셜 메소드
        # 변수 id의 iterator 객체를 만들어서, 그것을 return 하도록 만들어 줘야 한다.
        return iter(self.id)


def main():
    c = Car("32러5234")  # Car 객체가 iterable 객체이다.
    for i in c:
        print(i)


main()
