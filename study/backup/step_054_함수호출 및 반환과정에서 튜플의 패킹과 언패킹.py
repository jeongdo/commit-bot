print("========= 함수 반환과정에서 튜플의 패킹 (1) ============")


def ret_nums():
    return 1, 2, 3, 4, 5  # 튜플의 소괄화가 생략된 형태, 즉, 패킹되어 튜플 형태로 반환됨


nums = ret_nums()
print(nums)

print("========= 함수 반환과정에서 튜플의 패킹 (2) ============")

n, *others = ret_nums()
print(n)  # 최초의 하나가 들어온다.
print(others)  # 나머지는 리스트로 묶인다.

print("========= 매개변수의 튜플의 패킹 (1) ============")


# 매개변수도 묶인다.

def show_nums(n1, n2, *other):  # 세 번째 이후 값들은 튜플로 묶여 *other 에 전달
    print(n1, n2, other, sep=', ')


show_nums(1, 2, 3, 4)
show_nums(1, 2, 3, 4, 5)

print("========= 매개변수의 튜플의 패킹 (2) ============")


# 전달되는 모든 값들을 하나의 튜플로 묶여서 nums에 저장
def sum(*nums):
    s = 0
    for i in nums:
        s += i
    return s


print(sum(1, 2, 3, 4))

print("========= 함수 반환과정에서 튜플의 패킹 (4) ============")


# * -> 푼다. (함수를 호출할 때)

def show_man(name, age, height):
    print(name, age, height, sep=', ')


p = ('Yo0n', 22, 180)

show_man(*p)  # p에 담긴 값을 풀어서 각각의 매개변수로 전달

p = ['Yo0n', 22, 180]  # 리스트도 마찬가지이다.

show_man(*p)

print("========= 튜플안에 튜플이 있을 때 언패킹 ============")

t = (1, 2, (3, 4))

a, b, (c, d) = t  # 튜플 안의 값의 구조와 동일한 형태로 변수를 선언한다.

print(a, b, c, d, sep=', ')

print("========= 튜플안에 튜플에서 소괄호를 생략한 경우 ============")

pp = 'Hong', (32, 178), '010-1234-56xx', 'Korea'
na, (ag, he), ph, ad = pp
print(na, he)

print("========= 불필요한 정보가 담길 곳에는 _ 로 처리 해도 무방 ============")

na, (_, he), _, _ = pp
print(na, he)

print("========= for 루프에서의 언패킹 (1) ============")

ps = [('Lee', 172), ('Lee', 182), ('Lee', 179)]  # 리스트에 담긴 튜플, 3번의 튜플 언패킹이 진행된다. ([], []) 구조도 동일하게 이뤄진다.
for n, h in ps:
    print(n, h, sep=', ')

print("========= for 루프에서의 언패킹 (2) ============")

ps = (['Lee', 172], ['Lee', 182], ['Lee', 179])  # 튜플에 담긴 리스트
for n, h in ps:
    print(n, h, sep=', ')