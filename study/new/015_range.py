"""
015: range (연속된 숫자 생성기)
[심화] range는 리스트(List)가 아닙니다! 메모리를 극적으로 아껴주는 똑똑한 '객체'입니다.
"""
import sys

print("=== 1. range 기본 ===")
# range(시작, 끝(미포함), 스텝)
print(list(range(5)))         # [0, 1, 2, 3, 4]
print(list(range(2, 10, 2)))  # [2, 4, 6, 8]
print(list(range(10, 0, -1))) # [10, 9, 8, ..., 1] 역순

print("\n=== 2. [심화] range의 메모리 마법 (Lazy Evaluation) ===")
# range는 숫자를 미리 다 만들어두지 않고, '어디서 시작해서 어떻게 끝날지' 공식만 저장합니다.
# 그리고 값이 필요할 때마다 그때그때 하나씩 생성해서 던져줍니다.

# 10개짜리 리스트 vs range
list_10 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
range_10 = range(10)
print(f"리스트(10) 메모리 크기: {sys.getsizeof(list_10)} bytes")
print(f"range(10) 메모리 크기: {sys.getsizeof(range_10)} bytes")

# 1,000만 개짜리 리스트 vs range
# 리스트는 1000만 개의 숫자를 메모리에 전부 올리지만,
# range는 시작(0), 끝(1000만), 규칙(+1) 정보만 가지므로 메모리 크기가 똑같습니다!
range_10m = range(10_000_000)
print(f"range(1,000만) 메모리 크기: {sys.getsizeof(range_10m)} bytes") # 위와 동일함!