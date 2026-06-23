print("===== 정수형 데이터와 문자열 =============")
s = 'I am ' + str(7) + ' years old'  # 문자열 조합
print(s)

print("===== print 함수의 문자열 결합 방식 (+와 ,) 비고 =============")

friends = [('Jung', 22), ('Hong', 23), ('Park', 24)]

for f in friends:
    print('My friend', f[0], 'is', f[1], 'years old.')
    print('My friend ' + f[0] + ' is ' + str(f[1]), 'years old.')

print("===== % 키워드 예제 (1)=============")

s1 = 'My name is %s' % 'Yoon'  # %s의 위치에 문자열 'Yoon'이 삽입됨, %d : 정수, %f : 실수

print(s1)

print("===== % 키워드 예제 (2)=============")

s2 = 'My friend %s is %d years old and %fcm tall.' % ('Jung', 22, 178.5)

print(s2)

print("===== % 키워드 예제 (3)=============")

for f in friends:
    print('My friend %s is %d years old.' % (f[0], f[1]))

s3 = 'My friend %s is %s years old and %scm tall.' % ('Jung', str(22), 178.5)
# %s가 등장하면 문자열 이외에 원하는 것 대부분 가져다 놓을 수 있다.

print("======== % 키워드의 자동 형변환 예시 ==========")

# 정수를 %f의 위치에 가져다 놓은 경우, 정수가 실수로 자동 변환된다.
# 실수를 %d의 위치에 가져다 놓은 경우, 실수가 정수로 자동 변횐된다.

print('%f' % 25)
print('%d' % 3.14)

print("===== % 키워드와 딕셔너리 예제 =============")

dic1 = "%(name)s : %(age)d" % {'name': 'Yoon', 'age': 22}
print(dic1)

print("======== 보다 세밀한 문자열 조합 지정방법 ==========")

# %[flags][width][.precision]f
# %[flags] : - 또는 0 또는 +를 넣어서 특별한 신호를 줌
# %[width] : 폭, 어느 정도 넓이를 확보하고 출력할지 결정
# [.precision] : 정밀도, 소수 이하 몇재 자리까지 출력할지 결정

print('height: %f' % 3.14)  # 정밀도 설정 없이 출력
print('height: %.3f' % 3.14)  # 소수점 이하 셋째 자리까지 출력
print('height: %.2f' % 3.14)  # 소수점 이하 둘째 자리까지 출력
print('height: %7.2f' % 3.14)  # 7칸 확보하고 그 공간에 3.14를 출력
print('height: %07.2f' % 3.14)  # 0이 플래그이다. 빈공간을 0으로 채움
print('height: %-7.2f' % 3.14)  # 왼쪽으로 붙혀서 출력, 좌측정렬
print('height: %+7.2f' % 3.14)  # + 기호를 같이 출력, 정렬과는 상관이 없다.

print("======== 총정리 ==========")

print('%(h)s: %(v)-+10.3f 입니다.' % {'h': 'height', 'v': 3.14})
