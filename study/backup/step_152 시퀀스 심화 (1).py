# Chapter04-01
# 파이썬 심화
# 시퀀스형
# 컨테이너(Container : 서로다른 자료형[list, tuple, collections.deque], Flat : 한 개의 자료형[str,bytes,bytearray,array.array, memoryview])
# 가변(list, bytearray, array.array, memoryview, deque) vs 불변(tuple, str, bytes)
# 리스트 및 튜플 고급

# 지능형 리스트(Comprehending Lists)

# Non Comprehending Lists
chars = '+_)(*&^%$#@!~)'
code_list1 = []

for s in chars:
    # 유니코드 리스트
    code_list1.append(ord(s))  # ord : 문자표에 매핑되는 번호 출력

# Comprehending Lists
code_list2 = [ord(s) for s in chars]

# Comprehending Lists + Map, Filter
# 속도 약간 우세
code_list3 = [ord(s) for s in chars if ord(s) > 40]
# code_list4 = list(filter(lambda x: x > 40, chars))    # 40 보다 큰지를 true, false 로 리턴하는데, chars로 넣어줘도 되지만, 지금은 문자열이라 개별 필터 데이터가 필요
code_list4 = list(filter(lambda x: x > 40, map(ord, chars)))  # map(ord, chars) : ord 함수를 chars의 개수만큼 넣어줘.

# 전체 출력
print(code_list1)
print(code_list2)
print(code_list3)
print(code_list4)
print([chr(s) for s in code_list1])  # chr(s) for 로직에서 반환되는 최종 값이 char(s)에 저장
print([chr(s) for s in code_list2])
print([chr(s) for s in code_list3])
print([chr(s) for s in code_list4])

print()
print()

# Generator 생성
import array

# Generator : 한 번에 한 개의 항목을 생성(메모리 유지X)
tuple_g = (ord(s) for s in chars)
# Array : 한개의 자료형만 저장할 수 있고, 가변형 자료형이다. 자바의 new Array<String> 같은거
array_g = array.array('I', (ord(s) for s in chars))


# 표현식 기반 제너레이터 생성
# () 로 감싸져 있다고 해서 튜플이 아니다.
# st = [2 * i for i in range(1, 10)]  # 리스트 컴프리핸션하고 차이는 () 와 [] 의 차이일뿐이니 어렵게 생각하지 말자.
g1 = (2 * i for i in range(1, 10))
print(type(g1))
print(next(g1))
print(next(g1))

print("=================================")

print(type(tuple_g))
print(next(tuple_g))
print(type(array_g))
print(array_g.tolist())

print()
print()

# 제네레이터 : 한번에 많은 데이터를 로드하는게 아니라, 중도에 stop 로직을 통해 가능한 부분만큼 또는 필요한 만큼만 메모리에 로딩할 수 있다.
print(('%s' % c + str(n) for c in ['A', 'B', 'C', 'D'] for n in range(1, 11)))

for s in ('%s' % c + str(n) for c in ['A', 'B', 'C', 'D'] for n in range(1, 11)):
    print(s)

print()
print()

# 리스트 주의
marks1 = [['~'] * 5 for n in range(5)]  # ['~'] * 5 : 리스트 x 5, 사용하지 않는 n은 _로 치환 가능
marks2 = [['~'] * 5] * 5    # [] 안에 있을 때와 밖에 있을때가 결과가 전혀 다르다.

print(marks1)
print(marks2)

print()

# 수정
marks1[0][1] = 'X'
marks2[0][1] = 'X'

print(marks1)
print(marks2)

# 증명
print([id(i) for i in marks1])
print([id(i) for i in marks2])
