# from src.sqllite_member import CLASS # 클래스 가져올 때

# import src.sqllite_member  # 단순 함수만 가져올 때 (1)
import sqllite.member_sql as mem  # 단순 함수만 가져올 때 (2)

# 전형적인 호출 문법!!
# src.sqllite_member.member_select_all()

# alias를 이용한 간단 호출법!! 두가지 모두 숙지하자!!!
rows = mem.member_select_all()
# print(rows)
r1 = mem.member_select('kim', '222')
# print(r1)
r2 = mem.member_select('heo', '1234')
# print(r2)

for r in rows:
    # print(r)
    print(r[1])

for r in r2:
    print(r)

# mem.member_insert('jin', '666', '진씨')

# r3 = mem.member_select('jin')
# print(r3)
# mem.member_delete('jin')

# mem.member_update(1, '1234', '허씨')

# print(mem.member_select('heo'))
