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

    prop = property(getn, setn)  # 프로퍼티 설정, property 객체를 생성하면서 getn과 setn 메서드를 등록하는 것이다.


def main():
    n1 = Natural(1)
    n2 = Natural(2)
    n3 = Natural(3)
    # n1.setn(n2.getn() + n3.getn())
    n1.prop = n2.prop + n3.prop
    # = 기준으로, 왼쪽에 있는 객체는 setn 호출, 오른쪽에 있는 객체는 getn 호출,
    # 직접전근과 동일하게 그 객체의 메소드를 호출하기 때문에, 직접접근을 해도 안전해 진다.

    print(n1.getn())


main()
