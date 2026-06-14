class SoSimple:
    def __init__(self, i):
        self.i = i

    def seti(self, i):
        self.i = i

    def geti(self):
        return self.i


# 클래스에 속한 변수 추가하기
# 파이썬의 클래스는 클래스이자 객체이다.

SoSimple.n = 8

print(SoSimple.n)

ss1 = SoSimple(3)
# 객체에 선언되어 있지 않으면, 클래스에 선언되어 있는지 찾아 올라간다.
print(ss1.n)
print(ss1.geti())

# 클래스도 객체이다 분석하기

print(type)  # <class 'type'>의 객체
print(type([1, 2]))  # [1, 2]의 자료형은 <class 'list'>
print(type(list))  # list 자료형은 <class 'type'>


class EmptyClass:
    pass


# <class 'type'> : 메타 클래스의 자세한 정보 : https://tech.ssut.me/understanding-python-metaclasses/

print(type(SoSimple))  # <class 'type'>의 객체
print(type(EmptyClass))  # <class 'type'>의 객체

class1 = EmptyClass

c1 = EmptyClass()
c2 = class1()  # 클래스도 객체이기 때문에, 변수 대입을 통해 객체 생성도 가능하다.
