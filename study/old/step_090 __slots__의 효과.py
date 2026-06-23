# 객체 하나당 하나씩 존재하는 __dict__의 존재는 부담이 된다.

import timeit


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '({0}, {1}, {2})'.format(self.x, self.y, self.z)


class Point3D_Slots:

    __slots__ = ('x', 'y', 'z')  # 속성을(변수를) x, y, z로 제한한다!, 딕셔너리가 생성되지 않는다.

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '({0}, {1}, {2})'.format(self.x, self.y, self.z)


def main():
    start = timeit.default_timer()

    p1 = Point3D(1, 1, 1)
    # print(p1.x, p1.y, p1.z)
    # print(p1.__dict__['x'], p1.__dict__['y'], p1.__dict__['z'])
    for i in range(3000):
        for j in range(3000):
            p1.x += 1
            p1.z += 1
            p1.y += 1

    print(p1)

    stop = timeit.default_timer()
    print('Point3D 실행시간 : ', stop - start)

    print("===========")

    start = timeit.default_timer()

    p2 = Point3D_Slots(1, 1, 1)

    for i in range(3000):
        for j in range(3000):
            p2.x += 1
            p2.z += 1
            p2.y += 1

    stop = timeit.default_timer()

    print('Point3D_Slots 실행시간 : ', stop - start)

    print(p2)


# (9000001, 9000001, 9000001)
# Point3D 실행시간 :  4.7551213
# ===========
# Point3D_Slots 실행시간 :  4.0119565
# (9000001, 9000001, 9000001)


main()
