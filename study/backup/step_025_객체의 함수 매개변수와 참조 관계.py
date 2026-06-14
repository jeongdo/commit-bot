# 함수의 매개변수 참조 관계
def func(s):
    s[0] = 0
    s[-1] = 0


st = [1, 2, 3]

func(st)

# 리스트 객체라서 공유되네..
print(st)
