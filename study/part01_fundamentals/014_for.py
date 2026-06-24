# ============================================================================
# 014 - for (반복문)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. Python for문이 이터러블 프로토콜 기반임을 이해한다
#   2. for-else, break/continue의 동작 원리를 익힌다
#   3. enumerate, zip, reversed 등과 결합하는 패턴을 체화한다
#   4. 루프 내 안티패턴을 파악하고 Pythonic하게 고친다
#
# [왜 필요한가]
#   - Python for문 = Java for-each, 항상 이터러블을 순회
#   - 내부적으로 iter() + next() 호출 → PART 10 이터레이터의 기반
#   - for-else는 Python 고유 기능 — 검색 패턴에 매우 유용
#
# [Java 비교]
#   Java  : for(int i=0; i<n; i++) 인덱스 기반
#           for(String s : list) for-each
#   Python: for item in iterable: 항상 for-each
#           for i in range(n):    인덱스 필요 시
# ============================================================================

from itertools import zip_longest, islice

# ── LEVEL 1: 기본 for 루프 ───────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 기본 for 루프")
print("=" * 50)

# 리스트, 튜플, 문자열, dict, set 모두 순회 가능
for fruit in ["apple", "banana", "cherry"]:
    print(f"  {fruit}")

print()
for char in "Python":
    print(char, end=" ")
print()

# dict 순회
scores = {"Alice": 92, "Bob": 85, "Carol": 88}
for name, score in scores.items():   # 키+값 동시
    print(f"  {name}: {score}")

# range()
print("\nrange(2,10,2):", end=" ")
for i in range(2, 10, 2):
    print(i, end=" ")
print()

print("역순 range(5,0,-1):", end=" ")
for i in range(5, 0, -1):
    print(i, end=" ")
print()

# ── LEVEL 2: enumerate / zip / reversed ─────────────────────────────────────

print("\nLEVEL 2: enumerate / zip / reversed")
print("-" * 40)

fruits = ["apple", "banana", "cherry"]

# enumerate: 인덱스 + 값 동시 (range(len()) 안티패턴 대체)
print("enumerate:")
for i, fruit in enumerate(fruits, start=1):   # 1부터 시작
    print(f"  {i}. {fruit}")

# zip: 두 이터러블 병렬 순회
names  = ["Alice", "Bob", "Carol"]
scores_list = [92, 85, 88]
print("\nzip:")
for name, score in zip(names, scores_list):
    print(f"  {name}: {score}")

# zip_longest: 긴 쪽 기준 (짧은 쪽은 fillvalue로 채움)
print("\nzip_longest:")
a = [1, 2, 3]
b = ["x", "y"]
for ai, bi in zip_longest(a, b, fillvalue="?"):
    print(f"  ({ai}, {bi})")

# reversed: 역순 이터레이터 (새 리스트 안 만듦)
print("\nreversed:")
for item in reversed(fruits):
    print(f"  {item}", end=" ")
print()

# ── LEVEL 3: for-else — break 없이 완료 시 실행 ─────────────────────────────

print("\nLEVEL 3: for-else")
print("-" * 40)

# for-else: break가 실행되지 않고 루프가 정상 완료되면 else 실행
# Java에는 없는 Python 고유 문법

# 검색 패턴
def find_prime(nums):
    results = []
    for n in nums:
        for d in range(2, int(n**0.5) + 1):
            if n % d == 0:
                break           # 약수 발견 → 소수 아님
        else:
            results.append(n)   # break 안 됨 → 소수
    return results

primes = find_prime(range(2, 30))
print(f"소수 (2~29): {primes}")

# 인증 패턴
def authenticate(user_id, valid_tokens):
    for token in valid_tokens:
        if token["user_id"] == user_id and token["active"]:
            print(f"  인증 성공: user_id={user_id}")
            break
    else:
        print(f"  인증 실패: user_id={user_id}")

tokens = [
    {"user_id": 1, "active": True},
    {"user_id": 2, "active": False},
]
authenticate(1, tokens)
authenticate(2, tokens)
authenticate(3, tokens)

# ── LEVEL 3: for 루프 내부 동작 (이터레이터 프로토콜) ──────────────────────

print("\nLEVEL 3: for 루프 내부 동작")
print("-" * 40)

