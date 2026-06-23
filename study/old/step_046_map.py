def pow(n):
    return n ** 2


st1 = [1, 2, 3]
st2 = [pow(st1[0]), pow(st1[1]), pow(st1[2])]  # 되긴 되는데...

print(st2)

print("================================================")

# 첫 번째는 실행함수, 두 번째는 리스트 : 리스트 각 요소를 하나씩 꺼내서 함수에 전달
# 최종적으로 map 이 값을 꺼낼 수 있는 iterator 객체가 반환된다.

print(type(map(pow, st1)))

print(map(pow, st1))

st3 = list(map(pow, st1))

print(st3)

print("================================================")

ir = map(pow, st3)

for i in ir:
    print(i, end='\n')

print("================================================")


# 튜플과 문자열로 map에 전달 가능

def dbl(e):
    return e * 2


print(list(map(dbl, (1, 2, 3))))

print(list(map(dbl, 'hello')))  # 문자를 정수로 곱하면 해당 정수만큼의 문자열이 된다.


print("================================================")


# 매개변수가 여러개인 함수의 map 함수 처리
def sum(n1, n2):
    return n1 + n2


st4 = [1, 2, 3]
st5 = [3, 2, 1]

st6 = list(map(sum, st4, st5))

print(st6)
