"""
014: while (조건부 반복문)
특정 조건이 True인 동안 무한히 반복합니다.
"""

print("=== 1. 기본 while 및 제어문(break, continue) ===")
count = 0
while count < 5:
    count += 1
    if count == 3:
        print("3은 건너뜁니다! (continue)")
        continue  # 아래 코드를 무시하고 다시 while의 처음(조건식)으로 올라감
    if count == 5:
        print("5에서 반복문을 강제 종료합니다! (break)")
        break     # 반복문을 완전히 탈출함
    print(f"현재 카운트: {count}")

print("\n=== 2. [실무 패턴] 무한 루프 (Event Loop) ===")
# 사용자 입력을 계속 받거나, 서버가 요청을 대기할 때 주로 사용합니다.
# (실행 중단을 방지하기 위해 주석 처리해 두었습니다.)
"""
while True:
    command = input("명령을 입력하세요 ('quit' 입력 시 종료): ")
    if command == "quit":
        break
    print(f"입력하신 명령: {command}")
"""