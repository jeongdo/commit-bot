# >>> 3.14
# 3.14
# >>> H
# Traceback (most recent call last):
#   File "<input>", line 1, in <module>
# NameError: name 'H' is not defined
# >>> [1, 2, 3]
# [1, 2, 3]
# >>> type([1,2,3])
# <class 'list'>

[1, "hello", 'hello', 4]

[1, ["hello", 'hello'], 4]

list1 = [1, 2, 3] + [4, 5]  # 뒤쪽에 항목이 추가된다.
print(list1)

list2 = [1, 2, 3] * 2  # 뒤쪽에 항목이 추가된다.
print(list2)

list3 = [1, 2, 3, 4, 5]
n1 = list3[0]
print(n1, list3[4])
print(n1, list3[4 - 1])
print(n1, list3[-1], list3[-2])  # 리스트의 마지막 값 -1은 자주 사용한다. 0에서 다시 -로 위치를 재부여
