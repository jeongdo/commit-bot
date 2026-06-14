def generator2():
    yield from 'AB'     # from 키워드는 주어진 데이터를 순차적으로 반환을 하겟다.
    yield from range(1, 4)


t3 = generator2()

print(next(t3))
print(next(t3))
print(next(t3))
print(next(t3))
print(next(t3))
# print(next(t3))