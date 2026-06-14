# 빌트인 함수
# import 선언 없이 그냥 언제든 호출 가능한 함수

# 빌트인 모듈
# 위치 신경쓰지 않고 언제든 import 할 수 있는 모듈, 파이썬이 해준 모듈
import math

print(type(print))  # <class 'builtin_function_or_method'>
print(type(input))  # <class 'builtin_function_or_method'>

print(math.fabs(-10))  # 절대값 반환, 빌트인 모듈
