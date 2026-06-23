# 코루틴 Ex3
# StopIteration 예외 처리를 await로 변경가능 (파이썬 3.5 이상)
# 파이썬 3.5 이상에서 -> def 키워드를 async, yield 키워드를 await로 바꿔사용해도 되게 반영, 짝을 맞춰서 사용해야 함.
# 중첩 코루틴 처리

def generator1():
    for x in 'AB':
        yield x
    for y in range(1, 4):
        yield y


t1 = generator1()

print(next(t1))
print(next(t1))
print(next(t1))
print(next(t1))
print(next(t1))
# print(next(t1))

t2 = generator1()

print(list(t2))