# for x in iterable: 은 아래와 완전히 동일
# 1) it = iter(iterable)  → __iter__() 호출
# 2) while True:
#        try: x = next(it)  → __next__() 호출
#        except StopIteration: break

my_list = [10, 20, 30]
it = iter(my_list)          # 이터레이터 생성
print("iter() + next() 직접 사용:")
while True:
    try:
        item = next(it)
        print(f"  next(it) = {item}")
    except StopIteration:
        print("  StopIteration → 루프 종료")
        break

# ── LEVEL 4: Pythonic 루프 패턴 ─────────────────────────────────────────────

print("\nLEVEL 4: Pythonic 루프 패턴")
print("-" * 40)

# 패턴 1: 안티패턴 vs Pythonic
items = ["a", "b", "c", "d"]

# Anti: range(len()) 인덱스 루프
print("Anti-pattern:")
for i in range(len(items)):
    print(f"  items[{i}] = {items[i]}", end="  ")
print()

# Pythonic: 직접 순회
print("Pythonic:")
for item in items:
    print(f"  {item}", end="  ")
print()

# 인덱스 필요시: enumerate
print("인덱스 필요:")
for i, item in enumerate(items):
    print(f"  [{i}]={item}", end="  ")
print()

# 패턴 2: 루프 내 리스트 수정 금지
nums = [1, 2, 3, 4, 5, 6]
# Bad: for n in nums: if n%2==0: nums.remove(n) → 건너뜀 발생
# Good: 컴프리헨션으로 새 리스트
odds = [n for n in nums if n % 2 != 0]
print(f"\n홀수만: {odds}")

# 패턴 3: 슬라이딩 윈도우
data = [1, 3, 5, 2, 4, 7, 6]
window = 3
print(f"\n슬라이딩 윈도우(크기={window}):")
for i in range(len(data) - window + 1):
    w = data[i:i+window]
    print(f"  {w} → 합={sum(w)}, 평균={sum(w)/window:.1f}")

# 패턴 4: 청크(배치) 처리
def chunks(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i+size]

records = list(range(1, 22))
print(f"\n청크(크기=5) 처리:")
for i, chunk in enumerate(chunks(records, 5)):
    print(f"  배치 {i+1}: {chunk}")

# 패턴 5: 중첩 루프 → itertools.product
from itertools import product
print("\nitertools.product (중첩 루프 대체):")
for x, y in product(range(3), range(3)):
    print(f"  ({x},{y})", end=" ")
print()

# 패턴 6: 조건부 순회
print("\n짝수 인덱스만 (islice):")
for item in islice(enumerate(items), 0, None, 2):  # 스텝 2
    print(f"  {item}", end=" ")
print()

# ── LEVEL 5: 오픈소스 패턴 ──────────────────────────────────────────────────

print("\nLEVEL 5: 오픈소스 패턴")
print("-" * 40)

# 패턴: 대용량 파일 라인 처리 (제너레이터 기반)
import io

def process_csv(fileobj, batch_size=3):
    """대용량 CSV를 배치로 처리 — 메모리 효율적"""
    header = next(fileobj).strip().split(",")
    batch = []
    for line in fileobj:
        row = dict(zip(header, line.strip().split(",")))
        batch.append(row)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch   # 나머지

# 시뮬레이션
csv_data = """name,score,grade
Alice,92,A
Bob,85,B
Carol,88,B
Dave,91,A
Eve,79,C
Frank,95,A"""

fileobj = io.StringIO(csv_data)
print("배치 처리:")
for batch_num, batch in enumerate(process_csv(fileobj, batch_size=2), 1):
    print(f"  배치 {batch_num}: {[r['name'] for r in batch]}")

# ============================================================================
# [주의사항]
#   1. 루프 중 컬렉션 수정 금지 → 컴프리헨션 또는 복사본 사용
#   2. range(len(lst)) 대신 enumerate(lst) 사용 (Pythonic)
#   3. for-else의 else는 "break 없이 완료"를 의미 — 혼동 주의
#   4. StopIteration이 for 루프를 종료시킴 (제너레이터 기반)
#   5. 대용량 데이터는 제너레이터/yield로 메모리 효율화
#
# [다음 단계]
#   → 015_while.py: while 루프 — 서버 루프, 재시도 패턴
# ============================================================================
