
# file : 파일 경로
# mode : 파일이 열리는 모드
# 'r' : 읽기 용으로 열림 (기본값)
# 'w' : 쓰기 위해 열기, 파일을 먼저 자른다.
# 'x' : 베타적 생성을 위해 열리고, 이미 존재하는 경우 실패
# 'a' : 쓰기를 위해 열려 있고, 파일의 끝에 추가하는 경우 추가합니다.
# 'b' : 2진 모드(바이너리 모드)
# 't' : 텍스트 모드 (기본값)
# '+' : 업데이트 (읽기 및 쓰기)를 위한 디스크 파일 열기
# 'U' : 유니버설 개행 모드 (사용되지 않음)
# buffering : 버퍼링끄기는 0(바이너리모드에서만 동작함), 라인모드는 1 (텍스트 모드에서만 가능), 고정 크기로 보내려면 임의의 바이트수를 1보다 큰 양의 수로 입력, 기본 정책은 아래와 같습니다.

# open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)

# 이진 파일은 고정 크기 청크로 버퍼링됩니다. 버퍼의 크기는 기본 장치의 "블록 크기"를 결정하고 다시 떨어지는 경험적 방법을 사용하여 선택됩니다 io.DEFAULT_BUFFER_SIZE. 많은 시스템에서 버퍼는 일반적으로 4096 또는 8192 바이트 길이입니다.
# "대화식"텍스트 파일 ( isatty() 반환 되는 파일 True)은 회선 버퍼링을 사용합니다. 다른 텍스트 파일은 바이너리 파일에 대해 위에서 설명한 정책을 사용합니다.
# encoding : 파일을 디코딩하거나 인코딩하는데 사용되는 이름, 대부분 utf-8 이지만 모든 시스템이 utf-8이라는 보장이 없으므로 명시적으로 하는 것이 좋다.
# 파이썬에서 지원되는 인코딩 목록 - https://docs.python.org/3.6/library/codecs.html

# Access mode	   Description
#   'r'	            Read only
#   'r+'	        Read and write. 파일이 없으면 에러 발생
#   'w'	            Write only. 파일이 없으면 파일 생성
#   'w+'	        Write and Read
#   'a'	            Append only
#   'a+'	        Append and read

# mode='wt'라고 되어 있는 부분은 쓰기모드이면서 텍스트모드를 가리킵니다.
# mode를 작성할 때 r(읽기), w(쓰기), a(추가하기) 세가지중 하나와 t(텍스트)와 b(바이너리) 둘중 하나와 반드시 결합해야


import os

print("=============== append & write =======================")

file_aba_path = os.path.abspath('../data/sample_03.txt')

with open(file_aba_path, "a") as file:
    file.write("Hello~ \n")
    file.write("World!")
    file.close()

print("=============== append & writelines =======================")

file_aba_path = os.path.abspath('../data/sample_03.txt')

with open(file_aba_path,  mode='at', encoding='utf-8') as file:
    file.writelines(['writelines로 추가합니다.', '내부 원소는 개행이 안되는군요.', '개행을 하려면 개행문자를 입력해야합니다.\n', '마지막에는 안붙여도 개행문자가..'])
    file.close()

