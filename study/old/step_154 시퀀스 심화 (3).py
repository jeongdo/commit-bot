# 파이썬 심화
# 시퀀스형
# 해시테이블(hashtable) -> 적은 리소스로 많은 데이터를 효율적으로 관리
# Dict -> Key 중복 허용 X, Set -> 중복 허용 X
# Dict 및 Set 심화

# Dict 구조
# print(__builtins__.__dict__)

print()
print()

# Hash 값 확인
t1 = (10, 20, (30, 40, 50))
t2 = (10, 20, [30, 40, 50])

print(hash(t1))
# print(hash(t2)) # 예외 발생 : 리스트는 해쉬값으로 뽑아 낼 수 없다. 리스트가 값을 바꿀 수 있기 때문이다.

print()
print()

# Dict Setdefault 예제        : Setdefault 속도 향상
source = (('k1', 'val1'),
          ('k1', 'val2'),
          ('k2', 'val3'),
          ('k2', 'val4'),
          ('k2', 'val5'))

new_dict1 = {}
new_dict2 = {}

# No use setdefault
for k, v in source:
    if k in new_dict1:
        new_dict1[k].append(v)
    else:
        new_dict1[k] = [v]

print(new_dict1)

# Use setdefault
for k, v in source:
    new_dict2.setdefault(k, []).append(v)
    # {'k1': ['val1', 'val2'], 'k2': ['val3', 'val4', 'val5']}

print(new_dict2)

# 주의
new_dict3 = {k: v for k, v in source}   # {'k1': 'val2', 'k2': 'val5'}, 키 중복이 덮어 써버린다.

print(new_dict3)

print()
print()
