"""
008: str (문자열)
불변(Immutable) 객체이며, 다양한 내장 메서드를 제공합니다.
"""

print("=== 1. 문자열 연산 ===")
print("Python" + " is fun!")
print("-" * 20)

print("\n=== 2. 인덱싱(Indexing) ===")
word = "Backend"
print(f"첫 글자: {word[0]}, 마지막 글자: {word[-1]}")

print("\n=== 3. 실무 필수 문자열 메서드 ===")
text = "  Hello, World!  "
print(f"공백 제거: [{text.strip()}]")
print(f"소문자 변환: [{text.lower()}]")

# 원본은 바뀌지 않고 새로운 문자열 반환
print(f"치환: [{text.replace('World', 'Python').strip()}]")

# 분리와 결합
csv_data = "apple,banana"
fruits = csv_data.split(",")
print(f"split: {fruits}")
print(f"join: {' / '.join(fruits)}")