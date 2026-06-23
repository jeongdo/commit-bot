"""
016: nested loop (중첩 루프)
반복문 안에 반복문이 있는 구조입니다. (2차원 데이터 처리 등)
"""

print("=== 1. 중첩 루프 동작 원리 ===")
# 바깥쪽 루프(i)가 1번 돌 때, 안쪽 루프(j)는 끝까지 돕니다.
for i in range(2):         # 0, 1
    for j in range(3):     # 0, 1, 2
        print(f"i={i}, j={j}")

print("\n=== 2. [심화] 다중 반복문 탈출 (Flag 변수 활용) ===")
# 안쪽 루프에서 break를 걸면 안쪽 루프만 깨집니다.
# 바깥쪽 루프까지 한 번에 깨고 싶다면 상태를 저장하는 변수(Flag)가 필요합니다.

found = False
for x in range(5):
    for y in range(5):
        if x == 2 and y == 2:
            print(f"목표물 발견! x={x}, y={y}")
            found = True
            break # 안쪽 루프 탈출
    if found:
        break     # 바깥쪽 루프까지 탈출

# (참고) 이런 경우 차라리 012번에서 배운 함수+return(Guard Clause)으로 빼버리는 것이 훨씬 깔끔합니다.