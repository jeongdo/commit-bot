# ============================================================================
# 008 - str (문자열)
# Python Mastery Curriculum | PART 1: Python Fundamentals
# ============================================================================
#
# [학습 목표]
#   1. Python str의 불변성(immutability)과 유니코드 지원을 이해한다
#   2. f-string의 모든 포맷 옵션을 익힌다
#   3. 자주 쓰는 str 메서드를 실무 패턴으로 체화한다
#   4. 인코딩/디코딩 (str ↔ bytes) 처리를 안다
#
# [왜 필요한가]
#   - 모든 프로그램의 I/O는 결국 문자열 처리
#   - 불변성 이해 없이는 str += 반복의 O(n²) 함정에 빠짐
#   - 한국어 처리 시 인코딩 문제 반드시 직면
#
# [Java 비교]
#   Java  : String (불변), StringBuilder (가변), char 타입 별도 존재
#           "A" + "B" 반복 → StringBuilder로 최적화 필요
#   Python: str (불변), 가변은 list + join, char 없음 (길이1 str)
#           "".join([...])로 효율적 연결
# ============================================================================

import sys
import re

# ── LEVEL 1: 문자열 리터럴 ───────────────────────────────────────────────────

print("=" * 50)
print("LEVEL 1: 문자열 리터럴")
print("=" * 50)

s1 = "double quotes"
s2 = 'single quotes'
s3 = """triple double
multi-line 가능"""
s4 = '''triple single
multi-line'''

# raw string: 이스케이프 무시 (정규식, 경로에 필수)
path  = r"C:\Users\Alice\docs"   # 백슬래시 그대로 유지
regex = r"\d{3}-\d{4}"            # 정규식 패턴

# 바이트 리터럴
b = b"hello bytes"

print(s3)
print(f"raw path  : {path}")
print(f"raw regex : {regex}")
print(f"bytes     : {b}")

# 이스케이프 시퀀스
print("\n이스케이프:")
print("탭\t사이")
print("줄\n바꿈")
print("따옴표: \"인용\"")
print("유니코드: \u4e2d\ub2e8 →", "\u4e2d\ub2e8")    # 中단
print("이모지 : \U0001F600 →", "\U0001F600")          # 😀

# ── LEVEL 2: f-string 완전 정복 ─────────────────────────────────────────────

print("\nLEVEL 2: f-string 포맷 옵션")
print("-" * 40)

name  = "Alice"
age   = 30
score = 95.678
n     = 255

# 기본
print(f"이름: {name}, 나이: {age}")

# 표현식
print(f"내년 나이: {age + 1}")
print(f"이름 길이: {len(name)}")
print(f"대문자  : {name.upper()}")

# 숫자 포맷
print(f"\n숫자 포맷:")
print(f"  소수 2자리  : {score:.2f}")            # 95.68
print(f"  폭10 소수2  : {score:10.2f}")          # ____95.68
print(f"  천 단위 콤마: {1234567.89:,.2f}")       # 1,234,567.89
print(f"  부호 표시  : {score:+.1f}")            # +95.7
print(f"  0 패딩    : {42:05d}")                # 00042
print(f"  퍼센트    : {0.856:.1%}")              # 85.6%
print(f"  과학 표기  : {1.23e-4:.2e}")           # 1.23e-04

# 진수
print(f"\n진수 포맷:")
print(f"  10진: {n}")
print(f"  16진: {n:x}  또는  {n:#x}")            # ff / 0xff
print(f"  8진 : {n:o}  또는  {n:#o}")            # 377 / 0o377
print(f"  2진 : {n:b}  또는  {n:#b}")            # 11111111 / 0b11111111
print(f"  16진(8자리 패딩): {n:#010x}")           # 0x000000ff

# 정렬
print(f"\n정렬:")
print(f"|{'왼쪽':<15}|{'오른쪽':>15}|{'중앙':^15}|")
print(f"|{'left':<15}|{'right':>15}|{'center':^15}|")
print(f"|{'*'*15}|{'*'*15}|{'*'*15}|")

# 채우기 문자
print(f"|{'TITLE':=^30}|")   # =으로 채움
print(f"|{'INFO':-^30}|")    # -으로 채움

