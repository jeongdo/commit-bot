# __name__ 같은 형태를 가지며, 파이썬에 의해 호출되는 (프로그래머가 그 이름을 직접 명시하여 호출하지 않는)
# 메소드를 가리켜, 스페셜 메소드(special methods) 라 한다.

t = (1, 2, 3)
print(len(t))       # t.__len__()

itr = iter(t)       # itr = t.__iter__()

for i in itr:
    print(i)

s = str(t)          # s = t.__str__()
print(s)