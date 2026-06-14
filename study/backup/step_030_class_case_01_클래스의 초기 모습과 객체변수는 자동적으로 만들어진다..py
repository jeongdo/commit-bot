from clazz.ageinfo_01 import AgeInfo


def main():
    father = AgeInfo()                  # father 이름의 AgeInfo 객체 생성
    father.age = 39                     # 인스턴스 변수, 파이썬이 현재는 알아서 age 변수를 넣어준다.
    print("아버지 나이", father.get_age())     # 인스턴스 메소드
    father.up_age()
    AgeInfo.up_age(father)              # 이런식으로 전달이 됨을 보여준다.
    print("아버지 나이", father.get_age())

    mom = AgeInfo()
    mom.age = 30
    print("어머니 나이", mom.get_age())


main()
