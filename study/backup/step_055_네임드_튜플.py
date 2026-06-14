from collections import namedtuple  # collections 모듈의 namedtuple 호출

tri_one = (12, 15)  # 주석의 정보가 필요하다. 밑변 21, 높이 15
print(tri_one)

print("============== 네임드 튜플 ====================")

Tri = namedtuple('Triangle', ['bottom', 'height'])
# Tri = namedtuple('Tri', ['bottom', 'height']) # 이왕이면 같게 한다.

t = Tri(3, 7)  # 튜플 객체 생성

print(t)

print(t[0], t[1])  # 일반 튜플과 동일한 방법으로 접근 가능

print(t.bottom, t.height)  # 일반 튜플과 달리 이름으로도 접근이 가능

# 파이썬은 클래스도 객체이다.

print("============== 네임드 튜플의 언패킹 (1) =============")

t1 = Tri(12, 79)

a, b = t1

print(a, b)

print("============== 네임드 튜플의 언패킹 (2) =============")


def show(n1, n2):
    print(n1, n2)


show(*t1)
