# sqllite db 관련은 기본적으로 파이썬에 내장되어 있다.

import os
import sqlite3

db_file_path = os.path.abspath('../data/sample.db')

conn = sqlite3.connect(db_file_path)
cur = conn.cursor()

# 전체 회원 조회
cur.execute('select * from member')
rows = cur.fetchall()

for r in rows:
    print(r)

print(" ====================== ")

# 특정 회원 조회
# cur.execute("select * from member where mid=?", (1, 'kim')) # python 2.x
cur.execute("select * from member where mid=:mid", {'mid': 'kim'})  # python 3.x
rows = cur.fetchall()

for r in rows:
    print(r)

print(" ====================== ")

# 회원 입력

# sql = "insert into member (mid, mpw, mname) values ('park', '0000', '박씨')"
# sql = "insert into member (mid, mpw, mname) " \
#       "values (?, ?, ?)"
# cur.execute(sql, ('han', '444', '한씨'))
# conn.commit()

# 회원 삭제
# sql = "delete from member where mid=:mid"
# cur.execute(sql, {'mid':'park'})
# conn.commit()

# 회원 수정

# sql = "update member set mpw=:mpw, mname=:mname " \
#       "where mseq=:mseq"
# sql = "update member set mpw=?, mname=? " \
#       "where mseq=?"
# cur.execute(sql, ('1', '1234', '허씨'))
# conn.commit()


# 일괄 입력
#
# sql = "insert into member (mid, mpw, mname) " \
#       "values (?, ?, ?)"
#
# data = (('han1', '444', '한씨1'), ('han2', '444', '한씨2'), ('han3', '444', '한씨3'))
#
# cur.executemany(sql, data)
# conn.commit()

conn.close()
