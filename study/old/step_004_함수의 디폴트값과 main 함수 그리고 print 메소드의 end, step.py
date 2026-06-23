def add(n1, n2):
    return n1 + n2


# 프로그램 실행 흐름을 하나로 묶어 두는 것이 의미가 있다.
def main():
    print(add(4, 5), end="\n")


main()


# age = 0 은 디폴트값 (값을 전달하지 않으면)
def who_are_you(name, age=0):
    print("이름 : ", name)
    print("나이 : ", age)


who_are_you(name="허정도")  # end="\n" 이부분을 이해했줘?

print(1, 2, 3, end="####\n")
print(1, 2, 3, sep=",")     # step 은 각 프린트 대상 요소 다음에 실행됨.
print(1, 2, 3, sep=",", end="$$$")
print()

print("============================")

for i in [1, 2, 3]:
    print(i, end='_')
print()
for i in [1, 2, 3]:
    print(i, end=' ')
