dic = {"id": "leee", "pw": 111, 999: "seoul"}

print("============= list(dic)로 리스트로 형변환을 한번 해주어야 한다.  ==================")

# (['id', 'pw', 999, 'addr']), 튜퓰로 반환되고, 이걸 다시 리스트로 변환해주어야 한다.
# for x in list(dic.keys()): # dic2.keys = dic2
for x in list(dic):
    print(dic[x])
    del dic[x]  # del dic[x]는 x번째 요소값을 삭제한다. 결국 빈 객체만 남게 된다.

print(len(dic))
print(type(dic))
print(dic)

