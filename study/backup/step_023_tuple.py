# 튜플과 레인지도 자료형의 일종이다.

list1 = [1, 2, 3]  # mutable 객체 (수정가능)
tuple1 = (1, 2, 3)  # 문자열도 immutable, immutable 객체는 수정불가이다. 값을 조회는 가능하지만, 값의 변형은 불가

print(list1)
print(tuple1)
print(type(list1))
print(type(tuple1))

# 바꾸지 못하는 데이터를 넣자.
test_data = [('동수', 1213), ('정수', 2213), ('수정', 2313)]

print(test_data[0][1], end="\n")

# 튜플도 리스트와 거의 같은 객체함수를 가진다.
print(len(test_data), end="\n")

print((1, 2, 3) + (4, 5))  # 수정 : 새로운 생성이기에 가능하다.  # test_data + (4, 5) : 안됨.
print(test_data * 2)  # 수정 : 새로운 생성이기에 가능하다.
print(test_data[0:1])  # 수정 : 새로운 생성이기에 가능하다.

for i in (1, 32, 3, 4):
    print(i)
