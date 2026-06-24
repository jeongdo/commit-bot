# ============================================================================
# 024 - global_variable (전역 변수와 모듈 상태)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. global/nonlocal 키워드의 정확한 동작을 이해한다
#   2. 전역 변수의 문제점과 올바른 대안을 안다
#   3. 모듈 수준 상태를 안전하게 관리하는 패턴을 익힌다
#   4. 스레드 안전한 공유 상태 관리를 미리 파악한다
# ============================================================================

import threading
import time

# ── LEVEL 1: global 키워드 ──────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: global 키워드")
print("=" * 50)

request_count = 0    # 전역 카운터

def handle_request(path):
    global request_count
    request_count += 1
    return f"[{request_count}] {path}"

print(handle_request("/"))
print(handle_request("/users"))
print(handle_request("/orders"))
print(f"총 요청: {request_count}회")

# global 없이 읽기는 가능
APP_NAME = "MyApp"

def show_app():
    print(f"  앱: {APP_NAME}")   # 전역 읽기 → global 불필요

show_app()

# ── LEVEL 2: nonlocal 키워드 ────────────────────────────────────────────────

print("\nLEVEL 2: nonlocal 키워드")
print("-" * 40)

def make_bank_account(initial=0):
    """클로저로 구현한 간단한 은행 계좌"""
    balance = initial
    history = []

    def deposit(amount):
        nonlocal balance
        balance += amount
        history.append(f"+{amount} → {balance}")
        return balance

    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return None, "잔액 부족"
        balance -= amount
        history.append(f"-{amount} → {balance}")
        return balance, "성공"

    def get_balance():
        return balance   # 읽기 → nonlocal 불필요

    def get_history():
        return list(history)

    return deposit, withdraw, get_balance, get_history

dep, wit, bal, hist = make_bank_account(1000)
print(f"초기 잔액: {bal()}")
dep(500)
dep(200)
wit(300)
result, msg = wit(2000)
print(f"2000 출금: {result}, {msg}")
print(f"최종 잔액: {bal()}")
print(f"거래 내역: {hist()}")

# ── LEVEL 3: 전역 변수의 문제점 ─────────────────────────────────────────────

print("\nLEVEL 3: 전역 변수의 문제점")
print("-" * 40)

# 문제 1: 테스트 어려움 (이전 상태가 다음 테스트에 영향)
_bad_global = 0

def increment_bad():
    global _bad_global
    _bad_global += 1
    return _bad_global

# 테스트 간 격리 불가
print(f"1번 호출: {increment_bad()}")
print(f"2번 호출: {increment_bad()}")
# 3번 테스트 시작 시 _bad_global=2 → 테스트 실패 가능

# 문제 2: 스레드 안전 문제
shared_counter = 0
lock = threading.Lock()

def increment_unsafe():
    global shared_counter
    # 읽기-증가-쓰기 사이에 다른 스레드 개입 가능!
    current = shared_counter
    time.sleep(0.0001)
    shared_counter = current + 1

def increment_safe():
    global shared_counter
    with lock:    # 원자적 연산 보장
        current = shared_counter
        shared_counter = current + 1

# 안전하지 않은 버전 테스트
shared_counter = 0
threads = [threading.Thread(target=increment_unsafe) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
print(f"\n비안전 10개 스레드: {shared_counter} (예상 10, 실제 더 적을 수 있음)")

shared_counter = 0
threads = [threading.Thread(target=increment_safe) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
print(f"안전 10개 스레드: {shared_counter} (항상 10)")

# ── LEVEL 4: 전역 상태 대안 패턴 ────────────────────────────────────────────

print("\nLEVEL 4: 전역 상태 대안")
print("-" * 40)

# 대안 1: 클래스로 상태 캡슐화 (권장)
class RequestCounter:
    def __init__(self):
        self._count = 0
        self._lock  = threading.Lock()

    def increment(self):
        with self._lock:
            self._count += 1
            return self._count

    def reset(self):
        with self._lock:
            self._count = 0

    @property
    def value(self):
        return self._count

    def __repr__(self):
        return f"RequestCounter({self._count})"

counter = RequestCounter()
counter.increment()
counter.increment()
print(f"클래스 카운터: {counter}")   # RequestCounter(2)
counter.reset()
print(f"리셋 후: {counter.value}")   # 0

# 대안 2: 컨텍스트 객체 (요청별 독립 상태)
class AppContext:
    """요청별 독립 컨텍스트 — 전역 상태 없음"""
    def __init__(self, user_id, session_id):
        self.user_id    = user_id
        self.session_id = session_id
        self.log        = []
        self.start_time = time.monotonic()

    def record(self, event):
        elapsed = time.monotonic() - self.start_time
        self.log.append(f"[{elapsed:.3f}s] {event}")

    def summary(self):
        return {
            "user_id":    self.user_id,
            "session_id": self.session_id,
            "events":     len(self.log),
        }

def process_request(ctx: AppContext, path: str):
    ctx.record(f"요청 시작: {path}")
    # 처리...
    ctx.record(f"요청 완료: {path}")
    return f"OK: {path}"

ctx1 = AppContext(user_id=1, session_id="abc")
ctx2 = AppContext(user_id=2, session_id="xyz")

process_request(ctx1, "/users")
process_request(ctx2, "/orders")
print(f"\n컨텍스트 1: {ctx1.summary()}")
print(f"컨텍스트 2: {ctx2.summary()}")

# 대안 3: 설정을 파라미터로 전달
def build_report(data, config=None):
    """전역 설정 대신 파라미터로 전달"""
    config = config or {"format": "text", "max_rows": 100}
    rows = data[:config["max_rows"]]
    return f"Report({config['format']}): {len(rows)}행"

print(f"\n{build_report(list(range(200)))}")
print(f"{build_report(list(range(200)), {'format': 'json', 'max_rows': 50})}")

# ── LEVEL 5: 모듈 수준 싱글톤 ───────────────────────────────────────────────

print("\nLEVEL 5: 모듈 수준 싱글톤 (권장 패턴)")
print("-" * 40)

# Python 모듈 자체가 싱글톤 — 한 번만 로드됨
# 모듈 수준 변수 = 사실상 싱글톤

class _Config:
    """모듈 레벨 설정 싱글톤"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data = {
                "debug":   False,
                "version": "1.0.0",
            }
        return cls._instance

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value

    def update(self, **kwargs):
        self._data.update(kwargs)

# 어디서든 Config()는 같은 인스턴스
config = _Config()
config.set("debug", True)

config2 = _Config()   # 같은 인스턴스!
print(f"config is config2: {config is config2}")   # True
print(f"debug (config2):   {config2.get('debug')}")  # True (config에서 설정한 값)

# ============================================================================
# [주의사항]
#   1. global 변수 최소화 — 상수만 모듈 레벨에 (UPPER_CASE)
#   2. 멀티스레드: global 변수 수정 시 Lock 필수
#   3. 테스트 전 global 변수 초기화/격리 필수 (fixture 패턴)
#   4. 모듈 import는 한 번만 → 모듈 수준 변수는 자연스러운 싱글톤
#   5. 전역 상태 피하고 싶으면: 의존성 주입(DI) 패턴 사용
#
# [다음 단계]
#   → 025_main_function.py: __name__ 과 진입점 설계
# ============================================================================
