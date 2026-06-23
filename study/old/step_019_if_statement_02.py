def main():
    print("main function")

    num = 24

    # if num % 2 == 0:
    #     if num % 3 == 0:
    #         print("2의 배수이면서, 3의 배수입니다.")
    #     else:
    #         print("2의 배수입니다.")
    # else:
    #     print("2의 배수도 3의 배수도 아닙니다.")

    if (num % 2) == 0 and num % 3 == 0:
        print("2의 배수이면서, 3의 배수입니다.")
    else:
        print("2의 배수도 3의 배수도 아닙니다.")

    # and (java의 &&), or (java의 ||) 처럼 그냥 문장으로 쓰는구나!

    if not True:
        print("no True!")
    else:
        print("not True!")

    # not (java의 !)


main()
