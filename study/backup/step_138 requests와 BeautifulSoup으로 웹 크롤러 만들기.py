# pom.xml
# <!-- https://mvnrepository.com/artifact/org.jsoup/jsoup -->
# <dependency>
#     <groupId>org.jsoup</groupId>
#     <artifactId>jsoup</artifactId>
#     <version>1.11.3</version>
# </dependency>

# pycharm 설치 : settion - current 프로젝트 - project interpreter - (+) 클릭 후 패키지 검색
# console 설치 : pip install beautifulsoup4
# pip install requests

# urllib는 폴더명 아래의 request.py명
import urllib.request

# bs4.py로 파일명이다. 이 파일에서 클래스 호출.
# 파라미터는 초기값 None은 안줘도 그만인 경우
# *list : 리스트 파라미터 의미, **dic : 딕셔너리 파라미터 의미
from bs4 import BeautifulSoup

host = "http://www.ytn.co.kr"

# 단순하게 통신만 한다.
data = urllib.request.urlopen(host + "/video/video_list_goodNews.html")

# 생성자를 실행한것이고, htmlStr은 객체
htmlStr = BeautifulSoup(data, "html.parser")

# print(htmlStr) # 너무 많아서 전부 표출되지 않는다.
# divStr = htmlStr.select("div#video_list_v2014")
# print(divStr)
# for dlStr in divStr:
#     dlStr.select("dl.news_list2014")
#     print(dlStr)

# divStr = htmlStr.select("div#video_list_v2014 > dl.news_list2014")
# print(divStr)

# divStr = htmlStr.select("div#video_list_v2014 > dl.news_list2014 > dt")
# print(divStr)

# divStr = htmlStr.select("div#video_list_v2014 > dl.news_list2014 > dt > a")
# print(divStr)

craw_list = []

divStr = htmlStr.select("div#video_list_v2014 > dl.news_list2014")
for x in divStr:
    xStr = x.select("dt > a")
    for aStr in xStr:
        dic = {}
        # print(aStr)
        # print("================================")
        print(aStr.text)
        print(aStr.get("href"))
        dic["title"] = aStr.text
        dic["href"] = aStr.get("href")
        craw_list.append(dic)

# for y in divStr:
#     yStr = y.select("dd.text")
#     print(yStr)
#     for aStr in yStr:
#         print("================================")
#         print(aStr.text)
#         print(aStr.get("href"))

print(craw_list)
for dic in craw_list:
    # print(dic)
    print(dic["title"])
    print(host + dic["href"])
