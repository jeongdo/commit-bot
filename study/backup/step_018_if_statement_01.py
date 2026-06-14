def main():
    print("main function")

    # 한줄 처리
    if (2 > 10): print("실행안됨 : 거짓입니다.")

    if (2 > 10):
        print("참입니다.")
    else:
        print("거짓입니다.")

    if (2 > 10):
        print("참입니다.")
    elif (3 < 10):
        print("elif (elseif) : 참입니다.")
    else:
        print("거짓입니다.")


main()
