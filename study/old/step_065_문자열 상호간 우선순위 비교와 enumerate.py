print('A' < 'Z')  # 알파벳 순서상 뒤로 갈 수록 크다.
print('AA' < 'AZ')  # 첫 번째 문자가 같다면, 두 번째 문자를 비교한다.
print('AA' < 'AAA')  # 비교하는 문자들이 모두 같다면, 하나라도 긴 문자열이 크다.
print('A' < 'a')  # 소문자가 대문자보다 크다.

print("===========")

print('가' < '나')  # 가나다순으로 뒤로 갈수록 크다.
print('가' < '구')  # 아야어여오요~ 순으로 뒤로 갈수록 크다.
print('가가' < '가나')  # 첫 번째 문자가 같다면 두 번째 문자를 비교한다.
print('하하' < '하하하')  # 비교하는 문자들이 모두 같다면 하나라도 긴 문자열이 크다.

print("===== 딕셔너리로 순번을 저장한 문자열 ======")

names = ['박선주', '윤나은', '이지선', '장현지', '김현주']

names.sort()

print(names)

dnames = {}
i = 1

for n in names:
    dnames[i] = n  # i와 n을 각각 '키'와 '값'으로 해서 딕셔너리에 저장
    i += 1

print(dnames)

print("===== enumerate : 자동으로 0번부터 번호가 매겨짐 ======")

names2 = ['박선주', '윤나은', '이지선', '장현지', '김현주']
eo = enumerate(names2)  # iterator 객체인 enumerate 객체 반환

for n in eo:    # eo 에 담긴 것은 iterator 객체이므로 for 루프에 올 수 있음
    print(n)

print("===== enumerate : 10 부터 번호 매김 ======")

for n in enumerate(names2, 10):    # 10번부터 번호를 매기기 시작
    print(n)

print("===== enumerate와 딕셔너리 컴프리헨션 ======")

# 위의 예시 처럼 enumerate(sorted(names2), 1) 값들은 튜플로 꺼내지고,
# enumerate(sorted(names2), 1) 값이 k, v로 튜플 언패킹이 이뤄지며, 딕셔너리 컴프리헨션이 완성된다.
dnames2 = {k: v for k, v in enumerate(sorted(names2), 1)}

print(dnames2)
