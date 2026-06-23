
# class 메소드 인자로 클래스 정보를 받는다. 그리고 이 정보는 호출 경로에 따라 유동적이다. 이것이 class와 static 메소드의 차이이다.


class Date:     # 날짜를 표현한 클래스
    def __init__(self, y, m, d):
        self.y = y      # 년
        self.m = m      # 월
        self.d = d      # 일

    def show(self):
        print('{0}, {1}, {2}'.format(self.y, self.m, self.d))

    @classmethod
    def next_day(cls, today):
        return cls(today.y, today.m, today.d + 1)  # today 다음 날에 대한 객체 생성 및 반환


class KDate(Date):      # Date 클래스 상속, 한국의 시각 출력
    def show(self):
        print('KOR : {0}, {1}, {2}'.format(self.y, self.m, self.d))


class JDate(Date):      # Date 클래스 상속, 일본의 시각 출력
    def show(self):
        print('JPN : {0}, {1}, {2}'.format(self.y, self.m, self.d))


def main():

    kd1 = KDate(2025, 4, 12)    # 한국의 시각 정보
    kd1.show()
    kd2 = KDate.next_day(kd1)   # KDate 객체가 전달되어져서 반환된다. 이건 static 메소드로는 할 수 없는 일이다.
    kd2.show()

    print("============================")

    jd1 = JDate(2027, 5, 19)  # 일본의 시각 정보
    jd1.show()
    jd2 = JDate.next_day(jd1)   # JDate 객체가 전달되어져서 반환된다.
    jd2.show()


main()
