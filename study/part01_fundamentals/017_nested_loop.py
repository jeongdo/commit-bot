# ============================================================================
# 017 - nested_loop (중첩 루프)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. 중첩 루프의 break/continue 동작 범위를 정확히 이해한다
#   2. 외부 루프 탈출 전략 3가지를 익힌다
#   3. itertools.product로 중첩 루프를 단일 루프로 변환한다
#   4. 중첩 루프의 시간복잡도와 최적화를 이해한다
#
# [왜 필요한가]
#   - Python에는 Java처럼 레이블(label) break가 없음
#   - 외부 루프 탈출이 불편 → 올바른 패턴 학습 필수
#   - O(n²) 이상 루프는 대부분 더 효율적 알고리즘으로 대체 가능
# ============================================================================

from itertools import product

# ── LEVEL 1: 기본 중첩 루프 ─────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 기본 중첩 루프")
print("=" * 50)

# 구구단 2~4단
for i in range(2, 5):
    for j in range(1, 10):
        print(f"{i}×{j}={i*j:2d}", end="  ")
    print()

# 2D 행렬 출력
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
print("\n행렬:")
for row in matrix:
    for val in row:
        print(f"{val:3d}", end="")
    print()

# ── LEVEL 2: break/continue의 범위 ──────────────────────────────────────────

print("\nLEVEL 2: break/continue의 범위")
print("-" * 40)

# break: 가장 안쪽 루프만 탈출
print("break (안쪽 루프만 탈출):")
for i in range(3):
    for j in range(5):
        if j == 2:
            break           # 안쪽 for j 루프만 탈출
        print(f"  ({i},{j})", end="")
    print()  # 바깥 루프는 계속

# continue: 현재 이터레이션 스킵
print("\ncontinue (현재 반복 스킵):")
for i in range(4):
    for j in range(4):
        if (i + j) % 2 == 0:
            continue        # 짝수 합이면 스킵
        print(f"  ({i},{j})", end="")
print()

# ── LEVEL 3: 외부 루프 탈출 전략 ────────────────────────────────────────────

print("\nLEVEL 3: 외부 루프 탈출 전략")
print("-" * 40)

# 목표: 행렬에서 특정 값 찾기
matrix = [
    [1,  2,  3,  4],
    [5,  6,  7,  8],
    [9,  10, 11, 12],
    [13, 14, 15, 16],
]
target = 11

# 전략 1: 플래그 변수 (비권장 — 코드 복잡)
print("전략 1: 플래그 변수")
found = False
found_pos = None
for i, row in enumerate(matrix):
    for j, val in enumerate(row):
        if val == target:
            found_pos = (i, j)
            found = True
            break
    if found:
        break
print(f"  {target} 위치: {found_pos}")

# 전략 2: 함수 + return (권장!)
print("\n전략 2: 함수 + return (권장)")
def find_in_matrix(matrix, target):
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val == target:
                return (i, j)   # 바로 반환 → 모든 루프 탈출
    return None

pos = find_in_matrix(matrix, target)
print(f"  {target} 위치: {pos}")

# 전략 3: 예외 사용 (특수 상황)
print("\n전략 3: 예외 사용 (깊은 중첩)")
class Found(Exception):
    def __init__(self, pos): self.pos = pos

try:
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            for k in range(1):   # 3중 중첩 예시
                if val == target:
                    raise Found((i, j))
except Found as e:
    print(f"  {target} 위치: {e.pos}")

# 전략 4: itertools.product로 단일 루프 변환 (권장!)
print("\n전략 4: itertools.product (가장 Pythonic)")
rows = range(len(matrix))
cols = range(len(matrix[0]))
result = next(
    ((i, j) for i, j in product(rows, cols) if matrix[i][j] == target),
    None
)
print(f"  {target} 위치: {result}")

# ── LEVEL 4: 행렬 연산 패턴 ─────────────────────────────────────────────────

print("\nLEVEL 4: 행렬 연산 패턴")
print("-" * 40)

# 전치 행렬 (리스트 컴프리헨션)
def transpose(matrix):
    rows, cols = len(matrix), len(matrix[0])
    return [[matrix[r][c] for r in range(rows)] for c in range(cols)]

m = [[1,2,3],[4,5,6],[7,8,9]]
t = transpose(m)
print("원본:")
for row in m: print(f"  {row}")
print("전치:")
for row in t: print(f"  {row}")

# zip(*matrix) 로 전치
t2 = [list(row) for row in zip(*m)]
print(f"zip(*matrix) 전치: {t2}")

# 행렬 곱셈 (O(n³))
def matmul(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    return [[sum(A[i][k]*B[k][j] for k in range(p)) for j in range(m)] for i in range(n)]

A = [[1,2],[3,4]]
B = [[5,6],[7,8]]
C = matmul(A, B)
print(f"\n행렬곱 A×B = {C}")

# ── LEVEL 4: 중첩 루프 최적화 ───────────────────────────────────────────────

print("\nLEVEL 4: 중첩 루프 최적화")
print("-" * 40)

import time

n = 200

# Bad: O(n³) 삼중 루프
t1 = time.perf_counter()
count_bad = sum(1 for i in range(n) for j in range(n)
                if i + j < n)
t1 = time.perf_counter() - t1

# Good: O(n²) 수학적 최적화
t2 = time.perf_counter()
count_good = sum(n - i for i in range(n))  # j의 범위 = 0 ~ n-i-1
t2 = time.perf_counter() - t2

print(f"O(n²) 루프: {count_bad}, {t1*1000:.2f}ms")
print(f"O(n ) 합산: {count_good}, {t2*1000:.2f}ms  ← 훨씬 빠름")
print(f"결과 같음: {count_bad == count_good}")

# ── LEVEL 5: itertools.product 활용 ─────────────────────────────────────────

print("\nLEVEL 5: itertools.product 고급 활용")
print("-" * 40)

from itertools import product, combinations, permutations

# 카르테시안 곱으로 파라미터 그리드 생성 (하이퍼파라미터 탐색)
learning_rates = [0.001, 0.01, 0.1]
batch_sizes    = [16, 32, 64]
optimizers     = ["adam", "sgd"]

grid = list(product(learning_rates, batch_sizes, optimizers))
print(f"하이퍼파라미터 그리드: {len(grid)}개 조합")
for lr, bs, opt in grid[:4]:
    print(f"  lr={lr}, batch={bs}, opt={opt}")
print(f"  ... (총 {len(grid)}개)")

# 체스판 퀸 공격 범위 (combinations 활용)
def queens_attack(positions):
    """퀸들이 서로 공격 가능한 쌍 수"""
    attacks = 0
    for (r1,c1), (r2,c2) in combinations(positions, 2):
        if r1==r2 or c1==c2 or abs(r1-r2)==abs(c1-c2):
            attacks += 1
    return attacks

queens = [(0,0), (1,5), (2,3), (3,7)]
print(f"\n퀸 공격 쌍 수: {queens_attack(queens)}")

# ============================================================================
# [주의사항]
#   1. break는 가장 안쪽 루프만 탈출 — Java 레이블 break 없음
#   2. 외부 루프 탈출의 가장 깔끔한 방법: 함수 분리 + return
#   3. O(n²) 이상 루프 발견 시 알고리즘 재검토 (set, dict, numpy 등)
#   4. zip(*matrix) 로 전치하면 리스트 컴프리헨션보다 간결
#   5. itertools.product가 중첩 for보다 Pythonic
#
# [다음 단계]
#   → 018_function.py: 함수 — 1급 객체, docstring, 타입 힌트
# ============================================================================
