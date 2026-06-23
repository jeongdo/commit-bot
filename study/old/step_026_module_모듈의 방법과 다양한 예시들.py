# 모듈 --> go module

# 1. 같은 폴더에 존재하는 파이썬 파일 import
#
# /home/a.py 에서 /home/b.py 를 import 하는 경우
#
# == == == == == == == a.py == == == == == == ==
# import b

# 2. 다른 폴더에 존재하는 파이썬 파일 import
#
# /home/a.py 에서 /data/python/b.py 를 import 하는 경우
#
# ============== a.py ==============
# import sys
# sys.path.insert(0, "/data/python/b.py")
# import b
#
# import 하고자 하는 파일의 directory를 system path에 넣어주어야 하기 때문에
# 먼저 sys 모듈을 import 하여 path에 원하는 directory를 추가해준뒤
# 원하는 파일을 import 한다.

# 3. 하위 폴더에 존재하는 파이썬 파일 import
#
# /home/a.py 에서 /home/lib/b.py 를 import 하는 경우
#
# /home/lib/__init__.py 를 만들어준다. (내용은 없어도 상관없음)
#
# ============== a.py ==============
# import lib.b
#
# import 하고자 하는 파일이 위치한 directory를 import 구문에서 직접접근 하고 싶다면
# 해당 directory에 __init__.py 파일을 작성해주어야 한다.
# 그러면 폴더를 .(점) 단위로 구분하여 파일을 부를 수 있다.

# 4. Class 또는 Function 만 import하기
#
# 여기서는 파일내부의 특정 코드만을 import 하는 방법 2가지를 한꺼번에 설명한다.
#
# /home/a.py 에서 /home/b.py 의 Human Class를 import 하는 경우
#
# /home/a.py 에서 /home/c.py 의 getName Function을 import 하는 경우
#
# /home/a.py 에서 /home/lib/d.py 의 getHometown Function을 import 하는 경우
#
# ============== b.py ==============
#
# class Human:
# 	def __init__(self, name):
# 		self.name = name
#
# 	def getName(self):
# 		return self.name
#
# ============== c.py ==============
#
# def getName():
# 	return "양파개발자"
#
# ============== d.py ==============
#
# def getHometown():
# 	return "전주"
#
#
# ※ /home/lib/__init__.py 생성 후
# ============== a.py ==============
#
# from b import Human
# from c import getName
# from lib.d import getHometown
#
# human = Human("Jack")
# print human.getName()
# print getName()
# print getHometown()

#  import module.circle as circle # 하단 함수 이름도 import 명 module.circle 통으로 길게 해줘야 해서 as로 별칭 처리
import module  # module 디렉토리 하위 모두 임포트


def main():
    r = float(input("반지름 입력: "))
    ar = module.circle.ar_circle(r)
    print("넓이 : ", ar)
    ci = module.test.ci_circle(r)
    print("둘레 : ", ci)


main()

import module.circle as circle  # module 디렉토리의 circle.py import 하고 길어서, circle로 이름을 짧게 준다.


def main():
    r = float(input("반지름 입력: "))
    ar = circle.ar_circle(r)
    print("넓이 : ", ar)
    ci = circle.ci_circle(r)
    print("둘레 : ", ci)


main()

import module.test as t_circle  # module 디렉토리의 test.py import 하고 길어서, t_circle로 이름을 짧게 준다.


def main():
    r = float(input("반지름 입력: "))
    ar = t_circle.ar_circle(r)
    print("넓이 : ", ar)
    ci = t_circle.ci_circle(r)
    print("둘레 : ", ci)


main()

import module.test as ci_circle  # module 디렉토리의 test.py 중 ci_circle 함수만 import 하겠다.
import module.circle as ar_circle  # module 디렉토리의 circle.py 중 ar_circle 함수만 import 하겠다.


def main():
    r = float(input("반지름 입력: "))
    ar = ar_circle(r)
    print("넓이 : ", ar)
    ci = ci_circle(r)
    print("둘레 : ", ci)


main()

import module.sub.triangle as triangle  # module 디렉토리의 하위 디렉토리 sub의 triangle.py 를 이름이 길어서 triangle 로 import 하겠다.


def main():
    r = float(input("반지름 입력: "))
    ar = triangle.ar_circle(r)
    print("넓이 : ", ar)
    ci = triangle.ci_circle(r)
    print("둘레 : ", ci)


main()

# 전부가 아니라 module의 특정 함수만 가져오서 이름 줄이기
from module.circle import ar_circle as cc
from module.sub.triangle import ci_circle as cii


def main():
    r = float(input("반지름 입력: "))
    ar = cc(r)
    print("넓이 : ", ar)
    ci = cii(r)
    print("둘레 : ", ci)


main()
