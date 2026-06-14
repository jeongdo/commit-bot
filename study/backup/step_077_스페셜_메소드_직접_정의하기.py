class Car:
    def __init__(self, id):
        self.id = id  # 차량 번호

    def __len__(self):
        return len(self.id)  # 차량번호의 길이 반환

    def __str__(self):
        return 'Vehicle number : ' + self.id


def main():
    c = Car("32러5234")
    print(len(c))  # Car 객체의 사용자가 정의한 __len__ 메소드가 호출됨
    print(str(c))  # Car 객체의 사용자가 정의한 __str__ 메소드가 호출됨


main()
