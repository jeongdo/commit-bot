def main():
    cnt = 0
    while cnt < 10:
        print(cnt, end='\n')
        cnt = cnt + 1
        if cnt == 8:
            break


main()
print("======================================")

for i in range(1, 11):
    # if i % 2 == 0:
    #     continue
    if i % 2 == 0:
        continue
    print(i, end='\n')

print("======================================")

for i in [1, 2]:
    for j in ['a', 'b', 'c']:
        print(j * i, end=' ')

print("======================================")

# 문자열 자체로 for 문을 실행할 수 있다.
# 다음 문자열의 r의 총 갯수는?
sr = ['father', 'mother', 'brother']
cnt = 0
for s in sr:
    for c in s:
        if c == 'r':
            cnt += 1
            continue

print(cnt)
