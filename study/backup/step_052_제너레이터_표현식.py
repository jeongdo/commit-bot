# 하나의 문장으로 제너레이터를 구성하는 방법 : 제너레이터 표현식

print("============================================")


def show_all(s):
    for i in s:
        print(i, end='\n')


st = [2 * i for i in range(1, 10)]  # 리스트 컴프리핸션
show_all(st)

print("=========== 제너레이터 함수 사용 ==============")


def times2():  # 제너레이터 함수의 정의
    for i in range(1, 10):
        yield 2 * i


g = times2()  # 제너레이터 객체의 생성 !!
show_all(g)  # 위에서 정의한 show_all 호출

print("=========== 제너레이터 표현식 사용 ==============")     # 재사용 하는게 아니고 한번 쓰고 말거면, 이렇게 하자!

# 표현식 기반 제너레이터 생성
# () 로 감싸져 있다고 해서 튜플이 아니다.
# st = [2 * i for i in range(1, 10)]  # 리스트 컴프리핸션하고 차이는 () 와 [] 의 차이일뿐이니 어렵게 생각하지 말자.
g1 = (2 * i for i in range(1, 10))

show_all(g1)  # 위에서 정의한 show_all 호출, 호출할 때마다 하나씩 지정된 값을 반환한다.

# print(next(g1))
# print(next(g1))

print("=============================================")


def two():
    print('two')
    return 2


g = (two() * i for i in range(1, 10))  # two() 함수는 호출 안되니 안심
print(next(g))
print(next(g))

print("=========== 호출함수에 제너레이터 표현식을 바로 전달하는 경우에는 소괄호 생략이 가능하다. ===========")

# show_all((2 * i for i in range(1, 10)))  # 함수에 제너레이터 표현식을 바로 전달하는 경우에는 다음과 같이 소괄호를 생략할 수 있다.
show_all(2 * i for i in range(1, 10))
