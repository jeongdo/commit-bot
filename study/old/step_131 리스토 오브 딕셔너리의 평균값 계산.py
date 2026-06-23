# 리스트 오브 딕셔너리

# [{}, {}, {}]

scores = [
    {"kor": 100, "eng": 100},
    {"kor": 88, "eng": 90},
    {"kor": 12, "eng": 33}
]

print(scores)
print()
for sc in scores:
    print(sc)  # 딕셔너리가 출력
print()

print("=== 국어 점수 출력 ===")
for sc in scores:
    print(sc["kor"])
print()

print("=== 각 학생들의 평균 점수 출력 ===")
for sc in scores:
    # print(sc["kor"] + sc["eng"])
    # print(sc["kor"])
    # print(sc["eng"])
    s_sum = sc["kor"] + sc["eng"]
    # print(sum)
    # print(len(sc.keys()))
    print(s_sum / len(sc.keys()))
    # print(sum(sc["kor"] + sc["eng"])/len(sc.keys()))

print()

print("=== 각 과목의 평균 점수 출력 1단계 ===")
ksum = 0
esum = 0
for sc in scores:
    ksum = ksum + sc["kor"]
    esum = esum + sc["eng"]
print(ksum / len(scores))
print(esum / len(scores))
print()

print("=== 각 과목의 평균 점수 출력 2단계===")

ksum = []
esum = []
for sc in scores:
    ksum.append(sc["kor"])
    esum.append(sc["eng"])

print(sum(ksum) / len(ksum))
print(sum(esum) / len(esum))
print()

print("=== 각 과목의 평균 점수 출력 3단계===")

ss = [[], []]
for sc in scores:
    ss[0].append(sc["kor"])
    ss[1].append(sc["eng"])
print(sum(ss[0]) / len(ss[0]))
print(sum(ss[1]) / len(ss[0]))
print()

print("=== 각 과목의 평균 점수 출력 4단계===")

ss = {"kor": [], "eng": []}

for sc in scores:
    for key in list(sc.keys()):
        ss[key].append(sc[key])

print(sum(ss["kor"]) / len(ss["kor"]))
print(sum(ss["eng"]) / len(ss["eng"]))
