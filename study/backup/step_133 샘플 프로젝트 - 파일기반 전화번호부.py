import os

while True:

    print("원하시는 메뉴의 번호를 입력해주세요.")
    print("================================")
    print("1. 입력")
    print("2. 조회")
    print("3. 검색")
    print("4. 종료")
    print("================================")

    menu = input("선택 입력 : ")

    file_aba_path = os.path.abspath('../data/phones.txt')

    if menu == '1':
        f = open(file_aba_path, "a+", encoding="UTF-8")
        name = input("이름 : ")
        phone_num = input("전화번호 : ")
        data = name + " " + phone_num + "\n"
        f.write(data)
        f.close()
        print("%s %s 입력이 완료되었습니다. " % (name, phone_num), "\n")
    elif menu == '2':
        f = open(file_aba_path, "r", encoding="UTF-8")
        while True:
            line = f.readline().strip()
            if len(line) <= 0 or line == '':
                break
            else:
                print(line)
        f.close()
    elif menu == '3':
        search = input('검색하실 이름을 입력해주세요: ')
        f = open(file_aba_path, "r", encoding="UTF-8")
        search_results = []
        while True:
            # slist = f.readline().strip().split(" ") #홍길동 전화번호 --> ['홍길동', '전화번호']
            sline = f.readline().strip()
            if len(sline) == 0: break
            slist = sline.split(" ")
            if slist[0] == search:
                # print(slist[1]) # 전화번호 출력
                search_results.append(slist[1])
        if len(search_results) == 0:
            print("일치하는 전화번호가 존재하지 않습니다.")
        else:
            # print(search_results)
            for x in search_results:
                print(x)
        f.close()
    elif menu == '4':
        print("=== 프로그램을 종료합니다. ===")
        break
    else:
        print("=== wrong menu number ===")
