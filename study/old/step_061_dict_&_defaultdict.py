from _collections import defaultdict  # defaultdict는 collections 모듈의 함수

print('==== 딕셔너리의 defaultdict 설명 =====')

s = 'robbot'

d2 = defaultdict(int)
print('==== 딕셔너리의 defaultdict으로 만든 빈 딕셔러니 객체 확인 =====')

print(d2)

print('==== 딕셔너리의 defaultdict에서 키만 설정한 예시 확인 =====')

d2['t'];   # 키값만 설정

print(d2)

print('==== 딕셔너리의 defaultdict으로 내부 객체값을 매핑할 때 키가 없다고 예외를 발생하지 않음 예시 =====')

# 딕셔너리의 defaultdict
# 이 딕셔너리는 찾는 키가 없으면 예외를 발생시키지 않고 해당 키를 추가하되,
# 미리 등록해 놓은 함수가 반환하는 디폴트 값을 그 키의 값으로 저장한다.

for k in s:
    d2[k] += 1  # 디폴트 메서드로 int 함수가 장착하고 defaultdict 호출, 키가 없으면, 디폴트 메서드 호출, r=0을 등록하고, +=1 연산 진행

print(d2)

print('==== 딕셔너리의 defaultdict의 int 메소드의 설명 =====')

n1 = int('36')  # 문자열을 정수로 반환해서 반환하는 int 함수
print(n1)

n2 = int()  # 아무 값도 전달하지 않으면 0을 반환하는 int 함수
print(n2)

print('==== 딕셔너리의 defaultdict의 사용자 정의 함수 예시 =====')


def ret_zero():
    return 0


zero = defaultdict(ret_zero)
zero['a']  # 해당 키가 없으므로 이 순간 'a':0 등록됨

print(zero)

print('==== 딕셔너리의 defaultdict의 사용자 정의 함수를 람다로 작성 예시 =====')

d4 = defaultdict(lambda: 7)  # 실제로 이런 상황에서는 람다식을 작성하는 것이 깔끔
d4['z']

# 람다를 풀어쓰면 아래와 같다.
# def lamda_test():
#     return 7
#
#
# d4 = defaultdict(lamda_test)
# d4['z']

print(d4)
