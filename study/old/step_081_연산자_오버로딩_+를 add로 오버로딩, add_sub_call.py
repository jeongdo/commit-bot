class Account:
    def __init__(self, aid, abl):
        self.aid = aid      # 계좌 번호
        self.abl = abl      # 계좌 잔액

    def __add__(self, m):   # 입금
        self.abl += m
        print('__add__')

    def __sub__(self, m):   # 출금
        self.abl -= m
        print('__sub__')

    def __call__(self):     # 계좌 상황을 문자열로 반환,  () 의 오버로딩이다.
        print('__call__')
        return str(self.aid) + " : " + str(self.abl)


def main():
    acnt = Account('James01', 100)  # 계좌 개설
    acnt + 100                      # 100원 입금, __add__ 호출로 이어짐          acnt.__add__(100)
    acnt - 50                       # 50원 출금, __sub__ 호출로 이어짐           acnt.__sub__(50)
    print(acnt())                   # 계좌 정보 확인, __call__ 호출로 이어짐      acnt.__call__()

    # __call__ : acnt() 처럼 acnt 객체이름을 대상으로 () 함수 호출형식으로 호출하면 __call__ 메소드가 호출되는 것이다.


main()