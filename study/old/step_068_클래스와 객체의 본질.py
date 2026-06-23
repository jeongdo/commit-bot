class Simple:
    def seti(self, i):  # 파이썬에서는 getter/setter 에서 필요한 멤버변수를 선언하지 않아도, 사용시 자동으로 선언된 것으로 간주한다.
        self.i = i  # 이문장이 실행되는 순간 i라는 객체 멤버 변수가 만들어진다.

    def geti(self):
        return self.i


s1 = Simple()
s1.seti(200)
print(s1.geti())

print("===== set 메소드를 호출하지 않아 i 변수가 존재하지 않는다. =============")

s2 = Simple()
s2.geti()


# Traceback (most recent call last):
#   File "C:/Dropbox/Python/study/python_3/src/step_068_클래스와 객체의 본질.py", line 10, in <module>
#     s1.geti()
#   File "C:/Dropbox/Python/study/python_3/src/step_068_클래스와 객체의 본질.py", line 6, in geti
#     return self.i
# AttributeError: 'Simple' object has no attribute 'i'


class Simple2:
    def __init__(self):
        self.i = 0  # 변수 초기화, 이 순간에 변수 i가 만들어진다. 객체가 생성될 동시에 변수도 초기화 된다.
        # __init__의 호출이 완료되는 시점을 객체 생성이 완료되는 시점으로 판단

    def seti(self, i):
        self.i = i  # 이 순간에 만들지 말고,

    def geti(self):
        return self.i


s3 = Simple2()
print(s3.geti())
