# ============================================================================
# 015 - while (반복문)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. while의 기본 동작과 while-else를 이해한다
#   2. while True + break 패턴으로 서버/이벤트 루프를 구현한다
#   3. 재시도(retry), 지수 백오프(exponential backoff) 패턴을 익힌다
#   4. 무한 루프 방지와 타임아웃 처리를 안다
#
# [Java 비교]
#   Java  : while, do-while (Python에 없음)
#   Python: while, while-else (Java에 없음)
#           do-while 패턴 = while True: ... if cond: break
# ============================================================================

import time
import random

random.seed(42)

# ── LEVEL 1: 기본 while ──────────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 기본 while")
print("=" * 50)

n = 1
while n <= 8:
    print(f"  n={n}", end="  ")
    n *= 2
print()

# while-else: 조건이 False로 자연 종료될 때 else 실행
print("\nwhile-else:")
i = 1
while i <= 5:
    print(f"  {i}", end=" ")
    i += 1
else:
    print("→ while 정상 완료!")

# break 시 else 건너뜀
i = 1
while i <= 5:
    if i == 3:
        break
    print(f"  {i}", end=" ")
    i += 1
else:
    print("실행 안 됨")  # break로 종료 → else 건너뜀
print("← break로 종료")

# ── LEVEL 2: do-while 패턴 (Python은 do-while 없음) ─────────────────────────

print("\nLEVEL 2: do-while 패턴")
print("-" * 40)

# Java: do { ... } while(condition);
# Python: while True: ... if not condition: break

attempt = 0
while True:
    attempt += 1
    result = random.choice(["fail", "fail", "fail", "success"])
    print(f"  시도 {attempt}: {result}")
    if result == "success" or attempt >= 5:
        break

print(f"  → {attempt}번 만에 종료")

# ── LEVEL 3: while True + break — 서버/이벤트 루프 ──────────────────────────

print("\nLEVEL 3: while True 서버 루프 패턴")
print("-" * 40)

# 실제 서버는 이런 구조:
# while True:
#     client = server.accept()
#     handle_client(client)

# 시뮬레이션
class MockEventQueue:
    def __init__(self, events):
        self._events = iter(events)

    def get(self, timeout=1):
        try:
            return next(self._events)
        except StopIteration:
            return {"type": "SHUTDOWN"}

def process_event(event):
    return f"처리: {event['type']} — {event.get('data','')}"

events = [
    {"type": "LOGIN",   "data": "user=Alice"},
    {"type": "REQUEST", "data": "GET /api/users"},
    {"type": "REQUEST", "data": "POST /api/orders"},
    {"type": "LOGOUT",  "data": "user=Alice"},
]
queue = MockEventQueue(events)

print("이벤트 루프:")
processed = 0
while True:
    event = queue.get(timeout=1)
    if event["type"] == "SHUTDOWN":
        print("  SHUTDOWN 수신 → 루프 종료")
        break
    print(f"  {process_event(event)}")
    processed += 1

print(f"  처리 이벤트: {processed}개")

# ── LEVEL 4: 재시도 (Retry) 패턴 ────────────────────────────────────────────

print("\nLEVEL 4: 재시도(Retry) 패턴")
print("-" * 40)

# 패턴 1: 기본 재시도
def retry(func, max_attempts=3, exceptions=(Exception,)):
    """실패 시 max_attempts 횟수까지 재시도"""
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except exceptions as e:
            last_exc = e
            print(f"  시도 {attempt}/{max_attempts} 실패: {e}")
            if attempt < max_attempts:
                time.sleep(0.01)
    raise last_exc

call_count = [0]
def unstable_api():
    call_count[0] += 1
    if call_count[0] < 3:
        raise ConnectionError(f"연결 실패 (시도 {call_count[0]})")
    return "API 성공"

try:
    result = retry(unstable_api, max_attempts=5)
    print(f"  결과: {result}")
except ConnectionError as e:
    print(f"  최종 실패: {e}")

# 패턴 2: 지수 백오프 (Exponential Backoff)
def retry_with_backoff(func, max_attempts=5, base_delay=0.01):
    """실패 시 대기 시간을 지수적으로 증가"""
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = base_delay * (2 ** attempt)   # 0.01, 0.02, 0.04, 0.08...
            jitter = random.uniform(0, delay * 0.1) # 지터: 동시 재시도 방지
            print(f"  {attempt+1}번 실패, {delay:.3f}s 후 재시도")
            time.sleep(delay + jitter)

call_count[0] = 0
try:
    result = retry_with_backoff(unstable_api, max_attempts=5)
    print(f"  결과: {result}")
except ConnectionError as e:
    print(f"  최종 실패: {e}")

# 패턴 3: 데코레이터로 재시도
import functools

def with_retry(max_attempts=3, delay=0.01, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
        return wrapper
    return decorator

@with_retry(max_attempts=3, delay=0.01, exceptions=(ValueError,))
def flaky_function(x):
    if random.random() < 0.5:
        raise ValueError("임시 오류")
    return x * 2

result = flaky_function(21)
print(f"\n데코레이터 재시도 결과: {result}")

# ── LEVEL 5: 타임아웃 처리 ──────────────────────────────────────────────────

print("\nLEVEL 5: 타임아웃 처리")
print("-" * 40)

import signal
import threading

# 방법 1: 시간 체크 루프
def long_running_task_with_timeout(timeout_seconds=0.1):
    start = time.monotonic()
    results = []
    i = 0
    while True:
        # 타임아웃 체크
        if time.monotonic() - start > timeout_seconds:
            print(f"  타임아웃! {i}번 처리 후 종료")
            break
        results.append(i * i)
        i += 1
    return results

data = long_running_task_with_timeout(0.001)
print(f"  처리된 항목 수: {len(data)}")

# 방법 2: threading.Event를 이용한 중단
stop_event = threading.Event()

def worker(stop_event):
    count = 0
    while not stop_event.is_set():
        count += 1
        time.sleep(0.001)
    return count

# 짧은 실행 후 중단
t = threading.Thread(target=lambda: None)  # 단순 예시
stop_event.set()  # 즉시 중단
print("  threading.Event 기반 중단: 구현 완료")

# ============================================================================
# [주의사항]
#   1. 무한 루프 탈출 조건을 항상 명확히 설계
#   2. while True에서 예외 처리 없으면 예외 발생 시 루프 탈출
#   3. 재시도 시 지터(jitter) 추가 → 동시 요청 폭풍(thundering herd) 방지
#   4. sleep() 은 CPU 낭비 없는 대기 — busy-wait 루프 금지
#   5. while-else의 else는 break 없이 종료 시만 실행
#
# [다음 단계]
#   → 016_range.py: range() — 게으른 시퀀스, 메모리 효율
# ============================================================================
