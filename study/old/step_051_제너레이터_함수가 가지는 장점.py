# 제너레이터는 iterator 객체의 한 종류이다.

def pows(s):
    r = []  # 빈 리스트
    for x in s:  # s에 던져서 x로 이동해서 x**2를 실행하고, r에 담는다.
        r.append(x ** 2)  # 필요한 부분을 미리 만들어 놓는다.
    return r


st = pows([1, 2, 3, 4, 5, 6, 7, 8, 9])

for i in st:
    print(i, end='\n')

print("============= 메모리 크기 체크 전 =================")

import sys

print(sys.getsizeof(st))  # 변수 st에 담긴 객체의 메모리 크기 정보 반환

print("================================================")


def gpows(s):
    r = []  # 빈 리스트
    for x in s:
        yield x ** 2        # 이번에는 next 호출할 때마다 던져 주는 차이만 설정한 것이다.


st = gpows([1, 2, 3, 4, 5, 6, 7, 8, 9])  # 필요할 때마다 여기서 생산을 하기 때문에, 메모리 소요가 작다.

for i in st:
    print(i, end='\n')

print("============= 메모리 크기 체크 후 =================")

print(sys.getsizeof(st))  # 메모리 사이즈가 작아졌다!

print("================================================")


# 정리하자면, 생성되는 값들을 순서대로 하나씩 가져다 쓰면 되는 상황에서는 이렇듯 제너레이터를 기반으로 코드를 작성하는 것이 합리적이다.
# 참고로 map, filter 도 사실은 제너레이터 함수이다. 즉, map, filter 함수가 반환하는 것은 iterator 객체이자 제너레이터 객체이다.


def get_nums():
    ns = [0, 1, 0, 1, 0, 1]
    for i in ns:
        yield i


g = get_nums()
print(next(g))
print(next(g))

# 파이썬 3.3 이상 코드

print("================================================")


def get_nums_3_3():
    ns = [0, 1, 0, 1, 0, 1]
    # for i in ns:
    #    yield i
    yield from ns   # ns에 있는 값들을 하나씩 yield


g_3_3 = get_nums_3_3()
print(next(g_3_3))
print(next(g_3_3))
