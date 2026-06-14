import os

# 절대 경로 구하기
abspath_01 = os.path.abspath('./sample.txt')
abspath_02 = os.path.abspath('../data/sample.txt')
abspath_03 = os.path.abspath('../data/')
abspath_04 = os.path.abspath('..')
print(abspath_01)
print(abspath_02)
print(abspath_03)
print(abspath_04)

# 상대 경로 구하기
# 절대 경로를 기준으로 한 상대경로를 구하는 구나!
print(os.path.relpath(abspath_02, './sample.txt'))
