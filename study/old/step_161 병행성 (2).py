# Chapter06-02
# 병행성(Concurrency)  : 한 컴퓨터가 여러 일을 동시에 수행
# 병렬성(Parallelism)  : 여러 컴퓨터가 여러 작업을 동시에 수행하고, 취합은 한 곳에서 진행
# 이터레이터, 제네레이터
# Iterator, Generator

# 파이썬 반복 가능한 타입
# for, collections, text file, List, Dict, Set, Tuple, unpacking, *args

# Generator Ex1
def generator_ex1():
    print('Start')
    yield 'A Point.'
    print('continue')
    yield 'B Point.'
    print('End')


temp = iter(generator_ex1())

# print(next(temp))
# print(next(temp))
# print(next(temp))

for v in generator_ex1():
    pass
    # print(v)

print()

# Generator Ex2
temp2 = [x * 3 for x in generator_ex1()]

# 표현식 기반 제너레이터 생성
# () 로 감싸져 있다고 해서 튜플이 아니다.
# st = [2 * i for i in range(1, 10)]  # 리스트 컴프리핸션하고 차이는 () 와 [] 의 차이일뿐이니 어렵게 생각하지 말자.
g1 = (2 * i for i in range(1, 10))
print(type(g1))
print(next(g1))
print(next(g1))

temp3 = (x * 3 for x in generator_ex1())  # 이건 제네레이터

print(temp2)  # x 에 해당하는 것은 yield 'A Point.' 리턴이다. 리스트 컴프리헨션에서는 각 리턴값을 3배수 한 것이 배열 하나에 들어갔다.
print(temp3)

for i in temp2:
    print(i)

print()
print()

for i in temp3:
    print(i)

print()
print()

# Generator Ex3(중요 함수)
# takewhile, filterfalse, accumulate, chain, product, product, groupby
import itertools  # 데이터 무한대 만들어 보기

gen1 = itertools.count(1, 2.5)

print(next(gen1))
print(next(gen1))
print(next(gen1))
print(next(gen1))

# ... 무한    : 무한대로 1부터 2.5 씩 증가하는 정수를 만들어낸다.
# while True:
#     print(next(gen1))


print()

# 조건 : 1000 미만일 때 까지
gen2 = itertools.takewhile(lambda n: n < 1000, itertools.count(1, 2.5))

for v in gen2:
    print(v)

print()
print("============================================")

# 필터 반대
gen3 = itertools.filterfalse(lambda n: n < 3, [1, 2, 3, 4, 5])  # n < 3 : 3미만이 1, 2 인데, 그 반대 결과인 3, 4, 5 출력

for v in gen3:
    print(v)

print()
print("============================================")

# 단순 합계라 아니라 순차적으로 현 상황까지의 누적의 합계 값을 각 요소 순번별로 출력한다.
gen4 = itertools.accumulate([x for x in range(1, 101)])

for v in gen4:
    print(v)

print()
print("============================================")

# 연결1 : 앞에 것과 뒤에 거를 하나로 묶어 준다.
gen5 = itertools.chain('ABCDE', range(1, 11, 2))

print(list(gen5))
print("============================================")

# 연결2 : enumerate 인덱스 번호를 붙혀 튜플형 원소의 리스트가 반환
gen6 = itertools.chain(enumerate('ABCDE'))

print(list(gen6))
print("============================================")
# 개별
gen7 = itertools.product('ABCDE')

print(list(gen7))
print("============================================")

# 연산(경우의 수), 순서쌍을 맺어준다.
gen8 = itertools.product('ABCDE', repeat=2)

print(list(gen8))
print("============================================")

# 그룹화
gen9 = itertools.groupby('AAABBCCCCDDEEE')

# print(list(gen9))

for chr, group in gen9:
    print(chr, ' : ', list(group))

print()