# Python 3.8+: = 디버깅 출력
x = 42
items = [1, 2, 3]
print(f"\n디버깅 출력 (=):")
print(f"  {x=}")             # x=42
print(f"  {items=}")         # items=[1, 2, 3]
print(f"  {len(items)=}")    # len(items)=3

# 중첩 f-string (동적 폭/정밀도)
width = 10
prec  = 3
print(f"\n중첩 f-string: {score:{width}.{prec}f}")  # ____95.678

# !r, !s, !a 변환 플래그
print(f"\n변환 플래그:")
text = "Hello\nWorld"
print(f"  !r : {text!r}")    # 'Hello\nWorld' (repr)
print(f"  !s : {text!s}")    # Hello\nWorld   (str — 이스케이프 해석)
print(f"  !a : {text!a}")    # 'Hello\nWorld' (ascii)

# ── LEVEL 2: 주요 str 메서드 ────────────────────────────────────────────────

print("\nLEVEL 2: 주요 str 메서드")
print("-" * 40)

s = "  Hello, Python World!  "

# 검색
print(f"find('Python')  : {s.find('Python')}")     # 9
print(f"index('Python') : {s.index('Python')}")    # 9
print(f"count('l')      : {s.count('l')}")         # 3
print(f"startswith('  '): {s.startswith('  ')}")   # True
print(f"endswith('!  ') : {s.endswith('!  ')}")    # True

# 변환
print(f"\nupper()   : {s.upper()}")
print(f"lower()   : {s.lower()}")
print(f"title()   : {s.title()}")
print(f"strip()   : |{s.strip()}|")
print(f"lstrip()  : |{s.lstrip()}|")
print(f"rstrip()  : |{s.rstrip()}|")
print(f"replace() : {s.replace('Python', 'Java')}")

# 분리/결합
words = s.strip().split()
print(f"\nsplit()      : {words}")
print(f"split(',')   : {s.strip().split(',')}")
csv = "a,b,c,d"
print(f"','.join([...]) : {'|'.join(csv.split(','))}")

# 판별
for test, method in [
    ("123",   str.isdigit),
    ("abc",   str.isalpha),
    ("abc123",str.isalnum),
    ("   ",   str.isspace),
    ("Title", str.istitle),
]:
    print(f"  {method.__name__}({test!r}) = {method(test)}")

# 패딩
print(f"\nzfill(8)   : {'42'.zfill(8)}")     # 00000042
print(f"center(20) : |{'HELLO'.center(20, '*')}|")
print(f"ljust(20)  : |{'left'.ljust(20, '-')}|")
print(f"rjust(20)  : |{'right'.rjust(20, '-')}|")

# ── LEVEL 3: 불변성과 메모리 ────────────────────────────────────────────────

print("\nLEVEL 3: str 불변성과 메모리")
print("-" * 40)

s = "hello"
print(f"id(s) before = {id(s)}")

# 수정 시도
try:
    s[0] = "H"    # TypeError!
except TypeError as e:
    print(f"s[0]='H' → TypeError: {e}")

# "수정"은 새 객체 생성
s = s.upper()   # 새 str 객체
print(f"id(s) after  = {id(s)}  (다른 주소)")

# ─── 문자열 연결 성능 비교 ───
import time

# 나쁜 방법: + 반복 (O(n²) — 매번 새 객체 생성)
def concat_bad(n):
    s = ""
    for i in range(n):
        s += str(i)    # 매번 새 str 객체 생성
    return s

# 좋은 방법: join (O(n))
def concat_good(n):
    parts = []
    for i in range(n):
        parts.append(str(i))
    return "".join(parts)    # 한 번에 연결

n = 5000
t1 = time.perf_counter(); concat_bad(n);  t1 = time.perf_counter() - t1
t2 = time.perf_counter(); concat_good(n); t2 = time.perf_counter() - t2
print(f"\n+  반복 ({n}회): {t1*1000:.3f}ms")
print(f"join ({n}회): {t2*1000:.3f}ms  ← 빠름")

# ── LEVEL 3: 유니코드와 인코딩 ──────────────────────────────────────────────

print("\nLEVEL 3: 유니코드와 인코딩")
print("-" * 40)

# Python 3의 str은 유니코드 (내부: UCS-1/UCS-2/UCS-4 동적 선택)
kor = "안녕하세요"
print(f"한국어 len    = {len(kor)}")        # 5 (문자 수)
print(f"UTF-8 bytes   = {len(kor.encode('utf-8'))} bytes")   # 15 bytes
print(f"UTF-16 bytes  = {len(kor.encode('utf-16'))} bytes")  # 12 bytes

