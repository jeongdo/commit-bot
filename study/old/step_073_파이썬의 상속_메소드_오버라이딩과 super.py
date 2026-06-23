class Father:
    def run(self):  # 달리기 능력이 있음!
        print("so fast!!")


class Son(Father):  # Father 클래스를 상속하는 Son 클래스
    def run(self):  # 달리기 능력을 더욱 증가시킨다.
        print("so so fast!!")
    def jump(self):  # 점프 능력이 자식은 있음
        print("so jump!!")
    def father_run(self):
        super().run()


def main():
    s = Son()
    s.run()
    s.father_run()
    s.jump()

main()
