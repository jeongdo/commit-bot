class SoSimple:
    def geti(self):
        return self.i


ss = SoSimple()

print("===== 객체 밖에서 변수와 메소드의 생성과 삭제가 가능하다. =====")

ss.i = 27  # 이 순간에 변수 ss 담긴 객체에 i라는 변수가 만들어진다.
print(ss.geti())

ss.hello = lambda: print('hi~')  # hello 라는 메소드를 추가
print(ss.hello())

del ss.i
del ss.hello  # ss에 담긴 객체에서 메소드 hello 삭제

# ss.geti()