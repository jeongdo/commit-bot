class Father:
    def run(self):  # 달리기 능력이 있음!
        print("so fast!!")


class Son(Father):  # Father 클래스를 상속하는 Son 클래스
    def jump(self):  # 점프 능력이 자식은 있음
        print("so jump!!")


class Mother(object):
    def dive(self):  # 점프 능력이 자식은 있음
        print("so dive!!")


class Son2(Father, Mother):
    def jump(self):  # 점프 능력이 자식은 있음
        print("so jump!!")


def main():
    s = Son()
    s.run()
    s.jump()

    print("================")

    s2 = Son2()
    s2.run()
    s2.jump()
    s2.dive()


main()
