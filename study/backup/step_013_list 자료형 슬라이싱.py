list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
list2 = list1[2:5]
print(list2)
print(list1)  # 원본은 사라지지 않는다.

print("==============================")

list1[2:5] = [0, 0, 0, 0, 0, 0]
print(list1)  # 늘릴수도 있고, 줄일수도 있다. 슬라이싱 연산

print("==============================")

list1[0:3] = [0, 0, 0]  # list1[:3] 동일
print(list1)

print("==============================")

list1[:] = []  # list1[:], 첫번째는 0, 마지막 없는 건 끝,
print(list1)

print("==============================")

list3 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
list4 = list3[0::2]  # 2칸씩 건너뛴다. 3이면 3칸씩 이동
print(list4)
# list3[0::2] = [1, 2, 3]  # 지정범위보다 데이터가 적어서 에러 발생, attempt to assign sequence of size 3 to extended slice of size 5
