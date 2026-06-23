# Chapter07-01

# Asyncio : 비동기 I/O Coroutine을 쉽게 활용할 수 있게 도와주는 라이브러리

# 비동기 I/O Coroutine 작업
# Generator -> 반복적인 객체 Return 사용

# blocking i/o : 호출된 함수가 자신의 작업이 완료 될 때까지 제어권을 가지고 있음. 타 함수는 대기
# non-blocking 비동기 처리 : 호출된 함수가 리턴 후 호출한 함수(메인 루틴)에 제어권 전달 -> 타함수는 일 지속

# 쓰레드의 단점 : 디버깅, 자원 접근 시 레이스컨디션(경쟁상태), 데드락(Dead Lock)) 등을 고려 후 코딩
# 코루틴의 장점 : 하나의 루틴만 실행 -> 락 관리 필요 없음, 제어권으로 실행
# 코루틴의 단점 : 사용 함수가 비동기로 구현이 되어 있어야 하거나, 또는 직접 비동기로 구현해야 한다. 비동기 라이브러리라도 동기함수를 적용하면 동기화 됨.

# Asyncio 웹 스크랩핑 실습
# aiohttp 권장
import asyncio
import timeit
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor  # Combining Coroutines with Threads and Processes
import threading

# 실행 시작 시간
start = timeit.default_timer()
# 서비스 방향이 비슷한 사이트로 실습 권장(예 : 게시판성 커뮤니티)
urls = ['http://daum.net', 'https://naver.com', 'http://mlbpark.donga.com/', 'https://tistory.com',
        'https://wemakeprice.com/']


async def fetch(url, executor):
    # 쓰레드명 출력
    print('Thread Name :', threading.current_thread().getName(), 'Start', url)

    # 실행 urlopen 이 블럭함 수 이기 때문에 non-block 로 만들어 줌
    # loop는 메인 영역에서 선언해서 참조할 수 있다.
    res = await loop.run_in_executor(executor, urlopen, url)

    print('Thread Name :', threading.current_thread().getName(), 'Done', url)

    # 결과 반환
    # return res.read()
    return res.read()[0:5]


# main은 async 비동기 함수이다.
async def main():
    # 쓰레드 풀 생성
    executor = ThreadPoolExecutor(max_workers=10)

    # future 객체 모아서 gather에서 실행
    futures = [
        asyncio.ensure_future(fetch(url, executor)) for url in urls
    ]

    # 결과 취합 await == yield, futures가 끝날때 까지, 리스트니깐 언팩킹
    rst = await asyncio.gather(*futures)

    print()
    print('Result : ', rst)


if __name__ == '__main__':
    # 루프 초기화
    loop = asyncio.get_event_loop()

    # 작업 완료 까지 루프는 계속 된다. 대기
    loop.run_until_complete(main())

    # 수행 시간 계산
    duration = timeit.default_timer() - start
    # 총 실행 시간
    print('Total Running Time : ', duration)
