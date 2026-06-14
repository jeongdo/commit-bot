# 자료형의 분류

# 1) 시퀀스 타입 : 리스트, 튜플, 레인지, 문자열(text sequence type)
#   저장된 값의 순서가 보전된다는 것이 이 자료형 유형들의 특징이다.
#   그래서 인덱싱 연산(특정 값을 참조하는 연산)과 슬라이싱 연산(시작과 끝을 정하여 이를 참조하는 연산)이 가능하다.

# 2) 매핑 타입 (mapping type)
#   딕셔너리
#   set : 저장된 값을 수정할 수 있는 mutable 객체
#   frozenset : immutable 객체

print('==== set 생성 예시외 연산 =====')

a = {'a', 'c', 'd', 'f'}
print(a)
print(type(a))  # 이것이 딕셔너리와 set에서 동시에 쓰인다.
b = {'a', 'b', 'd', 'f'}

print(a - b)  # a에 대한 b의 차집합 (A-B)
print(a & b)  # a와 b의 교집합 (AnB)
print(a | b)  # a와 b의 합집합 (AUB)
print(a ^ b)  # a와 b의 대칭 차집합 (A-B) U (B-A)

print('==== set 생성방법 2가지  =====')

c = set(['a', 'c', 'd', 'f'])  # set 함수에 iterable 객체 전달해서 set 생성
d = set('fdca')  # 문자열도 iterable 객체이므로 이를 통해 set 생성 가능`

print(c)
print(d)

print('==== set은 내용물만 같으면 일치한다.  =====')

print(c == d)  # 저장순서는 상관없다. 내용물만 같으면 true

print('==== set 자료형의 데이터 여부 판단  =====')

print('a' in a)  # 집함 a에 원소 'a' 가 포함되어 있는가?
print('b' not in a)  # 집함 a에 원소 'b' 가 포함되어 있지 않는가?

print('==== a&b의 결과로 얻은 set을 대상으로 for 루프 구성  =====')

for e in a & b:  # a&b의 결과로 얻은 집합을 대상으로 for 루프 구성
    print(e, end=' ')


print()
print('==== 빈 딕셔너리 만들기  =====')
di = {}  # 이것이 딕셔너리와 set에서 동시에 쓰인다.
print(di)
print(type(di))
print('==== 빈 set 만들기  =====')

s = set()  # 그래서 빈 set 만들기도 알아보자.

print(s)

print('==== frozenset 생성 예시외 연산 =====')

# frozenset 도 set 생성과 동일하다. frozenset은 set의 수정불가 객체 버전이다

a1 = frozenset(['a', 'c', 'd', 'f'])
b1 = frozenset(['a', 'b', 'd', 'f'])

print(a1 - b1)  # 이 예제는 set과는 차이가 없다.

print('==== set을 이용한 리스트의 중복 데이터 방지 연산 =====')

# 중복 데이터 제거
t = [3, 3, 4, 4, 1, 1, 'z', 'z']
t = list(set(t))

print(t)

print('==== set의 객체 메소드 add, discard 예시 (frozenset은 안됨) =====')

os = {1, 2, 3, 4, 5}
os.add(6)  # 원소 6을 집합에 추가
os.discard(1)  # 원소 1을 집합에서 제거

print(os)

print('==== set의 객체 메소드 수정 연산 예시 (frozenset은 안됨) =====')

os.update({7, 8, 9})  # 집합에 {7, 8, 9}의 모든 원소 추가

print(os)

os &= {2, 4, 6, 8}  # 집합 os에 {2, 4, 6, 8}와 겹치는 원소만 남김

print(os)

os -= {2, 4}  # 집합에 {2, 4}의 원소를 모두 삭제

print(os)

os ^= {1, 3, 6}  # 집합에서 {1, 3, 6} 에 있는 원소는 빼고 없는 원소는 추가

print(os)

# set 컴프리헨션
print('==== set 컴프리헨션 =====')

s1 = {x for x in range(1, 11)}
print(s1)

s2 = {x ** 2 for x in s1}
print(s2)

s3 = {x for x in s2 if x < 50}
print(s3)
