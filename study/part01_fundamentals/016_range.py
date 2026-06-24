# ============================================================================
# 016 - range() (게으른 시퀀스)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. range가 리스트가 아닌 게으른(lazy) 시퀀스 객체임을 이해한다
#   2. range의 메모리 효율성과 O(1) in 연산을 파악한다
#   3. 배치 처리, 역순, 짝수/홀수 인덱스 등 실무 패턴을 익힌다
#
# [왜 필요한가]
#   - for i in range(10**9): 도 메모리 48 bytes만 사용 (리스트라면 8GB!)
#   - n in range(10**9) 는 O(1) — 리스트라면 O(n) 탐색
#   - 모든 반복 카운터, 인덱스 기반 루프의 기반
#
# [Java 비교]
#   Java  : for(int i=0; i<n; i++) — 매 루프 카운터 증가
#   Python: for i in range(n)      — range 객체가 next() 제공
# ============================================================================

import sys

# ── LEVEL 1: range 기본 ──────────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: range 기본")
print("=" * 50)

# range(stop): 0 ~ stop-1
r1 = range(5)
print(f"range(5)       = {list(r1)}")         # [0,1,2,3,4]

# range(start, stop): start ~ stop-1
r2 = range(2, 8)
print(f"range(2,8)     = {list(r2)}")         # [2,3,4,5,6,7]

# range(start, stop, step): start, start+step, ...
r3 = range(0, 20, 4)
print(f"range(0,20,4)  = {list(r3)}")         # [0,4,8,12,16]

r4 = range(10, 0, -2)
print(f"range(10,0,-2) = {list(r4)}")         # [10,8,6,4,2]

# 빈 range
r5 = range(5, 2)   # start > stop, step > 0
print(f"range(5,2)     = {list(r5)}, len={len(r5)}")  # [] 0

# ── LEVEL 2: range는 시퀀스 — 인덱싱, 슬라이싱, in ──────────────────────────

print("\nLEVEL 2: range는 시퀀스")
print("-" * 40)

r = range(0, 100, 3)   # 0, 3, 6, ..., 99

print(f"len(range(0,100,3))   = {len(r)}")     # 34
print(f"r[0]                  = {r[0]}")        # 0
print(f"r[-1]                 = {r[-1]}")       # 99
print(f"r[5]                  = {r[5]}")        # 15
print(f"r[2:6]                = {list(r[2:6])}") # [6,9,12,15]
print(f"33 in r               = {33 in r}")     # True  (O(1)!)
print(f"34 in r               = {34 in r}")     # False (O(1)!)

# ── LEVEL 3: 메모리 효율성 — 핵심! ──────────────────────────────────────────

print("\nLEVEL 3: 메모리 효율성")
print("-" * 40)

big_n = 10_000_000

r_big  = range(big_n)
l_big  = list(range(1000))   # 1000개만 (10M 개 리스트는 너무 큼)

print(f"range({big_n:,})   = {sys.getsizeof(r_big)} bytes (항상 고정!)")
print(f"list(range(1000))  = {sys.getsizeof(l_big)} bytes")
print(f"range(10억)        = 48 bytes 예상 (리스트라면 ≈ 8GB)")

# O(1) in 연산 원리: 수식으로 계산
# n in range(start, stop, step)
# → start <= n < stop 이고 (n - start) % step == 0 인지 수식 계산
import time

BIG = 10**9

t1 = time.perf_counter()
result = BIG - 1 in range(BIG)   # O(1) — 수식 계산
t1 = time.perf_counter() - t1

print(f"\n{BIG-1} in range({BIG}) = {result}, 시간: {t1*1000:.4f}ms (O(1)!)")

# range의 속성
r = range(3, 20, 4)
print(f"\nrange(3,20,4) 속성:")
print(f"  start={r.start}, stop={r.stop}, step={r.step}")
print(f"  len={len(r)}, r[0]={r[0]}, r[-1]={r[-1]}")

