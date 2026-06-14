print("========= dict 기본적인 샘플 ============")
d = dict(a=1, b=2, c=3)

for k in d:  # k에는 키가 담긴다.
    print(d[k], end=', ')

print('\n')

print("========= dict.keys() 뷰 객체 반환 예시 ============")

# dict.keys()   # 딕셔너리의 키들만 참조하고자 할 때, 뷰 객체를 반환한다. (아이터레이터 객체이기도 하다.)
# dict.values() # 딕셔너리의 값들만 참조하고자 할 때, 뷰 객체를 반환한다. (아이터레이터 객체이기도 하다.)
# dict.items()  # 딕셔너리의 키와 값을 튜플형태로 참조하고자 할 때, 뷰 객체를 반환한다. (아이터레이터 객체이기도 하다.)

for j in d.keys():  # v에는 키가 담긴다.
    print(j, end=', ')

print('\n')

print("========= dict.values() 뷰 객체 반환 예시 ============")

for v in d.values():  # v에는 값이 담긴다.
    print(v, end=', ')

print('\n')

print("========= dict.items() - (1) 뷰 객체 반환 예시 ============")

for kv in d.items():
    print(kv, end=', ')

print('\n')

print("========= dict.items() - (2) 뷰 객체 반환, 튜플 언패킹 ============")

for k, v in d.items():  # 튜플 언패킹
    print(k, v, end=', ')

print('\n')

print("========= dict.items() - (3) 뷰 객체 반환를 대입 ============")

d1 = dict(a=1, b=2, c=3)
vo = d1.items()  # 뷰 객체 얻음

for kv in vo:
    print(kv, end=' ')

print('\n')

d1['a'] += 3
d1['c'] -= 2

print("========= dict.items() - (4) 뷰 객체 반환를 대입, 수정사항이 그대로 반영 됨. ============")

for kv in vo:  # 수정사항이 뷰 객체에 그대로 반영이 됨
    print(kv, end=' ')

print('\n')

print(d1)

