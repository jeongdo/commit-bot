# 객체가 갖는 값에 직접 접근하는 것은 오류의 확률을 높이므로, 메소드를 활용하는 것이 좋다.


class Natural:
    def __init__(self, input_number):
        # if (n < 1):
        #     self.__n = 1
        # else:
        #     self.__n = n
        self.setn(input_number)

    def getn(self):
        return self.__field_n

    def setn(self, input_number):
        if (input_number < 1):
            self.__field_n = 1
        else:
            self.__field_n = input_number


def main():
    n1 = Natural(1)
    n2 = Natural(2)
    n3 = Natural(3)
    n1.setn(n2.getn() + n3.getn())      # 조금 복잡해 보인다.

    print(n1.getn())


main()
