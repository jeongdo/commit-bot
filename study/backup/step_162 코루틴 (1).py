# Chapter06-03
# 흐름제어, 병행성(Concurrency)

# 코루틴(Coroutine) : 단일(싱글) 쓰레드, 스택을 기반으로 동작하는 비동기 작업
# 쓰레드 : OS 관리, CPU 코어에서 실시간, 시분할 비동기 작업 -> 멀티쓰레드

# yield : 메인 <-> 서브
# 코루틴 제어, 상태, 양방향 전송
# yield from

# 서브루틴 : 메인루틴에서 호출 -> 서브루틴에서 수행(흐름제어)
# 코루틴 : 루틴 실행 중 중지 ->  동시성 프로그래밍
# 코루틴 : 쓰레드에 비해 오버헤드 감소
# 쓰레드 : 싱글쓰레드 -> 멀티쓰레드 -> 복잡 -> 공유되는 자원 -> 교착 상태 발생 가능성, 컨텍스트 스위칭 비용 발생, 자원 소비 가능성 증가

# 코루틴 Ex1
def coroutine1():
    print('>>> coroutine started.')
    i = yield
    print('>>> coroutine received : {}'.format(i))


# 제네레이터 선언
cr1 = coroutine1()

print(cr1, type(cr1))

# yield 지점 까지 서브루틴 수행
next(cr1)

# 아무런 값을 전달하지 않으면 기본 전달 값 None, 즉 i = None
# next(cr1)

# 메인루틴과 서브루틴 간의 데이터 전송
cr1.send(100)  # i = yield 먼저 있다가, SEND가 되면, 지정된 값이 i로 전송되고, next가 호출된 것과 같이 결과 발생


# 잘못된 사용

# cr2 = coroutine1()
# next 없이 바로 send를 하면, 예외 발생한다.
# cr2.send(100) # 예외 발생
