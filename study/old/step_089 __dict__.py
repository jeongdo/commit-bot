# 객체 내에는 해당 객체의 변수 정보를(속성 정보를) 담고 있는 딕셔너리가 하나 존재한다.
# __dict__ 는 객체 당 하나씩 가지고 있다.

class Person:
    def __init__(self, n, a):
        self._name = n  # 이름
        self._age = a   # 나이
        self.__height = 10  # __height 가 _Person__height 로 이름이 바뀌어서 접근을 못했던 것이었다.


class Simple:
    def __init__(self, n, s):
        self._n = n
        self._s = s

    def __str__(self):
        return '{0}: {1}'.format(self._n, self._s)


def main():
    p = Person('James', 22)  # 22살의 James
    print(p.__dict__)  # 객체 내에 딕셔너리 정보 출력, 객체마다 이 정보는 유지된다. (클래스당 한개는 아니다.)
    print("==========")
    p.len = 178  # 객체에 변수를 추가
    p.adr = 'korea'
    p.__dict__['_Person__height'] = 20
    print(p.__dict__)
    sp = Simple(10, 'my')
    print("수정 전 => ", sp)
    sp.__dict__['_n'] += 10  # __dict__에 접근해서 값을 변경
    sp.__dict__['_s'] += ' your'
    print("수정 후 => ", sp)


main()
