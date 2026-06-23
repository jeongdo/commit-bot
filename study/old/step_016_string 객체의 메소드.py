# 문자열도 객체이다. 원본은 그대로 있고, 관련 객체함수는 새로운 문자열을 만든다.
str = "허허허허정도"
print(str.count("허"))  # '허' 가 몇번 등장?
print(str.count("허정"))  # '허정' 가 몇번 등장?
print("======================================")
org = " Koon "
print(org.lower())
print(org.upper())
print(org)  # 원본은 그대로이다.
print("======================================")
print(org.lstrip())  # 왼쪽 공백 제거
print(org.rstrip())  # 오른쪽 공백 제거
print(org.strip())  # 양쪽 공백 제거
print(len(org.strip()))  # 양쪽 공백 제거 후 문자열의 길이
print("======================================")
print(org.replace("oo", "kk"))  # 첫 번째만 바꾸기
print(org.replace("o", "i", 1))  # 대상의 한개만 바꾸기
print(org.replace("o", "i", 2))  # 대상의 두개까지만 바꾸기
print(org)
print("======================================")
str1 = "ab_cd_ef"
print(str1.split('_'))  # 대문 문자기준으로 문자열을 분리하고 각각의 새로운 문자열을 리스트로 반환된다
print("======================================")
str2 = "aaa bbb ccc find aaa is ddd aaakk aft the goog bbb"
print(str2.find("bbb"))  # bbb 있는 위치의 인덱스 값 반환, 없으면 -1
print(str2.rfind("bbb"))  # 마지막 bbb가 있는 위치를 찾는다. 끝부터 찾는다. 없으면 -1
print(str2.startswith("aaa"))
print(str2.endswith("bbb"))
print("======================================")
str3 = "aaa\nbbb"  # escape 시퀀스 : \n (줄바꿈), \t (탭), \' (작은 따옴표), \" (끈 따옴표)
print(str3)  # 줄바꿈을 그대로 표현하여 출력한 경우
print("======================================")
str3 = "제가 마음속으로 그랬습니다. \"이건 아니야\"라고 말이죠."
print(str3)
print("======================================")
