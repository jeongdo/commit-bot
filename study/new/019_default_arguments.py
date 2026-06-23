"""
019: default arguments (기본 인수)와 실무에서 가장 많이 하는 끔찍한 실수
"""

print("=== 1. 기본 인수의 올바른 사용 ===")
def make_coffee(size="Regular"):
    print(f"{size} 사이즈 커피 제조 중...")

make_coffee()        # 기본값 Regular 사용
make_coffee("Large") # Large로 덮어쓰기

print("\n=== 2. [초심화/매우중요] 가변(Mutable) 객체를 기본 인수로 쓸 때의 함정 ===")
# 리스트[]나 딕셔너리{}를 기본 인수로 주면 절대, 절대 안 됩니다.
# 파이썬에서 함수의 기본값은 '함수가 호출될 때'가 아니라 '함수가 정의될 때' 딱 한 번만 만들어집니다!

def bad_append(item, my_list=[]):
    my_list.append(item)
    return my_list

# 매번 빈 리스트에서 시작할 것 같지만...
print(bad_append(1)) # [1]
print(bad_append(2)) # [1, 2] -> ?? 왜 1이 살아있지?
print(bad_append(3)) # [1, 2, 3] -> 좀비 리스트가 되었습니다. (함수 정의 시 만들어진 리스트 객체를 계속 공유함)

print("\n=== 3. 안전한 기본 인수 패턴 (None 활용) ===")
# 따라서 실무에서는 항상 기본값을 None으로 주고, 함수 내부에서 리스트를 새로 생성합니다.
def good_append(item, my_list=None):
    if my_list is None:
        my_list = []  # 함수가 호출될 때마다 새로운 빈 리스트 객체 생성
    my_list.append(item)
    return my_list

print(good_append(1)) # [1]
print(good_append(2)) # [2] (정상 작동!)