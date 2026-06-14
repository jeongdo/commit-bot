def main():
    print("안녕")
    while True:
        try:
            age = int(input("나이 입력해: "))
            print(age, 10 / age, " 입력 오케이!!")
            break
        # except ValueError as msg:
        #     print("실수나 문자 같은거 입력하지마. 다시 입력 해 >> ", msg)
        # except ZeroDivisionError as msg:
        #     print("0을 나눌 수가 없잖아. 다시 입력 해 >> ", msg)
        # finally: # 예외 발생해도 무조건 실행
        #     print("어쨋든 프로그램 종료")
        except:  # 엄청나게 많은 예외를 한번에 처리할때 사용
            print("뭐가 먼지 몰겠네 어쨋든 프로그램 종료")

    print("잘가")


main()

# ZeroDivisionError: division by zero # ZeroDivisionError 입력하면 된다.
