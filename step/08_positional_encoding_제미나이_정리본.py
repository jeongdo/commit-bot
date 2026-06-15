import torch
import torch.nn as nn
import torch.optim as optim
import math


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=100):
        super().__init__()
        # ----------------------------------------------------------------------
        # ★ 핵심: max_len(100)은 전체 단어 종류(8만 단어)와 아무런 상관이 없음!
        #         오직 "한 문장에 들어올 수 있는 최대 단어 개수(글자 수 제한 버퍼)"를 뜻함.
        #         100칸짜리 버퍼. 추후에 토큰 사이즈만 반환 되게 조절함.
        # ----------------------------------------------------------------------
        pe = torch.zeros(max_len, d_model)

        # 문장 내 단어들의 물리적 절대 위치 인덱스 배열 [[0], [1], [2], ..., [99]]
        # max_len=4
        # torch.arange(0, 4) : [0, 1, 2, 3]  # Shape: (4,)
        # .unsqueeze(1)
        #  [
        #   [0],
        #   [1],
        #   [2],
        #   [3]
        # ]  # Shape: (4, 1) -> 2차원 배열
        # 데이터를 바라보는 '해석용 돋보기(Metadata)'만 싹 바꿔서 "야, 이제부터 이거 가로로 읽지 말고, 원소 1개짜리 2차원 배열이 세로로 4층 쌓여있는 것처럼 해석해!"
        # 파이토치 진영에서는 이걸 '뷰(View)만 바꾼다, 자바로 치면 new float[4][1]
        position = torch.arange(0, max_len).unsqueeze(1)

        # 뒤쪽 차원(방)으로 갈수록 주파수를 감쇠시켜 값이 느리고 묵직하게 움직이도록 상수를 계산
        # 1단계: torch.arange(0, 8, 2)0부터 시작해서 8 직전까지 2씩 건너뛰며 배열을 만듭니다.결과: [0, 2, 4, 6] (원소 개수: 4개)
        # 2단계: 상숫값 곱하기 * (-math.log(10000.0) / 8)4개짜리 배열 [0, 2, 4, 6]의 각 원소에 어떤 고정된 실수(상수)를 각각 곱합니다.
        # 원소에 숫자를 곱한다고 해서 배열의 칸수가 늘어나진 않습니다.결과: [0.0, -2.3026, -4.6052, -6.9078] (원소 개수: 4개)
        # 3단계: torch.exp(...) 최종 탈출4개짜리 배열의 모든 원소에 지수 함수($e^x$)를 씌워줍니다. 역시 칸수는 그대로 유지됩니다.
        # 결과: [1.0, 0.1, 0.01, 0.001] (원소 개수: 4개)💡 결과: div_term 변수에 최종 저장되는 실물 텐서는 오직 4칸짜리 1차원 배열입니다.
        div_term = torch.exp(
            torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model)
        )

        # pe: [100, 8]짜리 전부 0으로 채워진 대형 도화지
        # position: [100, 1]짜리 세로 배열 ([[0], [1], [2], ..., [99]])

        # 괄호 안의 곱셈 연산 (position * div_term)
        # 여기서 아까 언급한 [100][1] 구조의 마법이 일어납니다.
        # 파이토치는 세로 배열 [100, 1]과 가로 배열 [4]를 곱하라는 명령을 받으면, 서로 부족한 차원을 알아서 잭나이프처럼 쫙 복사해서 확장(Broadcasting)시킵니다.
        # position은 가로로 4칸 복사되어 [100, 4]가 됩니다.div_term은 세로로 100칸 복사되어 [100, 4]가 됩니다.
        # 그리고 두 행렬이 1:1로 곱해져서 최종적으로 [100, 4] 짜리 2차원 배열이 탄생합니다.
        # 2번 인덱스 행(3번째 단어 자리)의 결과 예시:[2*1.0, 2*0.1, 2*0.01, 2*0.001] $\rightarrow$ [2.0, 0.2, 0.02, 0.002]

        # div_term: [4]짜리 가로 배열
        # [0번 인덱스] ([0.0, 0.0, 0.0, 0.0]) / [1번 인덱스] ([1.0, 0.1, 0.01, 0.001]) / [2번 인덱스] ([2.0, 0.2, 0.02, 0.002])

        # torch.sin([0.0, 0.0, 0.0, 0.0]) $\rightarrow$ [0.0, 0.0, 0.0, 0.0] (짝수 방으로 입장)
        # torch.cos([0.0, 0.0, 0.0, 0.0]) $\rightarrow$ [1.0, 1.0, 1.0, 1.0] (홀수 방으로 입장)

        # 최종 완성된 0번 행 (pe[0]):  > 짝수/홀수 지퍼를 채우면   [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0] 이라는 고유한 지문 좌표가 나옵니다.
        # 최종 완성된 0번 행 (pe[99]): > 짝수/홀수 지퍼를 채우면  [ -0.9992, 0.0398,  -0.4575, -0.8892,  0.8360, 0.5487,  0.0988, 0.9951 ]

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        # 배치를 고려해 (1, max_len, d_model) 구조로 레지스트리 승격 (1, 100, 8)
        # pe.unsqueeze(0) 실행 결과
        # [
        #   [  # ← unsqueeze(0)이 새로 만든 대괄호! (Batch 차원)
        #     [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0],  # 0번 단어 지문
        #     [0.84, 0.54, 0.09, 0.99, 0.01, 1.0, 0.0, 1.0],  # 1번 단어 지문
        #     ...
        #     [-0.99, 0.03, -0.45, -0.88, 0.83, 0.54, 0.09, 0.99]  # 99번 단어 지문
        #   ]
        # ]
        self.pe = pe.unsqueeze(0)

    def forward(self, x):
        # x.size(1): 파이프라인을 타고 들어온 현재 문장의 '실제 단어 개수' (예: ['버그', '수정'] 이면 2)
        # PyTorch 텐서의 shape 조회 방식
        # x.size(0) → 배치 개수
        # x.size(1) → 시퀀스 길이 (토큰 개수)
        # x.size(2) → 임베딩 차원
        seq_len = x.size(1)
        # ----------------------------------------------------------------------
        # [:seq_len](예: 2칸)으로 자르는 행위는, 메모리에서 2칸짜리 배열을 새로 만들어서 복사하는 게 아닙니다.
        # 기존에 이미 파놓은 100칸짜리 거대한 통짜 배열의 시작 주소부터 딱 2칸 변수만큼만 바라보도록 포인터만 지정(View)하는 방식입니다.
        # 컴퓨터 아키텍처 관점에서 새로운 메모리 할당(Allocation) 없이 주소값만 툭 던지는 연산이기 때문에 비용이 사실상 0에 가깝습니다.
        # 딱 현재 문장 길이만큼만 앞에서부터 칼로 잘라서([:seq_len] -> 2칸) 1:1로 더해줌.
        # ----------------------------------------------------------------------
        return x + self.pe[:, :seq_len, :]


