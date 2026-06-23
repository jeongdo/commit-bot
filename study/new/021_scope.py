"""
021 : Scope (유효 범위)와 Namespace (이름 공간)
변수 이름이 어디까지 살아있고, 파이썬이 변수를 어떻게 찾는지(LEGB 규칙) 알아봅니다.
"""

print("=== 1. Scope 기본과 LEGB 룰 ===")
# L: Local (함수 내부)
# E: Enclosing (중첩 함수에서의 외부 함수)
# G: Global (전역, 파일 전체)
# B: Built-in (파이썬 내장, print, len 등)
# 파이썬은 변수를 찾을 때 L -> E -> G -> B 순서로 밖으로 나가며 찾습니다.

msg = "전역(Global) 변수입니다."

def outer_function():
    msg = "지역(Local) 변수입니다." # 이름은 같지만 전혀 다른 메모리 공간
    print(f"함수 내부에서 출력: {msg}")

outer_function()
print(f"함수 외부에서 출력: {msg}") # 함수 내부의 변화가 밖으로 영향을 주지 않음

print("\n=== 2. [심화] global 키워드의 위험성 ===")
# 함수 내부에서 전역 변수를 수정하고 싶다면 global 키워드를 씁니다.
# 하지만 실무에서는 상태 추적이 어려워져 버그의 원흉이 되므로 거의 금기시되는 패턴입니다.
# (대신 함수의 return 값을 활용하는 것을 권장합니다.)

count = 0
def increment():
    global count
    count += 1 # 전역 변수 직접 수정

increment()
print(f"global 키워드로 수정된 카운트: {count}")

print("\n=== 3. Namespace (이름 공간) ===")
# 변수와 객체의 관계(이름표)를 저장하는 거대한 딕셔너리입니다.
# globals() 와 locals() 함수를 통해 파이썬이 뒤에서 딕셔너리로 관리하고 있다는 것을 볼 수 있습니다.
my_secret_var = 777
print(f"globals() 딕셔너리에 변수가 있나요? {'my_secret_var' in globals()}")