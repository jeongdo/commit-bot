# for loop

for x in [1, 2, 3, 4, 5]:
    print(x)

print("===================")

# 100은 출력되지 않는다.
for x in range(1, 100, 1):
    print(x)

print("===================")

# range
sum1to10 = range(1, 10, 1)
# 범위값만을 돌려준다.
print(sum1to10)
print("===================")
# 리스트로 형변환 : *list, 딕셔너리로 형변환 : **dictionary
print(*sum1to10)

data = [1, 2, 3, 4, 5]

print("===================")

for x in data:
    print(x)

# 에러 구문이다. 그냥 단순한 리스트의 길이 숫자일 뿐
# for x in len(data):
#     print(data[x])
# 그래서 range 함수를 쓰는 것
print("===================")
for x in range(0, len(data)):
    print(data[x])

print("===== 중첩 for 예시 =====")

for a in ['a', 'b', 'c']:
    print(a, end=" : ")
    for x in [1, 2, 3, 4, 5]:
        print(x, end=" ")

print()
print("===== 중첩 for 구구단 =====")

for a in range(1, 10, 1):
    for b in range(2, 10, 1):
        result = a * b
        if result >= 10:
            end = "  "
        else:
            end = "   "
        print(b, "x", a, "=", result, end=end)
    print()

print("===== 중첩 while 문 구구단 =====")

a = 1
b = 2
while True:
    while True:
        result = a * b
        if result >= 10:
            end = "  "
        else:
            end = "   "
        print(b, "x", a, "=", result, end=end)
        b = b + 1
        if b >= 10:
            b = 2
            print()
            break
    a = a + 1
    if a >= 10:
        break