class CommitBot(nn.Module):
    def __init__(self):
        super().__init__()

        # 문장 최대 길이 버퍼를 100칸으로 설정하여 위치 인코더 초기화
        self.pos_enc = PositionalEncoding(d_model=8, max_len=100)

        # [토크나이저 사전 정의] 고유 번호(ID)가 마스터 임베딩 테이블의 '행(Row) 인덱스' 주소가 됨
        self.src_vocab = ['<pad>', '버그', '수정', '코드', '리팩토링']
        self.src_stoi = {w: i for i, w in enumerate(self.src_vocab)}

        self.tgt_vocab = ['<pad>', 'bug', 'fix', 'code', 'refactor']
        self.tgt_stoi = {w: i for i, w in enumerate(self.tgt_vocab)}
        self.tgt_itos = {i: w for i, w in enumerate(self.tgt_vocab)}

        # ----------------------------------------------------------------------
        # ★ 핵심: 진짜 단어 총개수(Vocab Size)는 바로 여기서 통제함!
        #         만약 단어가 8만 개로 늘어나면 첫 번째 인자만 80000으로 바꾸면 됨. float[80000][8]
        # ----------------------------------------------------------------------
        self.embedding = nn.Embedding(len(self.src_vocab), 8, padding_idx=0)

        # 2개의 헤드로 쪼개어 복사본 배열들을 다각도로 융합하는 동적 연산 파이프라인
        self.attention = nn.MultiheadAttention(embed_dim=8, num_heads=2, batch_first=True)

        # 최종 8차원 문맥 복사본을 단어별 점수(5차원 float 배열)로 매핑하는 선형 결합 레이어, 점수판
        self.fc = nn.Linear(8, len(self.tgt_vocab))
        # 현재 토이 코드 (tgt_vocab = 5개일 때)
        # self.fc = nn.Linear(8, 5) # 출력 형식: [1, 2, 5] -> 입력 단어 2개 각각의 뒤에 5칸짜리 점수판이 붙음
        #
        # logits = [
        #   ['버그' 자리]: [ 0.1,  8.4, -2.1,  0.5, -4.2 ], # 5칸
        #   ['수정' 자리]: [ -1.5, -0.2,  9.2,  1.1,  0.0 ]  # 5칸
        # ]

        # 실제 실무 모델 (tgt_vocab = 80,000개일 때)
        # self.fc = nn.Linear(8, 80000) # 출력 형식: [1, 2, 80000] -> 입력 단어 2개 각각의 뒤에 8만 칸짜리 대형 점수판이 붙음
        #
        # logits = [
        #   ['버그' 자리]: [ 0.1, -1.2, ..., 7.9, ..., -3.4 ], # 총 80,000칸!
        #   ['수정' 자리]: [ -2.5, 0.4, ..., 0.1, ...,  9.4 ]  # 총 80,000칸!
        # ]

        # [🗺️ 이해자료]

        # 시나리오 1: 공유 단어장 (Shared Vocabulary) → GPT 스타일
        # 유저님이 생각하신 "입구가 8만 개면 출력도 무조건 8만 개여야지!"가 100% 그대로 적용되는 구조입니다.
        #
        # 요즘 나오는 GPT, LLaMA 같은 대형 언어 모델들은 입력과 출력을 굳이 나누지 않고, 하나의 통합된 8만 칸짜리 마스터 단어장을 입구와 출구에서 같이 돌려씁니다.
        #
        # 입구 (Embedding): nn.Embedding(80000, 512) -> 8만 개 단어 중 하나를 짚어서 들어옴
        #
        # 출구 (Linear): nn.Linear(512, 80000) -> 8만 개 단어 전체에 대한 점수판을 깔아줌
        #
        # 이 구조에서는 입구와 출구가 정확히 80,000이라는 숫자로 대칭을 이룹니다. 자바로 치면 입력 ID와 출력 ID가 같은 Enum 클래스나 동일한 마스터 테이블의 PK를 바라보는 형태죠.

        # 시나리오 2: 독립 단어장 (Separate Vocabulary) → 번역기 스타일
        # 하지만 구글 번역기처럼 "한국어를 입력받아서 영어로 출력"하는 구조라면 얘기가 살짝 달라집니다. 이때는 입구와 출구의 단어 개수가 완전히 똑같지 않을 수 있습니다.
        #
        # 데이터 전처리 단계에서 DISTINCT를 때릴 때, 한국어 데이터셋과 영어 데이터셋을 각각 따로 때리기 때문입니다.
        #
        # 입력 데이터 (한국어 셋): 중복 제거했더니 유니크한 단어가 80,000개 나옴
        #
        # 출력 데이터 (영어 셋): 중복 제거했더니 유니크한 단어가 60,000개 나옴
        #
        # 이럴 경우, 아키텍처는 아래와 같이 수치 불균형이 일어난 채로 설계됩니다.
        #
        # 입구: 한국어 8만
        # self.embedding = nn.Embedding(80000, 8)
        #
        # # ... 중간 연산 (어텐션 등) ...
        #
        # # 출구: 최종 점수는 영어 단어장 크기(6만 개)에 맞춰서 점수판을 짜야 함
        # self.fc = nn.Linear(8, 60000)
        # 이때는 출구가 80,000이 아니라 60,000이 됩니다. 왜냐하면 최종 목적지가 영어 단어(bug, fix 등)의 세상이기 때문에, 굳이 한국어 단어 방들에다가 점수를 줄 필요가 없기 때문입니다.

        # CrossEntropyLoss가 (N, C) 형태만 받아서 펴주는 것
        # CrossEntropyLoss가 하는 일:
        # 1. output 점수들을 확률로 변환 (softmax)
        # 2. 정답 위치(1번)의 확률이 높을수록 loss는 작아짐
        #    - 정답 확률 0.7 → loss 0.35 (작음)
        #    - 정답 확률 0.9 → loss 0.10 (더 작음)
        #    - 정답 확률 0.3 → loss 1.20 (큼)

        self.criterion = nn.CrossEntropyLoss(ignore_index=0)
        self.optimizer = optim.Adam(self.parameters(), lr=0.05)

        # 손실함수와 옵티마이저
        self.criterion = nn.CrossEntropyLoss()  # 정답과 비교해서 오차 계산, 처음에 당연히 틀림.
        self.optimizer = optim.SGD(self.parameters(), lr=0.1)

        # SGD : 확률적 경사하강법(간단하고 빠른 업데이트 방식)
        # self.parameters() : 기본적으로 존재하고 있는 값 또는 범위: 10개 (bias) + (6*10의 연결강도 : 모든 경우의 수의 인식 + 그 상태값 증감함)

        # lr = 0.01(작은 걸음) → 천천히, 안정적으로 감 → 오래 걸림, but 잘감
        # lr = 0.9(큰 걸음)→ 빨리 감 → 근데 절벽으로 뛰어내릴 수도 있음(발산)

    def forward(self, src_ids):
        # READ (Copy-by-Value): 마스터 DB 테이블 행 주소에서 8칸짜리 float 값을 복사해옴
        emb = self.embedding(src_ids)

        # 100칸짜리 번호표 판에서 현재 문장 길이만큼만 슬라이싱해서 덧셈 집행
        emb = self.pos_enc(emb)

        # 동적 연산: 복사해온 로컬 변수들을 Q, K, V로 통과시켜 주변 단어들의 문맥을 융합
        attn_out, attn_weights = self.attention(emb, emb, emb)

        # OUTPUT: 최종 예측 점수(Logits) 도출 (이 시점까지 마스터 DB 원본은 완전 읽기전용 상태)
        logits = self.fc(attn_out)
        return logits, attn_weights

    def train_step(self, src_ids, tgt_ids):
        self.train()

        # 순전파: 복사본들로 연산하여 최종 의견(logits) 도출
        logits, _ = self.forward(src_ids)

        # [1단계: 채점] 복사본 연산 결과물과 정답을 대조하여 오차(Loss) 로그 발행
        loss = self.criterion(logits.view(-1, len(self.tgt_vocab)), tgt_ids.view(-1))

        # [2단계: 클린] 직전 트랜잭션에서 누적되었던 기울기 메모리 캐시 비우기
        self.optimizer.zero_grad()

        # [3단계: 역전파 미분] 오차를 기반으로 파이프라인을 역주행하며 각 파라미터 방의 기울기(Gradient) 계산
        loss.backward()

        # [4단계: 미세조정 UPDATE] 마스터 가중치 테이블 원본의 float 값들을 기울기 수치만큼 미세하게 보정하여 저장
        self.optimizer.step()

        return loss.item()

    def predict(self, src_words):
        self.eval()
        src_ids = torch.tensor([[self.src_stoi[w] for w in src_words]])
        with torch.no_grad():
            logits, attn_weights = self.forward(src_ids)
            pred_ids = logits.argmax(dim=-1)
            pred_words = [self.tgt_itos[i.item()] for i in pred_ids[0]]
        return pred_words, attn_weights, src_words


