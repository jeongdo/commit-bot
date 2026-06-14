# 리스트 오브 리스트 [[]]
list = [[11, 2, 3], [64, 1, 1], [13, 1, 2]]
print(list)
print("====================================")
for score in list:
    # print(score[0])
    print(sum(score))
    print(sum(score) / len(score))
    for s in score:
        print(s)

print("==== 국, 영, 수 각 평균을 구하시오. ====")
ksum = 0
esum = 0
msum = 0
for idx in list:
    print(idx[0])
    print(idx[1])
    print(idx[2])

print("==== 1단계 ====")
for idx in list:
    ksum = ksum + idx[0]
    esum = esum + idx[1]
    msum = msum + idx[2]

print(ksum / len(list))
print(esum / len(list))
print(msum / len(list))

print("==== 2단계 ====")

ksum = []
esum = []
msum = []
for idx in list:
    ksum.append(idx[0])
    esum.append(idx[1])
    msum.append(idx[2])

print(sum(ksum) / len(ksum))
print(sum(esum) / len(esum))
print(sum(msum) / len(msum))

print("==== 3단계 ====")

ss = [[], [], []]
for idx in list:
    ss[0].append(idx[0])
    ss[1].append(idx[1])
    ss[2].append(idx[2])
print(sum(ss[0]) / len(ss[0]))
print(sum(ss[1]) / len(ss[0]))
print(sum(ss[2]) / len(ss[0]))

print("==== 4단계 ====")

for idx in list:
    for i in range(0, len(ss)):
        ss[i].append(idx[i])

for i in range(0, len(ss)):
    print(sum(ss[i]) / len(ss[i]))