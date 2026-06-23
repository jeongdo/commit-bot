"""
Chapter 1
Python Advanced(1) - Python Variable Scope
Keyword - scope, global, nonlocal, locals, globals..

"""
"""
              global     local
함수안읽기       0          0
함수안쓰기       X*         0  
함수밖읽기       0          X
함수밖쓰기       0          X

전역변수는 주로 변하지 않는 고정 값에 사용
지역변수 사용 이유 :지역변수는 함수 내에 로직 해결에 국한, 소멸주기 함수 실행 해제 시
전역변수를 지역내에서 수정되는 것은 권장X

"""
# Ex1
a = 10  # Global variable


def foo():
    # Read global variable
    print('Ex1 > ', a)


foo()
# Read global variable
print('Ex1 > ', a)

print("=====================================================")

# Ex2
b = 20


# 함수 지역 스코프에서 먼저 찾고, 없으면 순차적으로 위로 올라가서, 글로벌 전역까지 해당 변수의 값을 찾아 간다.
def bar():
    b = 30  # Local variable
    print('Ex2 > ', b)  # Read local variable


bar()

print('Ex2 > ', b)  # Read global variable

print("=====================================================")

# Ex3
c = 40


def foobar():
    # c = c + 10   # UnboundLocalError
    # c = 10
    # c += 100

    print('Ex3 > ', c)


foobar()

# Ex4
d = 50


def barfoo():
    global d

    d = 60
    print('Ex4 > ', d)


barfoo()

print('Ex4 > ', d)  # Prints 5. Global variable d was modified within barfoo()


# Ex5(중요)
def outer():
    e = 70

    def inner():
        nonlocal e
        e += 10  # e = e + 10
        print('Ex5 > ', e)

    return inner


in_test = outer()  # Closure

in_test()
in_test()


# Ex6
def func(var):
    x = 10

    def printer():
        print('Ex5 > ', "Printer Func Inner")

    print('Func Inner', locals())  # 호출한 함수내의 정보를 딕셔너리로 전체 출력


func("Hi")

# Ex7
print('Ex7 >', globals())  # 전역 전체 출력,  # 호출한 파일 내의 모든 변수와 함수 정보를 딕셔너리로 전체 출력
globals()['test_variable'] = 100
print('Ex7 >', globals())

# Ex8(지역 -> 전역 변수 작성)
for i in range(1, 10):
    for k in range(1, 10):
        globals()['plus_{}_{}'.format(i, k)] = i + k

print(globals())

print(plus_3_5)  # 전역에 함수를 만들어 두어서 실행이 가능하다.
print(plus_9_9)