# ---------- 데이터 로드 및 빌드 런타임 ----------
bot = CommitBot()

train_data = [
    (['버그', '수정'], ['bug', 'fix']),
    (['코드', '수정'], ['code', 'refactor']),
    (['리팩토링', '코드'], ['refactor', 'code']),
]

print("🧪 학습 전 예측:")
for src_words, _ in train_data:
    words, _, _ = bot.predict(src_words)
    print(f"  {src_words} → {words}")

print("\n📚 300번 학습 시작...")


def to_ids(bot, src_words, tgt_words):
    src_list = []
    for w in src_words:
        src_list.append(bot.src_stoi[w])
    src_ids = torch.tensor([src_list])

    tgt_list = []
    for w in tgt_words:
        tgt_list.append(bot.tgt_stoi[w])
    tgt_ids = torch.tensor([tgt_list])

    return src_ids, tgt_ids


for epoch in range(300):
    total_loss = 0
    for src_words, tgt_words in train_data:
        src_ids, tgt_ids = to_ids(bot, src_words, tgt_words)
        total_loss += bot.train_step(src_ids, tgt_ids)
    if epoch % 60 == 0:
        print(f"  Epoch {epoch:3d} | Loss: {total_loss:.4f}")

print("\n✅ 학습 후 예측:")
for src_words, tgt_words in train_data:
    words, attn_weights, _ = bot.predict(src_words)
    correct = words == tgt_words
    print(f"  {src_words} → {words}  {'✅' if correct else '❌'} (정답: {tgt_words})")
