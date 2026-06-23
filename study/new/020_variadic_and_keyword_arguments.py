"""
020 ~ 021: 가변 인수 (*args)와 키워드 가변 인수 (**kwargs)
개수를 알 수 없는 인수를 유연하게 처리하는 마법의 별표(*) 기호입니다.
"""

print("=== 1. *args (위치 가변 인수) ===")
# 별(*)을 하나 붙이면, 입력된 여러 개의 값들을 모아서 하나의 '튜플(tuple)'로 만들어줍니다. (Packing)
def sum_all(*numbers):
    print(f"받은 데이터(튜플): {numbers}")
    return sum(numbers)

print(f"합계: {sum_all(1, 2, 3, 4, 5)}")

print("\n=== 2. **kwargs (키워드 가변 인수) ===")
# 별(**)을 두 개 붙이면, 키워드=값 형태의 입력들을 모아서 하나의 '딕셔너리(dict)'로 만들어줍니다.
def print_config(**kwargs):
    print(f"받은 데이터(딕셔너리): {kwargs}")
    for key, value in kwargs.items():
        print(f"설정 {key}: {value}")

print_config(host="localhost", port=8080, debug=True)

print("\n=== 3. [심화] 반대로 풀어서 던지기 (Unpacking) ===")
# 별표 기호는 함수를 정의할 때는 '모아주지만(Packing)',
# 함수를 호출할 때는 리스트나 딕셔너리를 '풀어서(Unpacking)' 던져줍니다.

nums = [10, 20, 30]
# print(sum_all(nums)) # 오류! 리스트 1개가 튜플에 통째로 들어가버림
print(sum_all(*nums))  # 리스트를 풀어서 sum_all(10, 20, 30)으로 전달함!

conf = {"host": "127.0.0.1", "port": 443}
print_config(**conf)   # 딕셔너리를 풀어서 print_config(host="127.0.0.1", port=443)으로 전달함!