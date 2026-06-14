print("'abc' == 'abc' : ", 'abc' == 'abc')
print("'abc' != 'abc' : ", 'abc' != 'abc')
print("[1, 2, 3] == [1, 2, 3] : ", [1, 2, 3] == [1, 2, 3])
print("[1, 2, 3] != [1, 2, 3] : ", [1, 2, 3] != [1, 2, 3])

print()

st1 = "1243"
st2 = "adc12"
st3 = "허1"
st4 = "!#"

print('st1.isdigit() : ', st1.isdigit())  # 숫자로만 구성?
print('st2.isdigit() : ', st2.isdigit())  # 숫자로만 구성?
print('st1.isalpha() : ', st1.isalpha())  # 알파벳만 구성?
print('st1.isalpha() : ', st1.isalpha())  # 알파벳만 구성?
print('st1.isalnum() : ', st1.isalnum())  # 알파벳 또는 숫자로 구성?
print('st2.isalnum() : ', st2.isalnum())  # 알파벳 또는 숫자로 구성?
print('st3.isalnum() : ', st3.isalnum())  # 알파벳 또는 숫자로 구성?
print('st4.isalnum() : ', st4.isalnum())  # 알파벳 또는 숫자로 구성?


def main():
    phone_number = input("스마트폰 번호 입력 : ")
    if phone_number.isdigit() and phone_number.startswith("010"):
        print("정상적인 입력입니다.")
    else:
        print("정상적이지 않은 입력입니다.")


main()
