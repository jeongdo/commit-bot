# 파이썬 스크립트 파일을 실행하면 자동으로 생성되는 변수로 __name__ 이라는 것이 있다.
import module.main.who_are_you

print('play importer')
print('__name__: {0}'.format(__name__))

# file name: who are you.py
# __name__: module.main.who_are_you     # 패키지와 파일 이름이 출력 되었다.
# play importer
# __name__: __main__  : 메인함수를 실행 시키는 주체가 되는 스크립트 파일이 __name__이 담기는 문자열은 __main__ 이다. 즉, 실행 주체에게 __main__ 이 담긴다.


# 그리고, import 되는 스크립트 파일의 __name__ 에는 파일의 이름을 문자열로 채운다.
