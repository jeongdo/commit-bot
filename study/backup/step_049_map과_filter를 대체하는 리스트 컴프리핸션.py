st1 = [1, 2, 3, 4, 5]

# st2 = list(map(lambda n : n**2, st1))
st2 = [n ** 2 for n in st1]

print(st2)

print("================================================")

# ost = list(filter(lambda n1: n1 % 2, st1))
ost = [n for n in st1 if n % 2]
print(ost)

print("================================================")

st5 = list(range(1, 11))
# st5 대상으로 n % 2 : 홀수만 대상이란 뜻, 짝수면 0이니, false 필터 대상이 되지 않음.
# fst = list(map(lambda n: n ** 2, filter(lambda n: n % 2, st5)))

# for n in st5 : 데이터를 가져와 n에 넣는 것 부터 시작
# 필터는 if n % 2 절로 대신한다.
# 맵은 n ** 2 로 대신한다.
fst = [n ** 2 for n in st5 if n % 2]
print(fst)
