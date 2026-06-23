
# 파이썬의 예외처리 예시
def main():
    print("안녕")
    try:
        age = int(input("나이 입력해: "))
        print(age)
    except ValueError:
        print("실수나 문자 같은거 입력하지마. 일단 가고 다시 실행 해")

    print("잘가")


main()
