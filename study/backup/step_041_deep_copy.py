import copy     # deepcopy  함수 호출 위해서 copy 모듈 import

# 깊은 복사
r5 = ['John', ('man', 'USA'), [175, 23]]
r6 = copy.deepcopy(r5)
r6[2][1] += 1  # 나이 한살 더 먹음

print(r5)

print(r6)

print("================================================")

print((r5[0] is r6[0]) and (r5[1] is r6[1]))  # 얕은 복사 확인, 문자열과 튜플은 얕은 복사만

print((r5[2] is r6[2]))  # 깊은 복사 확인, 리스트는 깊은 복사가 가능해져, r5와 r6이 차이가 난다.

# 결론, deepcopy 함수의 호출 결과로, immutable 객체를 대상으로는 얕은 복사가 진행되었고, mutable 객체를 대상으로는 깊은 복사가 진행된다.

print("================================================")

# 다음방식으로 튜플이나 문자열을 복사하면 얕은 복사가 진행된다.

d1 = (1, 2, 3)
d2 = 'Please'

c1 = tuple(d1)
c2 = str(d2)

print(d1 is c1)
print(d2 is c2)
