# 제너레이터는 iterator 객체의 한 종류이다.

def gen_num():  # 제너레이터 함수의 정의
    print('first number')
    yield 1  # yield가 하나라도 들어가면 제너레이터가 됩니다.
    print('second number')
    yield 2  # yield가 하나라도 들어가면 제너레이터가 됩니다.
    print('third number')
    yield 3


gen = gen_num()  # yield를 발견하면, 함수를 실행하지 않고, 제너레이터 객체를 생성하고 사용전 일단 대기중

print(next(gen))  # next(gen) 함수 호출되고, 호출될 때마다 선언한 yield 값 1이 반환되고, 1이전의 함수 내부의 print('first number') 실행
print(next(gen))  # 
print(next(gen))  # 한번 더 호출하면, StopIteration 예외가 발생한다.

# 이렇듯 함수 호출 이후에 그 실행의 흐름을 next 함수가 호출될 때까지 미루는 (늦추는) 특성을 가리켜 'lazy evaluation' 이라고 한다.

print("================================================")


def gen_for():
    for i in [1, 2, 3]:
        yield i  # for 루프 돌 때마다 매번 yield 문을 실행하게 된다.


print("================================================")

g = gen_for()
print(next(g))
print(next(g))
print(next(g))
