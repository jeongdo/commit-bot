sum = 0

for i in range(1, 11):  # 1~10 까지
    print(i)
    sum = sum + i

print(sum)
print("================================")
sum = 0

for i in range(1, 11, 1):
    print(i)
    sum = sum + i

print(sum)
print("================================")
sum = 0

for i in range(1, 11, 2):  # 다음 요소를 두단계씩 건너뛴다.
    print(i)
    sum = sum + i

print(sum)
print("================================")
sum = 0

for i in range(0, 10):  # 단순히 10회 반복, 0~9 실행
    print(i)
    sum = sum + i

print(sum)
print("================================")
sum = 0

for i in range(10):  # 단순히 10회 반복, range(0, 10) 가능
    print(i)
    sum = sum + i

print(sum)
print("================================")
