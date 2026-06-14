fs = '{0}....{1}...{2}'  # 번호 생략 가능
ms = fs.format('Roobt', 125, 'Box')

print(ms)

fs1 = '{}....{}...{}'  # 번호 생략 가능

ms = fs1.format('Roobt', 125, 'Box')

print(ms)

fs2 = '{toy}...{num}...{item}'.format(toy='Robot', num=12, item='Box')

print(fs2)


my = ['Robot', 125, 'Box']

fs3 = '{0}...{1}...{2}'.format(*my)    # 인자 전달 과정에서 리스트 대상으로 언패킹, {}

print(fs3)

my1 = ['Box', (24, 31)]
fs4 = '{0[0]}..{0[1]}..{1[0]}...{1[1]}'.format(*my1)
# {0}은 'Box' 이므로 {0[0]}은 'B', {0[1]}은 'o'
# {1}은 (24, 31) 이므로 {1[0]}은 24, {1[1]}은 31

print(fs4)

d = {'toy': 'Robot', 'price': 3500}
fs5 = '{0[toy]}, price={0[price]}'.format(d)    # 딕셔너리 값이 하나라서 0으로 지칭됨.

print(fs5)

print("===============")

# %[flags][width][.precision]f
print('{0}'.format(3.14))  # 정밀도 설정 없이 출력
print('{0:f}'.format(3.14))
print('{0:d}'.format(3))  # d는 값의 종류가 정수임을 명시하는 것
print('{0:.4f}'.format(3.14))   # 소수 이하 4자리까지만 출력
print('{0:9.4f}'.format(3.14))   # 9칸 확보, 소수 이하 4자리까지만 출력
print('{0:<9.4f}'.format(3.14))   # 9칸 확보, 소수 이하 4자리까지만 출력, 왼쪽 정렬
print('{0:>9.4f}'.format(3.14))   # 9칸 확보, 소수 이하 4자리까지만 출력, 오른쪽 정렬
print('{0:^9.4f}'.format(3.14))   # 9칸 확보, 소수 이하 4자리까지만 출력, 중앙 정렬
t1 = '%+d, %+d' % (5, -5)
print(t1)
print('{0:+d}, {1:+d}'.format(5, -5))
print('{:+}, {:+}'.format(5, -5))  # 0, 1, d  생략 가능
print('{0:*^10.4f}'.format(3.14))  # 중앙정렬, 빈 공간을 *로 채워라
print('{0:+<10}'.format(7))  # 왼쪽정렬, 빈 공간을 +로 채워라
print('{0:^^10}'.format('hi'))  # 중양정렬, 빈 공간을 ^로 채워라
