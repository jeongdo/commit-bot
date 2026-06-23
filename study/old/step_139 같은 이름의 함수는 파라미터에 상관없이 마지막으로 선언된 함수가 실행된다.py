#함수 모듈

def localPrintModule(x, *list):
    print(list)
    print(*list) # 리스트 결과만 딱 표출할려면
    return x


def localPrintDicModule(**dic):
    print("dic 출력 : ", dic)


def addNum(x, y):
    return x + y

def addDivNum(x, y):
    return x + 2, y + 3

# 같은 이름의 마지막 함수가 덮어 버린다. 파라미터에 상관없이 이름이 기준이다.
def addNum(x,y,z=None):
    return x - y + 1000000000