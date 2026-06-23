"""
013: for (반복문)
파이썬의 for문은 타 언어(C, Java)의 for(i=0; i<n; i++) 방식이 아닌,
컬렉션(리스트, 문자열 등)의 요소를 하나씩 순회하는 'for-each' 방식입니다.
"""

print("=== 1. 기본 순회 ===")
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

print("\n=== 2. 딕셔너리(dict) 순회 ===")
user = {"name": "Alice", "age": 30}
# 딕셔너리를 그냥 순회하면 '키(Key)'만 나옵니다.
for key in user:
    print(f"키: {key}, 값: {user[key]}")

# 실무 권장: .items()를 사용해 키와 값을 동시에 언패킹(Unpacking)합니다.
for key, value in user.items():
    print(f"{key} -> {value}")

print("\n=== 3. [심화] for ... else 문법 ===")
# 파이썬에만 있는 아주 독특하고 강력한 문법입니다.
# for문이 'break'로 중간에 끊기지 않고 '무사히 끝까지' 돌았을 때만 else 블록이 실행됩니다.
# (알고리즘 문제에서 소수 찾기, 검색 등에 플래그 변수 없이 깔끔하게 쓰입니다)

search_target = "grape"
for fruit in fruits:
    if fruit == search_target:
        print("포도를 찾았습니다!")
        break
else:
    # break를 만나지 않고 for문이 정상 종료됨 = 포도가 없었음
    print("과일 바구니에 포도가 없습니다.")