"""
022: module basics (모듈 기초)
파이썬 스크립트 파일(.py) 하나하나는 모두 '모듈'입니다.
다른 파일의 코드를 재사용하기 위해 import를 사용합니다.
"""

print("=== 1. 모듈 전체 가져오기 ===")
import math
print(f"원주율: {math.pi}")
print(f"제곱근: {math.sqrt(16)}")

print("\n=== 2. 모듈에서 특정 부분만 가져오기 ===")
# 모듈 이름을 매번 쓰기 귀찮을 때 씁니다.
from datetime import datetime, timedelta
now = datetime.now()
print(f"현재 시간: {now}")

print("\n=== 3. 모듈 이름 별칭(Alias) 지어주기 ===")
# 이름이 너무 길거나, 다른 라이브러리와 이름이 충돌할 때 사용합니다.
# (이후 200번대에서 배울 numpy를 np로, pandas를 pd로 부르는 이유입니다.)
import random as rd
print(f"랜덤 숫자: {rd.randint(1, 10)}")

# [심화] import 동작 원리
# 모듈을 처음 import 할 때, 파이썬은 해당 파일의 모든 코드를 '한 번 실행'하여
# 생성된 함수와 변수들을 메모리(sys.modules)에 캐싱해둡니다.