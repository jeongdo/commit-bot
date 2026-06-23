class Account():
    counter = 0

    def __init__(self, name, ini_bal):
        self.owner = name
        self.balance = ini_bal
        Account.counter += 1

    # 소멸함수자, del() 호출시 실행됨
    def __del__(self):
        Account.counter -= 1

    def deposit(self, amount):
        self.balance = self.balance + amount

    def print_bal(self):
        print(self.balance)

    def print_acc(self):
        print('''Account owner : %s
        Account balance : %s''' % (self.owner, self.balance))

    @staticmethod
    def account_instances():
        return Account.counter


acc1 = Account('Tom', 2000)
acc1.deposit(200)
acc1.print_acc()
acc2 = Account('Heo', 12000)
acc2.print_acc()

print("============ 전역변수 및 static 메소드 확인 ================")

print(Account.counter)
print(Account.account_instances())
print(acc1.account_instances())
print(acc2.account_instances())

print("============ 소멸함수 호출 후 전역변수 및 static 메소드 확인  ================")

del (acc2)

print(Account.counter)
print(Account.account_instances())
