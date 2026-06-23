"""
012: if (조건문)
프로그램의 흐름을 제어합니다.
[심화] 조건부 표현식(3항 연산자)과, 들여쓰기를 줄여주는 'Guard Clause' 패턴을 눈여겨보세요.
"""

print("=== 1. 기본 if-elif-else ===")
score = 85
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C")

print("\n=== 2. [심화] 조건부 표현식 (Ternary Operator) ===")
# 타 언어의 '조건 ? 참 : 거짓' 에 해당하는 문법입니다.
# 변수 = [참일 때 값] if [조건] else [거짓일 때 값]
age = 20
status = "성인" if age >= 18 else "미성년자"
print(f"나이 {age}는 {status}입니다.")

print("\n=== 3. [실무 패턴] Guard Clause (보호 구문) ===")
# 조건문이 중첩되면 코드가 오른쪽으로 계속 들어가서(Depth가 깊어져서) 읽기 힘들어집니다.
# 조건에 맞지 않으면 '미리 튕겨내는' 방식을 실무에서 매우 권장합니다.

def process_data(data):
    # 나쁜 예: 조건문이 깊어짐
    # if data:
    #     if len(data) > 0:
    #         print("데이터 처리 중...")

    # 좋은 예 (Guard Clause): 예외 상황을 먼저 걸러내고 함수를 종료시킴
    if not data:
        return "데이터가 없습니다."

    # 여기까지 도달했다면 데이터가 확실히 있다는 뜻! (마음 편히 메인 로직 작성)
    print("데이터 처리 중...")

process_data("정상 데이터")