# 코드포인트
print(f"\nord('A') = {ord('A')}")          # 65
print(f"ord('가') = {ord('가')}")          # 44032
print(f"chr(65)   = {chr(65)!r}")          # 'A'
print(f"chr(44032)= {chr(44032)!r}")       # '가'
print(f"chr(0x1F600)= {chr(0x1F600)!r}")  # '😀'

# 인코딩 → bytes
s = "Python 파이썬 🐍"
for enc in ["utf-8", "utf-16", "euc-kr"]:
    try:
        encoded = s.encode(enc)
        decoded = encoded.decode(enc)
        print(f"  {enc:<10}: {len(encoded)} bytes  |  round-trip OK: {s == decoded}")
    except (UnicodeEncodeError, LookupError) as e:
        print(f"  {enc:<10}: 오류 — {e}")

# BOM (Byte Order Mark)
utf8_bom = s.encode("utf-8-sig")
print(f"\nUTF-8 BOM: {utf8_bom[:3].hex()} 로 시작 (Excel 한글 호환)")

# ── LEVEL 4: 실무 패턴 ───────────────────────────────────────────────────────

print("\nLEVEL 4: 실무 패턴")
print("-" * 40)

# 패턴 1: 여러 줄 SQL / URL 조합
sql = (
    "SELECT u.id, u.name, o.total "
    "FROM users u "
    "JOIN orders o ON u.id = o.user_id "
    "WHERE u.active = 1 "
    "ORDER BY o.total DESC"
)
print(f"SQL: {sql[:60]}...")

# 패턴 2: 템플릿 문자열
from string import Template
t = Template("안녕하세요, $name님! 현재 $count개의 메시지가 있습니다.")
print(t.substitute(name="Alice", count=5))

# 패턴 3: 문자열 파싱 (split + strip)
csv_line = "  Alice , 30 , Seoul , developer  "
fields = [f.strip() for f in csv_line.split(",")]
print(f"파싱 결과: {fields}")

# 패턴 4: 정규식 활용
import re
text = "연락처: 010-1234-5678, 이메일: alice@example.com"
phone = re.search(r"\d{3}-\d{4}-\d{4}", text)
email = re.search(r"[\w.]+@[\w.]+\.[\w]+", text)
print(f"전화번호: {phone.group() if phone else 'N/A'}")
print(f"이메일  : {email.group() if email else 'N/A'}")

# 패턴 5: 다국어 처리
import unicodedata
chars = ["A", "가", "😀", "①", "Ⅰ"]
for ch in chars:
    print(f"  {ch!r}: {unicodedata.name(ch, 'UNKNOWN'):<30} 카테고리={unicodedata.category(ch)}")

# ── LEVEL 5: 오픈소스 패턴 ──────────────────────────────────────────────────

print("\nLEVEL 5: 오픈소스 패턴")
print("-" * 40)

# Django의 slugify 유사 구현
import unicodedata, re

def slugify(value):
    """Django slugify 단순화 버전"""
    # 유니코드 정규화 → ASCII 근사
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    # 소문자 변환
    value = value.lower()
    # 알파벳/숫자/하이픈/언더스코어 외 제거
    value = re.sub(r"[^\w\s-]", "", value)
    # 공백/하이픈을 하이픈으로 통일
    value = re.sub(r"[-\s]+", "-", value).strip("-_")
    return value

titles = ["Hello World", "Python 3.12 Release", "My  Blog Post!"]
for t in titles:
    print(f"  slugify({t!r}) = {slugify(t)!r}")

# ============================================================================
# [주의사항]
#   1. str += 반복은 O(n²) → 반드시 list + join 사용
#   2. 인코딩: encode() 기본값 utf-8, 한국어는 euc-kr도 고려
#   3. len("가") = 1 (문자수), len("가".encode()) = 3 (바이트수) 구분
#   4. f-string 안에 같은 따옴표 사용 불가 → !r, 바깥 따옴표 변경
#   5. str.format() 보다 f-string 권장 (가독성, 성능 모두 우위)
#
# [다음 단계]
#   → 009_input.py: 사용자 입력과 CLI 처리
# ============================================================================
