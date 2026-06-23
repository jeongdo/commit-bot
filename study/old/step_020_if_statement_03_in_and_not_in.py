def main():
    print("main function")

    str = "Tomato Spaghetti"

    if str.find("mato") != -1:
        print("mato 있음")
    else:
        print("없음")

    if "ghe" in str:
        print("ghe 있음")
    else:
        print("ghe 없음")

    if "ghe" not in str:
        print("ghe 없음")
    else:
        print("ghe 있음")

    if "ghe11" not in str:
        print("ghe11 없음")
    else:
        print("ghe11 있음")

    print(bool(0))  # False
    print(bool(5))
    print(bool(""))  # False
    print(bool("kkk"))
    print(bool([1, 2, 3]))
    print(bool([]))  # False

    # 0제외 모든 값은 true
    if "111":
        print("문자열 111이 true이다.")

    if 90:
        print("숫자 90이 true이다.")

    if 0:
        print("0이 true 이다.")
    else:
        print("0은 false 이다.")

    num = 1

    if num != 0:
        print("num은 0이 아니다.")

    if num:
        print("num은 0이 아니다. 이게 좀더 세련!")

    print(3 in [1, 2, 3])
    print(3 not in [1, 2, 3])


main()
