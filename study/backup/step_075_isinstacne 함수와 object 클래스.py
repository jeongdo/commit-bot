class Simple:
    pass


s = Simple()

print(isinstance(s, Simple))  # 해당 클래스의 객체인지 true/false로 반환

print(isinstance([1, 2], list))


class Fruit:
    pass

class Apple(Fruit):
    pass

class SuperApple(Apple):
    pass


sa = SuperApple()
print(isinstance(sa, SuperApple))  # Fruit을 간접 상속
print(isinstance(sa, Apple))
print(isinstance(sa, Fruit))

print("#############################")

# type 클래스도 object 클래스를 상속한다.

print("# 파이썬의 모든 클래스는 object 클래스를 직접 혹은 간접 상속한다. #")

print(isinstance(s, object))
print(isinstance([1, 2], object))

print("# issubclass(Z, A) #")   # Z는 A를 상속하는가?

print(issubclass(Apple, Fruit))
