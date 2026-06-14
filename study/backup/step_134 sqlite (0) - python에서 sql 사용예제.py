import os
import sqlite3

# step-0. 파이썬에 기본적으로 내장된 sqlite 데이타베이스를 사용하는 방법을 알아보고자 한다.

# step-1. 준비 : Database 파일의 경로 설정 (현재 실행중인 폴더 아래에 DB폴더).

BASE_DIR = os.path.abspath('..')
TARGET_DIR = os.path.join(BASE_DIR, "database")
TARGET_FILE = 'test.db'
TARGET_FILE_FULL_PATH = os.path.join(TARGET_DIR, TARGET_FILE)


# step-2. DB 폴더 생성 : 폴더가 없으면 새로 만듬.
def makeDir():
    if not os.path.isdir(TARGET_DIR):
        os.makedirs(TARGET_DIR)


# step-4. Database 테이블 생성
def createTable():
    con = sqlite3.connect(TARGET_FILE_FULL_PATH)
    cur = con.cursor()

    # 테이블이 이미 있다면 생성시 에러나므로 삭제해주는 옵션 코드
    # cur.execute('Drop Table If Exists new_table')
    # cur.execute( 'Drop Table If Exists PhoneBook')
    # con.commit()

    cur.execute('''Create Table if not exists  PhoneBook (         
        Name VARCHAR(12),
        PhoneNum VARCHAR(20),
        Address VARCHAR(80)
        )
    ''')
    con.commit()
    cur.close()
    con.close()


if __name__ == '__main__':
    makeDir()

    # step-4. Database 테이블 생성
    createTable()

    # step-3. Database 연결객체 및 커서 만들기
    # con = sqlite3.connect(':memory:') # 메모리 db 옵션
    con = sqlite3.connect(TARGET_FILE_FULL_PATH)
    cur = con.cursor()

    # step-5. 데이터 입력.
    # 기본( 필드명 없이 데이타 순서대로 ,Primary Key는 넣으면 안됨.)

    sql = "INSERT INTO PhoneBook VALUES( 'Kim ManJae', '010-1234-5678', '서울 용산');"
    cur.execute(sql)

    # 필드명 지정(순서는 상관없이 필드명과 값이 매치되면됨.)
    sql = "Insert Into PhoneBook (Name, PhoneNum, Address ) \
      VALUES('Kim ManJae', '010-1234-5678', '서울 용산');"
    cur.execute(sql)

    # 변수를 이용 : 튜플
    sql = "INSERT INTO PhoneBook VALUES(?, ?, ?);"
    name, phone, addr = 'Kang Minkyung', '010-8521-7896', '강원도 인제'
    cur.execute(sql, (name, phone, addr))

    # 변수를 이용 :  딕셔너리, 변수의 데이타순서는 앞의 값과 매칭만되면됨
    name, phone, addr = 'Kweon Mijin', '011-7852-2587', '서울 마포'
    sql = "INSERT INTO PhoneBook VALUES(:iName, :iPhone, :iAddr);"
    cur.execute(sql, {'iPhone': phone, 'iName': name, 'iAddr': addr})

    # 데이타 리스트 이용.
    datalist = (('Tom', '010-1543-5820', '제주 제주시'), \
                ('John', '010-5152-5462', '충남 부여'))

    sql = "INSERT INTO PhoneBook VALUES(?, ?, ?);"
    cur.executemany(sql, datalist)

    # step-6. 데이터 조회 : 조건에 맟는 모든 데이타 가져오기.
    cur.execute("SELECT * FROM PhoneBook;")

    for row in cur:
        print(row)

    # 조건에 맞는 데이타 3개만 가져오기
    # cur.execute("SELECT * FROM PhoneBook limit 3 ;")

    # 조건에 맞는 데이타중 3번째부터 2개 가져오기.
    # cur.execute("SELECT * FROM PhoneBook limit 3,2 ;")

    cur.execute("SELECT * FROM PhoneBook;")

    # 쿼리 결과를 첫번째 것 자동으로 다음레코드로 포인터 이동,
    cur.fetchone()
    # 쿼리 결과를 2개 가져오기. 포인터는 자동으로 4번째로.
    cur.fetchmany(2)

    # 모든 쿼리 결과를 가져오기( fetchall )
    cur.fetchall()

    # step-7. 데이터베이스 닫기.
    # Database 사용이 끝났으면 반드시 닫아야 한다.
    con.commit()
    cur.close()
    con.close()
