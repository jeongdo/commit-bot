# filter 함수는 값을 걸러내는 기능을 제공하는 함수이다.


def is_odd(n):
    return n % 2  # 2로 나누어 떨어지면 짝수이고 0이다. 0이면 false 이니, 우리가 구할려고 하는 건 홀수 == 1


st = [1, 2, 3, 4, 5]

ost = list(filter(is_odd, st))  # st를 대상으로 필터링이 됨.

print(ost)

print("================================================")
st1 = list(range(1, 11))

# not (n1 % 3)  : 3으로 나누어 떨어지면 0인데, 이것을 다시 부정했으니, 3으로 나누어 떨어지는 수를 구하라는 뜻.
fst = list(filter(lambda n1: not (n1 % 3), st1))  # not === ! 와 같은 의미

print(fst)

print("================================================")

# map(lambda n2: n2**2, st1) : 대상 파라미터 데이터 부터 생성
# 각 파라미터의 제곱수를 구해놓은 후에,  map(lambda n2: n2 ** 2, st1)) 를 iterator 객체로 대체하게 된다.
# 그다음 3으로 나누어 떨어지는 수를 필터한다.
# 그 결과 3의 배수3의 제곱, 6의 제곱, 9의 제곱
fst1 = list(filter(lambda n2: not (n2 % 3), map(lambda n2: n2 ** 2, st1)))

print(fst1)
