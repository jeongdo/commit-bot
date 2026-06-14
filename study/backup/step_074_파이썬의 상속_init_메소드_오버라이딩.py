class Car:
    def __init__(self, id, f):
        self.id = id        # 차량 번호
        self.fuel = f       # 남아 있는 연료의 사ㅣㅇ태

    def drive(self):        # 주행시는 연료 감소
        self.fuel -= 10

    def add_fuel(self, f):  # 연료 보충
        self.fuel += f

    def show_info(self):    # 현재 차의 상태 출력
        print("id: ", self.id)
        print("fuel: ", self.fuel)


class Truck(Car):
    def __init__(self, id, f, c):
        super().__init__(id, f)     # 부모 Car의 __init__ 메소드 호출
        self.cargo = c

    def add_cargo(self, c):  # 짐을 추가
        self.cargo += c

    def show_info(self):  # 현재 차의 상태 출력
        super().show_info()
        print("cargo: ", self.cargo)


def main():
    t = Truck("42럭4212", 0, 0)
    t.add_fuel(100)
    t.add_cargo(50)
    t.drive()
    t.show_info()


main()