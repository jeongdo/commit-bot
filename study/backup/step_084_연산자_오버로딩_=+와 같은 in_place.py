n = 5
print(id(n))
print(n)

n += 1
print(n)  # 물론, 결과가 달라진건 맞는데.
# 정수와 문자열은 immutable 객체이다. 생성하고 나면 값을 바꿀 수 없다.

print(id(n))
# 왜 메모리 공간까지 달라졌지? n이 참조하는 객체가 바뀐 것이다.
# 즉, 새로운 객체가 만들어진 것 += 연산으로, 수정이 가능한 mutable 객체로의 변화가 일어난 것.


print("===============================================================")

n1 = [1, 2]
print(id(n1))
print(n1)

n1 += [3]
print(id(n1))   # 리스트의 경우는 주소값이 달라지지 않았다. mutable 겍체이기 때문이다.
print(n1)

print("==========Vector3의 __iadd__ 연산자(+=)의 오버로딩===============")


class Vector3:       # 수학의 벡터를 구조화한 클래스
    def __init__(self, x, y):
        self.x = x      # 벡터의 x 방향 값
        self.y = y      # 벡터의 y 방향 값

    def __add__(self, o):  # 벡터의 덧셈 연산
        return Vector3(self.x + o.x, self.y + o.y)       # 새로운 객체 생성 및 반환

    def __iadd__(self, o):  # 벡터의 += 연산
        self.x += o.x
        self.y += o.y
        return self         # v1 += v2의 연산 결과로 v1을 반환, 꼭 넣어줘야 한다. v1.__iadd__(v2), self 는 v1이 된다.
        # self 를 반환하지 않으면 연산은 잘 해놓고 v1은 텅 비는 상태가 될 수 있다.

    def __str__(self):    # 벡터 정보를 문자열로 반환
        return 'Vector3({0}, {1})'.format(self.x, self.y)


# +와 - 연산보다는 +=과 -= 연산이 더 어울려서 그 부분을 수정해보자.
class Account2:
    def __init__(self, aid, abl):
        self.aid = aid      # 계좌 번호
        self.abl = abl      # 계좌 잔액

    def __iadd__(self, m):   # 입금
        self.abl += m
        print('__iadd__')
        return self

    def __isub__(self, m):   # 출금
        self.abl -= m
        print('__isub__')
        return self

    def __str__(self):     # 계좌 상황을 문자열로 반환,  () 의 오버로딩이다.
        print('__str__')
        return '{0}, {1}'.format(self.aid, self.abl)


def main():
    v1 = Vector3(3, 3)
    print(v1, id(v1))
    v2 = Vector3(7, 7)
    v3 = v1 + v2  # 새로운 Vector 객체 생성되어 v3에 저장

    print(v1)
    print(v2)
    print(v3)
    v1 += v2
    print(v1, id(v1))

    print("=====================")

    acnt = Account2('James01', 100)  # 계좌 개설
    acnt += 100                      # 100원 입금, __iadd__ 호출로 이어짐          acnt.__iadd__(100)
    acnt -= 50                       # 50원 출금, __isub__ 호출로 이어짐           acnt.__isub__(50)
    print(acnt)                      # 계좌 정보 확인, __str__ 호출로 이어짐        acnt.__str__()


main()
