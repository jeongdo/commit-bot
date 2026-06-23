# step_003_간단한 함수 만들기.py 먼저 참조
cnt = 200


def var1(t):
    # cnt = 0
    global cnt  # 사용빈도는 낮을것이다.
    t += 1
    cnt += 30  # local variable 'cnt' referenced before assignment
    print(t)


var1(cnt)  # 201

# print(t) # name 't' is not defined
print(cnt)  # 230
