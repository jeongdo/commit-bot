# 클래스도 객체이다 분석하기

class SoSimple:
    def __init__(self, i):
        self.i = i

    def seti(self, i):
        self.i = i

    def geti(self):
        return self.i


print(type)  # <class 'type'>의 객체
print(type([1, 2]))  # [1, 2]의 자료형은 <class 'list'>
print(type(list))  # list 자료형은 <class 'type'>, 리스트 클래스는 type 클래스의 객체이기도 하다.


class EmptyClass:
    pass


# <class 'type'> : 메타 클래스의 자세한 정보 : https://tech.ssut.me/understanding-python-metaclasses/

print(type(SoSimple))  # <class 'type'>의 객체
print(type(EmptyClass))  # <class 'type'>의 객체

class1 = EmptyClass

c1 = EmptyClass()
c2 = class1()  # 클래스도 객체이기 때문에, 변수 대입을 통해 객체 생성도 가능하다.
