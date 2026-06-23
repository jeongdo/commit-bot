# 적절한 형태로 +와 - 연산자 오버로딩

n1 = 3
n2 = 5

print(n1 + n2)

s1 = 'Y'
s2 = 'onn'

print(s1 + s2)  # 문자열의 연산자 오버로딩이 적용된 것이라고 볼 수 있다.


class Vector:       # 수학의 벡터를 구조화한 클래스
    def __init__(self, x, y):
        self.x = x      # 벡터의 x 방향 값
        self.y = y      # 벡터의 y 방향 값

    def __add__(self, o):  # 벡터의 덧셈 연산
        return Vector(self.x + o.x, self.y + o.y)       # 새로운 객체 생성 및 반환

    def __call__(self):    # 벡터 정보를 문자열로 반환
        return 'Vector({0}, {1})'.format(self.x, self.y)


def main():
    v1 = Vector(3, 3)
    v2 = Vector(7, 7)
    v3 = v1 + v2  # 새로운 Vector 객체 생성되어 v3에 저장
    print(v1())
    print(v2())
    print(v3())


main()
