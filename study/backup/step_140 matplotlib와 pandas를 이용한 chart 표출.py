# step_140 matplotlib와 pandas를 이용한 chart 표출.py

import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

# list = [1,6,1,4,5]
# list = [[1,6,1,4,5]]
# list = [[1,6,1,4,5], [1,2,3,22,5]]
# plt.plot() # 빈차트 표출
# plt.plot([100,80,60,40,20], [1,2,3,22,5], "rs--")
# plt.show()

plt.rcParams["figure.figsize"] = (7, 3)
plt.rcParams["axes.grid"] = True

mon = [2, 4, 6, 8, 10]
dic = {"kim": [80, 70, 50, 40, 90],
       "lee": [70, 50, 80, 70, 80]}

frame = pd.DataFrame(dic, index=mon)
print(frame)

# db insert
conn = sqlite3.connect("../data/sample.db")
# frame.to_csv() # csv로 저장
# frame.to_excel # excel로 저장

# db_read
# frame.to_sql("score", conn, if_exists="replace")

result = pd.read_sql_query("select * from score", conn)

print()
print(result.to_dict(), end='\n')
print()

# print(result.to_string())
print(result)

frame.plot()
frame.plot(subplots=True)  # 차트 분리

plt.show()
