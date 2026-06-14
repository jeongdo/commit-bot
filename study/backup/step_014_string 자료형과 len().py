str1 = "hello " + "world"
print(str1)
print(type(str1))

print("======================================")

str2 = str1 * 3
print(str2)

print("======================================")

print(str1[2], str1[3], str1[4])

print(str1[2:5])

print("======================================")

# str1[0] = 'K'  # 한번 담겨진 문자열은 수정이 불가능하다

for i in str1:
    print(i, end=' ')

print()
print("======================================")

print(len(str1))


def so_simple(s):
    print(s)
    return "Bye~"


r = so_simple("Hello")
print(r)
