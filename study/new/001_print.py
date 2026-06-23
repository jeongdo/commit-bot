"""
001: print() 함수의 다양한 활용법 완벽 가이드
"""

print("=== 1. 기본 출력 ===")
print("Hello, Python!")
print(12345)
print(True)

print("\n=== 2. 여러 값 동시에 출력하기 ===")
print("Python", "Java", "C++")

print("\n=== 3. sep 옵션 (구분자 변경) ===")
print("2026", "06", "23", sep="-")
print("apple", "banana", "cherry", sep=", ")

print("\n=== 4. end 옵션 (끝 문자 변경) ===")
print("첫 번째 줄입니다.", end=" ")
print("두 번째 줄이 바로 이어집니다.")

print("\n=== 5. 이스케이프 문자(Escape Characters) 활용 ===")
print("안녕\n하세요")     # \n : 줄바꿈
print("이름:\t홍길동")    # \t : 탭

print("\n=== 6. 문자열 포매팅 ===")
name = "Alice"
score = 95
# f-string (가장 현대적이고 권장되는 방식)
print(f"이름: {name}, 점수: {score}점")

print("\n=== 7. 파일로 출력하기 (file 옵션) ===")
with open("sample.txt", "w", encoding="utf-8") as f:
    print("이 내용은 화면에 보이지 않고 텍스트 파일에 저장됩니다.", file=f)