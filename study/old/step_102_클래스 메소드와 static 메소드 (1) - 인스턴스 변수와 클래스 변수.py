print("===== 인스턴스 변수 =====")


class Simple01:
    def __init__(self):
        self.iv = 10  # iv는 인스턴스 변수, 객체별로 존재하는 변수


s = Simple01()

print(s.iv)  # 인스턴스 변수는 객체를 통해서 접근을 한다.

print("===== 클래스 변수와 인스턴스 변수 =====")


class Simple02:
    cv = 20  # cv는 클래스 변수, 클래스 Simple02에 속하는 변수

    def __init__(self):
        self.iv = 10  # iv는 인스턴스 변수, 객체별로 존재하는 변수


print(Simple02.cv)  # 인스턴스 변수는 객체를 통해서 접근을 한다.

s = Simple02()

print(s.cv)  # 클래스 변수는 개체를 통해서도 접근이 가능. 이건 객체가 많아져도, 클래스 당 하나만 만들어 진다.
print(s.iv)  # 인스턴스 변수는 객체를 통해서 접근을 한다.
