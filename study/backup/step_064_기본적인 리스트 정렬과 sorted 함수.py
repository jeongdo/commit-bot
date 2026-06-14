print('==== 리스트의 오름차순 정렬 =====')

ns = [3, 1, 4, 2]
ns.sort()  # 오름차순 정렬
print(ns)
print('==== 리스트의 내림차순 정렬 =====')
ns.sort(reverse=True)  # 내림차순 정렬을 위한 True의 전달
print(ns)

print('==== 오름차순 정렬의 함수의 사용자 정의 예시 =====')
ns1 = [('Yoon', 33), ('Lee', 13), ('Park', 20)]


def age(t):
    return t[1]  # 나이를 반환하는 함수


ns1.sort(key=age)
print(ns1)

print('==== 내림차순 정렬의 함수의 사용자 정의 예시 =====')
ns1.sort(key=age, reverse=True)
print(ns1)

print('==== 내림차순 정렬의 람다 함수의 사용자 정의 예시 =====')
ns2 = [('Yoon', 33), ('Lee', 13), ('Park', 20)]
ns2.sort(key=lambda t: t[1], reverse=True)
print(ns2)

print('==== 문자열 길이 순의 오름차순 정렬 예시 =====')
names = ['Julia', 'Yoon', 'Steven']
names.sort(key=len)

print(names)

print('==== 두 수의 합을 기준의 오름차순 정렬 예시 =====')
nums = [(3, 1), (2, 9), (0, 5)]
nums.sort(key=lambda t: t[0] + t[1], reverse=True)  # 두 수의 합을  기준
print(nums)

print('==== sorted 함수 사용하기 =====')
# sorted 함수 사용하기
org = [('Yoon', 33), ('Lee', 13), ('Park', 20)]
cpy = sorted(org, key=lambda t: t[1], reverse=True)  # 나이 기준 내림차순 정렬

print(org)  # 원본이 유지된다.

print(cpy)  # 정렬된 사본이 생성되었다.

print('==== sorted 함수를 튜플에 사용하기 (1) : 결과가 사본 리스트로 =====')
# 튜플의 사용 예

org = (3, 1, 2)
cpy = sorted(org)
print(org)
print(cpy)  # 튜플의 경우, 정렬 결과가 리스트에 담긴다.

print('==== sorted 함수를 튜플에 사용하기 (2) : 결과가 사본 튜플로 =====')
org = (3, 1, 2)
cpy = tuple(sorted(org))
print(org)
print(cpy)  # 원본과 동일한 자료형을 유지할 수 있게 된다.

print('==== sorted 함수를 튜플에 사용하기 (3) : 문자열의 첫 번째 문자인 3과 2와 1을 산술 비교 =====')
org = ('321', '214', '172')
cpy = tuple(sorted(org, key=lambda s: int(s[0])))
print(org)
print(cpy)  # 문자열의 첫 번째 문자인 3과 2와 1을 산술 비교 정렬한다.
