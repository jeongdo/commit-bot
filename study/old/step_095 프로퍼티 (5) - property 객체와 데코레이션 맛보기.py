# 데코레이터라는 것을 기반으로 프로퍼티를 지정하는 방법도 있다.


class Natural:
    def __init__(self, input_number):
        self.prop = input_number  # 프로퍼티 prop을 통해 접근

    @property  # 프로퍼티 객체를 만들어라.
    def prop(self):
        return self.__field_n

    @prop.setter
    def prop(self, input_number):
        if (input_number < 1):
            self.__field_n = 1
        else:
            self.__field_n = input_number


def main():
    n1 = Natural(1)
    n2 = Natural(2)
    n3 = Natural(3)

    n1.prop = n2.prop + n3.prop

    print(n1.prop)


main()
