ds = [1, 2, 3, 4]
for i in ds:
    print(i, end=' ')


# Iterable 객체 : iter 함수에 인자로 전달 가능한 객체
# Iterator 객체 : iter 함수가 생성해서 반환하는 객체


ir = iter(ds)  # ir은 Iterator 객체이며 iter() 통해 얻을 수 있다.  ds는 iter 함수에 인자로 전달 가능한 객체로 Iterable 객체라고 한다.

print(next(ir))
print(next(ir))
print(next(ir))
print(next(ir))
# print(next(ir)) # StopIteration 예외 발생

print("================================================")

ir2 = ds.__iter__()  # iter 함수 호출의 실제 모습  iter() --> ds의 __iter__() 객체함수로 바꾸어서 호출하는 것이다. 이것을 스페셜 메소드라고 부른다.

print(ir2.__next__())   # next 함수 호출의 실제 모습,  이런 방식은으로 메소드를 직접 호출말고, 다르게 지정한 방법으로 호출해라.

print("================================================")

tp = ('one', 'two', 'three')
ir3 = iter(tp)

print(next(ir3))

str1 = 'four'
ir4 = iter(str1)

print(next(ir4))

print("================================================")

print(dir(ds))  # 리스트 객체 안에 있는 것들의 이름을 보여라. '__iter__' 를 찾을 수 있다.

print(hasattr(ds, '__iter__'))  # 리스트에 __iter__ 함수가 있나요?

print("================================================")

# 사실 for 루프도 값을 하나씩 꺼내기 위해 iterable 객체를 생성해서 이것의 도움을 받는 것이었다.

for i in ds:
    print(i, end=' ')

# for 루프의 내부 처리도

ir5 = iter(ds)
while True:
    try:
        i = next(ir5)
        print(i, end='\n')
    except StopIteration:
        break

print("================================================")

ir6 = iter(ds)          # next 로 호출이 끝나서 itr5 를 재사용하지 않았다.

for i in ir6:           # for 루프에 iterator 객체를 대체해도 정상 동작한다. 즉, iterator 객체는 iterable 객체 자격도 가지고 있는 것이다.
    print(i, end='\n')

print("================================================")

ir7 = iter([1, 2, 3])   # 리스트의 iterator 객체를 얻음.
ir8 = iter(ir7)         # iterator 객체를 전달하면서 다시 전달된 iterator 객체를 그대로 되돌려 준다.

# 이는 iterable 객체와 마찬가지로 iterator 객체도 iter 함수의 인자가 될 수 있고, 또 그 결과로 iterator 객체가 반환되기 때문이다.
# 비록 iter 함수에 전달된 iterator 객체가 그대로 반환되는 것이지만 말이다.

print(ir7 is ir8)
print(id(ir7))          # ir7이 참조하는 객체의 위치 정보 확인
print(id(ir8))          # ir8이 참조하는 객체의 위치 정보 확인
