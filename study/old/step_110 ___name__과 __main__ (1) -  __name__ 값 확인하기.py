# 파이썬 스크립트 파일을 실행하면 자동으로 생성되는 변수로 __name__ 이라는 것이 있다.

def main():
    print('file name: who are you.py')
    print('__name__: {0}'.format(__name__))


main()

# file name: who are you.py
# __name__: __main__
