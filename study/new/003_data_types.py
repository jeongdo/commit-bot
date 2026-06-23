"""
003: data types (데이터 타입 총정리)
파이썬에서 다루는 데이터들의 큰 그림입니다.
"""

print("=== 1. 숫자형 (Numeric) ===")
print(f"정수: {42}, 실수: {3.14}, 복소수: {3 + 4j}")

print("\n=== 2. 시퀀스 (Sequence) ===")
print(f"문자열(str): {'Python'}")
print(f"리스트(list): {[1, 2, 3]} (수정 가능)")
print(f"튜플(tuple): {(1, 2, 3)} (수정 불가)")

print("\n=== 3. 매핑 (Mapping) ===")
dict_val = {"name": "Bob", "age": 25}
print(f"딕셔너리(dict): {dict_val}")

print("\n=== 4. 세트 (Set) ===")
set_val = {1, 2, 2, 3}
print(f"세트(set): {set_val} (중복 제거됨)")

print("\n=== 5. 불리언과 None ===")
print(f"불리언(bool): {True}, {False}")
print(f"NoneType: {None} (값이 없음을 의미)")