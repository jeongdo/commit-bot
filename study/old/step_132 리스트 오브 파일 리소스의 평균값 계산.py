# 리스트 오브 file 리소스
import os

file_aba_path = os.path.abspath('../data/score.txt')

f = open(file_aba_path, "r")

line_cnt = 1

while True:
    line = f.readline().strip()
    if len(line) <= 0 or line == '':
        break
    # print(line)
    # print(line.split(","))
    items = line.split(",")
    sum = 0
    for i in items:
        # print(int(i))
        sum = sum + int(i)
    # print(line_cnt, "번 학생의 합계 : ", sum, end = ", ")
    # print(line_cnt, "번 학생의 평균 : ", sum / len(items))
    print("합계: %d  평균 : %f" % (sum, sum / len(items)))
    print()
    line_cnt = line_cnt + 1
