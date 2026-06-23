"""
005: bool (불리언), Truthy/Falsy, 그리고 단축 평가
"""

print("=== 1. 논리 연산자 ===")
print(f"True and False: {True and False}")
print(f"not True: {not True}")

print("\n=== 2. Truthy와 Falsy ===")
# 0, 빈 문자열(''), 빈 리스트([]), None 등은 거짓(False)으로 평가됩니다.
# 그 외의 값이 있는 모든 데이터는 참(True)으로 평가됩니다.
user_input = ""
if not user_input:
    print("입력값이 비어 있습니다! (Falsy 활용)")

print("\n=== 3. [심화] 단축 평가 (Short-Circuit) ===")
# or는 첫 번째로 '참'인 값을, and는 첫 번째로 '거짓'인 값을 반환합니다.

# 실무 활용 패턴: 기본값 세팅하기
# user_name이 비어있으면 뒤의 "익명"이 할당됨
user_name = "" or "익명"
print(f"환영합니다, {user_name}님!")

# 평가 중단 확인 (''이 거짓이므로 뒤의 'Python'은 보지 않고 '' 반환)
print(f"and 단축평가 결과: {'Hello' and '' and 'Python'}")