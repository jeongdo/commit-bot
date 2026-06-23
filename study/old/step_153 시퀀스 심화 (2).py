# Chapter04-02
# 파이썬 심화
# 시퀀스형 
# 컨테이너(Container : 서로다른 자료형[list, tuple, collections.deque], Flat : 한 개의 자료형[str,bytes,bytearray,array.array, memoryview])
# 가변(list, bytearray, array.array, memoryview, deque) vs 불변(tuple, str, bytes)
# 리스트 및 튜플 고급

# Tuple Advanced
# Unpacking

# b, a = a, b

print(divmod(100, 9))       # 100을 9로 나눈 몫과 나머지를 반환
# print(divmod((100, 9)))   # () 데이터는 오류 발생, *(100, 9) 같이 풀어서 전달해야 함.
print(divmod(*(100, 9)))
print(*(divmod(100, 9)))

print()

# x, y, rest = range(10)  #  에러 발생

x, y, *rest = range(10)
print(x, y, rest)
x, y, *rest = range(2)
print(x, y, rest)
x, y, *rest = 1, 2, 3, 4, 5
print(x, y, rest)

print()
print()

# Mutable(가변) vs Immutable(불변)

l = (15, 20, 25)
m = [15, 20, 25]

print(l, id(l))
print(m, id(m))

l = l * 2
m = m * 2

print(id(l))
print(id(m))    # 재할당

l *= 2
m *= 2

print(id(l))
print(id(m))    # 연산자의 활용에 따라 리스트는 메모리 위치가 같을 수 있다.

print()
print()

# sort vs sorted 
# reverse, key=len, key=str.lower, key=func..

# sorted : 정렬 후 새로운 객체 반환, 원본은 그대로 유지
f_list = ['orange', 'apple', 'mango', 'papaya', 'lemon', 'strawberry', 'coconut']

print('sorted -', sorted(f_list))
print('sorted -', sorted(f_list, reverse=True))
print('sorted -', sorted(f_list, key=len))
print('sorted -', sorted(f_list, key=lambda x: x[-1]))  # 문장의 마지막 단어를 기준으로 정렬 기준을 삼는다.
print('sorted -', sorted(f_list, key=lambda x: x[-1], reverse=True))
print()

print('sorted -', f_list)

print()

# sort : 정렬 후 객체 직접 변경, 원본이 변경

# 반환 값 확인(None)
print('sort -', f_list.sort(), f_list)
print('sort -', f_list.sort(reverse=True), f_list)
print('sort -', f_list.sort(key=len), f_list)
print('sort -', f_list.sort(key=lambda x: x[-1]), f_list)
print('sort -', f_list.sort(key=lambda x: x[-1], reverse=True), f_list)

# List vs Array 적합 한 사용법 설명
# List 리스트 기반 : 융통성, 다양한 자료형, 범용적 사용
# Array 숫자 기반 : 배열(리스트와 거의 호환)
