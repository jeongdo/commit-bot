def main():
    print("안녕")
    while True:
        try:
            age = int(input("나이 입력해: "))
            print(age, 10 / age, " 입력 오케이!!")
            break   # 입력이 정상이면 while 루프를 탈출!
        except ValueError as msg:       # 변수 msg 오류 메시지가 담긴다.
            print("실수나 문자 같은거 입력하지마. 다시 입력 해 >> ", msg)
        except ZeroDivisionError as msg:
            print("0을 나눌 수가 없잖아. 다시 입력 해 >> ", msg)
        finally:  # 예외 발생해도, 발생하지 않아도 무조건 실행
            print("어쨋든 프로그램 종료")

    print("잘가")


main()

# ZeroDivisionError: division by zero # ZeroDivisionError 를 입력하면 된다.
