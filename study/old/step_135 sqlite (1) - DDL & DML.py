# 데이터베이스 접속 방법

# table     : member
# column    : mseq (Primary key), mid, mpw, mname

# DDL (Data Definition Language)
# RDB의 종류에 따라 DDL 구문은 다르다.
# create table member (
#       mseq integer primary key,
#       mid text(20)
#       mpw text(20)
#       mname text(20)
# );

# DML (Data Manipulation Language)
# insert ( = Create)

# sqllite의 경우, 테이블 옆에 해당 칼럼이 없는 경우는 auto increment 값도 입력을 받는다.
# insert into member values (1,'lee', '111', '이씨');
# insert into member values (2,'kim', '222', '김씨');

# insert into member (mid, mpw, mname) values ('lee', '111', '이씨')

# select ( = Read)
# select id, pw from member;
# select * from member;
# select * from member where id ='lee';
# select * from member where id ='lee' and pw ='111';

# update ( = Update)
# update member set pw ='222'
# update member set pw ='222' where id = 'kim'

# delete ( = Delete)
# delete from member pw ='222'
# delete from member pw ='222' where id = 'kim'
