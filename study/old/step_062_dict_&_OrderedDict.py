from _collections import OrderedDict

print('==== 3.7 이상의 dict의 저장순서 보전 확인 =====')

# 3.7 부터는 dict에 입력되는 순서를 보장하기 시작했다.

d = {}
d['a'] = 1
d['b'] = 2
d['c'] = 3

print(d)

for kv in d.items():
    print(kv)

# 3.7 이전의 경우
print('==== 3.7 이전의 경우 저장순서를 보전하기 위한 OrderedDict 확인 =====')

od = OrderedDict()  # OrderedDict 객체 생성
od['aa'] = 1
od['bb'] = 2
od['cc'] = 3

print(od)

for kv in od.items():
    print(kv)


print('==== 3.7 이전의 경우 저장순서를 보전하기 위한 OrderedDict 확인 =====')

d2 = dict(c=3, a=1, b=2)

print(d2)

print('==== dict의 저장순서와 동일객체 여부 확인 =====')
print(d == d2)  # True : d와 d2는 저장 순서는 다르고, 내용물은 같다.

print('==== OrderedDict 저장순서와 동일객체 여부 확인 =====')
od1 = OrderedDict(cc=3, aa=1, bb=2)

print(od1)

print(od == od1)  # 내용물은 같지만, 저장순서가 달라. False 반환,
# 딕셔너리의 저장 순서가 객체 구분에 의미를 갖는 상황이라면 OrderedDict을 사용해야 한다.

print('==== OrderedDict move_to_end 메소드 =====')
od1.move_to_end('cc')  # 키값 bb 데이터를 맨 끝으로 보내기

for kv in od1.items():
    print(kv)

print('\n')

print('==== OrderedDict move_to_end 메소드 값은 맨앞으로 보내기=====')
od1.move_to_end('bb', last=False)  # 매개변수 last에 False 전달하면 맨 앞으로 이동

for kv in od1.items():
    print(kv)
