class Simple:
    def __init__(self, i):
        self.i = i


s = Simple(10)
print(s)
print(s.__str__())  # object 클래스의 __str__ 메소드 호출


class Simple2:
    def __init__(self, i):
        self.i = i

    # object 클래스의 __str__ 메소드를 오버로딩 한것이다.
    def __str__(self):                          # 문자열의 객체 형태를 조합하여 포함할 때 사용하는 메소드
        return 'Simple2({0})'.format(self.i)    # 'Simple(20)' 형태의 문자열 생성 및 반환


s1 = Simple2(10)
print(s1)


class Vector2:       # 수학의 벡터를 구조화한 클래스
    def __init__(self, x, y):
        self.x = x      # 벡터의 x 방향 값
        self.y = y      # 벡터의 y 방향 값

    def __add__(self, o):  # 벡터의 덧셈 연산
        return Vector2(self.x + o.x, self.y + o.y)       # 새로운 객체 생성 및 반환

    def __str__(self):    # 벡터 정보를 문자열로 반환
        return 'Vector2({0}, {1})'.format(self.x, self.y)


def main():
    v1 = Vector2(3, 3)
    v2 = Vector2(7, 7)
    v3 = v1 + v2  # 새로운 Vector 객체 생성되어 v3에 저장
    # print(v1())
    # print(v2())
    # print(v3())
    # 이제 소괄호를 사용하지 않아도 된다.
    print(v1)
    print(v2)
    print(v3)


main()
