# 튜플과 레인지도 자료형의 일종이다.
for i in range(1, 11):  # 1<=i<11
    print(i)

r = range(1, 10)
print(9 in r)
print(10 not in r)

list1 = list((1, 2, 3))  # 튜플을 리스트로
print(list1)
list2 = list(range(1, 9, 3))  # 레인지를 리스트로
print(list2)

tuple1 = tuple([1, 2, 3])  # 리스트를 튜플로
tuple2 = tuple(range(1, 5, 2))  # 레인지를 튜플로
tuple3 = tuple("Hello")  # 문자열을 튜플로

print(tuple1)
print(tuple2)
print(tuple3)

print(list(range(10, 2)))  # 범위가 없으므로 빈공간, 1이 생략된 것과 같다.
print(list(range(10, 2, 1)))  # 범위가 없으므로 빈공간
print(list(range(10, 2, -1)))  # 10부터 1씩 감소하여 3까지 이르는 정수
print(list(range(10, 2, -2)))  # 10부터 2씩 감소하여 3까지 이르는 정수
print(list(range(10, 2, -3)))  # 10부터 3씩 감소하여 3까지 이르는 정수