# ── LEVEL 4: 실무 패턴 ───────────────────────────────────────────────────────

print("\nLEVEL 4: 실무 패턴")
print("-" * 40)

# 패턴 1: 배치(청크) 처리
data = list(range(1, 23))
batch_size = 5
print(f"배치 처리 (크기={batch_size}):")
for start in range(0, len(data), batch_size):
    batch = data[start:start + batch_size]
    print(f"  배치 {start//batch_size + 1}: {batch}")

# 패턴 2: 짝수/홀수 인덱스
items = list("ABCDEFGHIJ")
evens = items[::2]    # 0,2,4,6,8
odds  = items[1::2]   # 1,3,5,7,9
print(f"\n짝수 인덱스: {evens}")
print(f"홀수 인덱스: {odds}")

# 패턴 3: 역순 순회
print(f"\n역순 range:")
for i in range(len(items) - 1, -1, -1):
    print(f"  items[{i}] = {items[i]}", end="  ")
print()

# 패턴 4: 2D 좌표 생성
print("\n2D 격자 (range 조합):")
size = 3
grid = [(x, y) for y in range(size) for x in range(size)]
print(f"  {grid}")

# 패턴 5: 슬라이딩 윈도우
data = [1, 3, 5, 2, 4, 7, 6, 8]
window_size = 3
print(f"\n슬라이딩 윈도우 (크기={window_size}):")
for i in range(len(data) - window_size + 1):
    window = data[i:i+window_size]
    print(f"  [{i}:{i+window_size}] = {window}, 평균={sum(window)/window_size:.1f}")

# ── LEVEL 5: 커스텀 range 유사 클래스 ──────────────────────────────────────

print("\nLEVEL 5: 커스텀 게으른 시퀀스 (range 원리 재현)")
print("-" * 40)

class ArithSequence:
    """등차수열 시퀀스 — range와 유사한 게으른 객체"""

    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop  = stop
        self.step  = step

    def __len__(self):
        if self.step > 0:
            return max(0, (self.stop - self.start + self.step - 1) // self.step)
        else:
            return max(0, (self.start - self.stop - self.step - 1) // (-self.step))

    def __getitem__(self, index):
        if index < 0:
            index += len(self)
        if not 0 <= index < len(self):
            raise IndexError("index out of range")
        return self.start + index * self.step

    def __contains__(self, value):
        if self.step > 0:
            if not (self.start <= value < self.stop):
                return False
        else:
            if not (self.stop < value <= self.start):
                return False
        return (value - self.start) % self.step == 0

    def __iter__(self):
        current = self.start
        while (self.step > 0 and current < self.stop) or \
              (self.step < 0 and current > self.stop):
            yield current
            current += self.step

    def __repr__(self):
        return f"ArithSequence({self.start}, {self.stop}, {self.step})"

seq = ArithSequence(0, 20, 3)
print(f"ArithSequence(0,20,3):")
print(f"  len={len(seq)}, [0]={seq[0]}, [-1]={seq[-1]}")
print(f"  9 in seq: {9 in seq}")     # True  (0,3,6,9,12,15,18)
print(f"  10 in seq: {10 in seq}")   # False
print(f"  list: {list(seq)}")

print(f"\nsys.getsizeof(seq) = {sys.getsizeof(seq)} bytes (작음!)")

# ============================================================================
# [주의사항]
#   1. list(range(n))은 메모리 O(n) → 큰 n에는 range 직접 사용
#   2. range는 반복 가능(iterable)하지만 소진(exhaust)되지 않음
#      (이터레이터가 아님 → 여러 번 순회 가능)
#   3. range는 float step 불가 → numpy.arange() 또는 math 사용
#   4. range 슬라이싱은 range 반환 (리스트 아님)
#
# [다음 단계]
#   → 017_nested_loop.py: 중첩 루프와 외부 루프 탈출 전략
# ============================================================================
