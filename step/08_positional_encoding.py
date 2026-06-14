import torch
import torch.nn as nn
import torch.optim as optim
import math


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=100):
        super().__init__()
        # ------------------------------------------------
        # 1. pe: 위치 인코딩을 저장할 빈 행렬 생성
        #    shape: (max_len, d_model) = (최대 문장 길이, 임베딩 차원)
        #    여기에 미리 계산한 위치 신호를 채워넣을 예정
        # ------------------------------------------------
        pe = torch.zeros(max_len, d_model)

        # ------------------------------------------------
        # 2. position: 문장 내 각 단어의 위치 번호
        #    torch.arange(0, max_len) → [0, 1, 2, ..., max_len-1]
        #    .unsqueeze(1) → 열 벡터로 변환: shape (max_len, 1)
        #    예) max_len=4 → [[0],[1],[2],[3]]
        # ------------------------------------------------
        position = torch.arange(0, max_len).unsqueeze(1)

        # ------------------------------------------------
        # 3. div_term: 위치에 곱해질 주파수 역수(파장)
        #    torch.arange(0, d_model, 2) → [0, 2, 4, ...] (짝수 인덱스)
        #    (-math.log(10000.0) / d_model) = 음수 상수
        #    exp()를 씌워서 주파수 감쇠 상수를 만듦
        #    결과 shape: (d_model/2,)
        #    이 값들은 차원이 커질수록 작아져서
        #    → 높은 차원에서는 느리게, 낮은 차원에서는 빠르게 진동하는 sin/cos 주파수 결정
        # ------------------------------------------------
        div_term = torch.exp(
            torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model)
        )

        # ------------------------------------------------
        # 4. 짝수 차원(0,2,4,...) → sin 함수로 채움
        #    position * div_term: (max_len,1) * (1, d_model/2) → (max_len, d_model/2)
        #    sin() 적용 후 pe의 짝수 열에 할당
        # ------------------------------------------------
        pe[:, 0::2] = torch.sin(position * div_term)

        # ------------------------------------------------
        # 5. 홀수 차원(1,3,5,...) → cos 함수로 채움
        #    같은 position * div_term 사용, cos 적용
        # ------------------------------------------------
        pe[:, 1::2] = torch.cos(position * div_term)

        # ------------------------------------------------
        # 6. 배치 차원 추가
        #    pe shape: (max_len, d_model) → unsqueeze(0) → (1, max_len, d_model)
        #    이렇게 하면 forward()에서 x (batch, seq_len, d_model)과
        #    바로 broadcasting 덧셈이 가능해짐
        # ------------------------------------------------
        self.pe = pe.unsqueeze(0)

    def forward(self, x):
        # x: (batch, seq_len, d_model)
        seq_len = x.size(1)
        # self.pe[:, :seq_len, :]  → (1, seq_len, d_model)
        # x + ...  → batch 방향으로 알아서 broadcasting
        return x + self.pe[:, :seq_len, :]


class CommitBot(nn.Module):
    def __init__(self):
        super().__init__()

        self.pos_enc = PositionalEncoding(d_model=8)  # Positional Encoding 초기화

        # 입력 단어 (한글)
        self.src_vocab = ['<pad>', '버그', '수정', '코드', '리팩토링']
        self.src_stoi = {w: i for i, w in enumerate(self.src_vocab)}

        # 출력 단어 (영어)
        self.tgt_vocab = ['<pad>', 'bug', 'fix', 'code', 'refactor']
        self.tgt_stoi = {w: i for i, w in enumerate(self.tgt_vocab)}
        self.tgt_itos = {i: w for i, w in enumerate(self.tgt_vocab)}

        # [06과 동일] 단어 → 8차원 밀집 벡터
        self.embedding = nn.Embedding(len(self.src_vocab), 8, padding_idx=0)

        # [핵심 추가] Self-Attention: 단어들이 서로를 참조해 문맥 반영
        # "수정" 앞에 "버그"가 있으면 → fix
        # "수정" 앞에 "코드"가 있으면 → refactor
        self.attention = nn.MultiheadAttention(embed_dim=8, num_heads=2, batch_first=True)

        # embed_dim=8은 전체 임베딩 차원입니다. 단어 하나가 8차원 벡터로 표현되죠.
        # num_heads=2 "왜 되는지 모르는데 그냥 씀" 이 AI 전체의 분위기거든.

        # 8차원 → 출력 단어 수만큼 점수
        self.fc = nn.Linear(8, len(self.tgt_vocab))

        self.criterion = nn.CrossEntropyLoss(ignore_index=0)
        self.optimizer = optim.Adam(self.parameters(), lr=0.05)

    def forward(self, src_ids):
        # src_ids = tensor([[1, 2]])   # [버그(1), 수정(2)] 인덱스
        # 인덱스 → 벡터로 변환
        emb = self.embedding(src_ids)

        emb = self.pos_enc(emb)  # # Positional Encoding 위치 정보 더하기

        # tensor([[[0.3, -0.1, 0.8, ...],   ← 버그의 8차원 벡터
        #          [0.1,  0.5, 0.2, ...]]])  ← 수정의 8차원 벡터

        # shape: (1, 2, 8)  = (배치(문장이 1개), 단어수 2개 (버그, 수정), 차원 (단어하나가 8차원 벡터))
        # [                        # 배치 1개
        #   [                      # 문장
        #     [0.3, -0.1, 0.8, 0.2, 0.5, -0.3, 0.1, 0.7],   # 버그 (8차원)
        #     [0.1,  0.5, 0.2, 0.9, 0.3,  0.4, 0.6, 0.2],   # 수정 (8차원)
        #   ]
        # ]

        # 학습할 때 문장 여러 개를 한 번에 넣을 수 있어
        # 배치 1  →  (1, 2, 8)   문장 1개
        # 배치 32 →  (32, 2, 8)  문장 32개 동시에

        attn_out, attn_weights = self.attention(emb, emb, emb)  # # Q, K, V

        # Q (Query) → "나는 뭘 찾고 있나?" (수정이 묻는다)
        # K (Key) → "나는 어떤 단어야?" (버그, 코드 가 대답)
        # V (Value) → "참조 비중 결정되면 실제로 가져올 정보"

        logits = self.fc(attn_out)  # (1, seq, vocab)
        return logits, attn_weights

    def train_step(self, src_ids, tgt_ids):
        # 모델을 학습 모드로 전환 (Dropout, BatchNorm 등이 학습용으로 활성화)
        # predict()에서 self.eval()로 끈 걸 다시 켜는 것
        # self.train()  →  학습할 때
        # self.eval()   →  예측할 때 (predict)
        self.train()

        # 순전파: 입력 → 모델 통과 → 예측 점수 반환
        # logits shape: (1, 2, 5) = (배치, 단어수, 후보수)
        # _ 는 attn_weights인데 학습에 안 쓰니까 버림
        logits, _ = self.forward(src_ids)

        # CrossEntropyLoss가 (N, C) 형태만 받아서 펴주는 것
        # CrossEntropyLoss가 하는 일:
        # 1. output 점수들을 확률로 변환 (softmax)
        # 2. 정답 위치(1번)의 확률이 높을수록 loss는 작아짐
        #    - 정답 확률 0.7 → loss 0.35 (작음)
        #    - 정답 확률 0.9 → loss 0.10 (더 작음)
        #    - 정답 확률 0.3 → loss 1.20 (큼)

        # 05. loss = self.criterion(output.unsqueeze(0), target)
        # output = self.fc(inp)        # shape: (10,)   1차원
        # output.unsqueeze(0)          # shape: (1, 10) 2차원으로 승격,  배치 차원 추가

        # N=1 (문장 or 입력 1개), C=10 (후보 10개)

        # 07  단어 2개 → 3차원을 2차원으로 펴야 함
        # logits.view(-1, len(self.tgt_vocab))        # (1, 2, 5) → (2, 5), 입력 2개, 후보 5개
        # tgt_ids.view(-1)                            # (1, 2)    → (2,),   정답 2개

        # 배치 2  →  문장 2개 동시에
        #
        # logits shape: (2, 2, 5)  = (배치2, 단어2개, 후보5개)
        # tgt_ids shape: (2, 2)    = (배치2, 단어2개)
        #
        # view(-1, 5) → (4, 5)    2문장 × 2단어 = 4개 펼쳐짐
        # view(-1)    → (4,)       정답도 4개
        # -1 이 알아서 계산하는 거니까:
        # 배치 1  →  (1, 2, 5) → view(-1, 5) → (2, 5)   1×2=2
        # 배치 2  →  (2, 2, 5) → view(-1, 5) → (4, 5)   2×2=4
        # 배치 4  →  (4, 2, 5) → view(-1, 5) → (8, 5)   4×2=8
        # 배치가 바뀌어도 view(-1, 5) 코드는 그대로야. -1 이 배치 × 단어수를 자동 계산해주니까. 그게 -1 쓰는 이유

        # (1, 2, 5)
        #  ↑
        # 문장 몇 개를 한 번에 넣었냐
        #
        # 지금은 ["버그", "수정"] 1문장만 넣으니까 1

        # 배치가 왜 있냐면:
        # 배치 1  →  (1, 2, 5)   문장 1개씩 학습
        # 배치 4  →  (4, 2, 5)   문장 4개 동시에 학습
        # 배치 32 →  (32, 2, 5)  문장 32개 동시에 학습

        # 실제 대형 모델은 배치 32~512씩 넣어서 한 번에 학습해. 속도가 훨씬 빠르거든.
        # 07.py는 문장 1개씩 넣으니까 항상 1이고, 그래서 view(-1)로 그 1을 날려버리는 거야.
        # (1, 2, 5) → view(-1, 5) → (2, 5)   배치 1 사라짐
        # (1, 2)    → view(-1)    → (2,)     배치 1 사라짐

        # 배치 2  →  문장 2개 동시에 입력
        #
        # src_ids = tensor([[1, 2],    # 문장1: [버그, 수정]
        #                   [3, 2]])   # 문장2: [코드, 수정]
        # # shape: (2, 2)  = (배치2, 단어2개)
        # 그러면 logits는:
        # (2, 2, 5)
        #  ↑
        #  배치 2
        #
        # view(-1, 5) → (4, 5)   2문장 × 2단어 = 4개 펼쳐짐

        # 배치 1   →  문장 1개 보고 바로 업데이트
        #            방향이 정확한데 자주 흔들림 (지그재그, 느림)
        #
        # 배치 2   →  문장 2개 평균 내서 업데이트
        #            방향이 더 안정적, 업데이트 횟수 절반 (개별 특성 뭉개짐)
        #
        # 배치 32  →  32개 평균
        #            매우 안정적, GPU 병렬처리로 속도 빠름 (절충점, 실험으로 찾는 것)

        # logits.view(-1, 5) : (1, 2, 5) → (2, 5)  단어별 후보 점수
        # tgt_ids.view(-1)   : (1, 2)    → (2,)    단어별 정답 인덱스
        loss = self.criterion(logits.view(-1, len(self.tgt_vocab)), tgt_ids.view(-1))

        # 이전 step()에서 누적된 기울기 초기화
        # 안 하면 이전 학습 기울기가 더해져서 엉뚱한 방향으로 업데이트됨
        self.optimizer.zero_grad()

        # 역전파: loss 기준으로 모든 파라미터의 기울기 자동 계산
        # embedding, W_Q, W_K, W_V, fc 전부 기울기 계산됨
        loss.backward()

        # 계산된 기울기로 파라미터 업데이트
        # learning_rate 만큼 정답 방향으로 이동
        self.optimizer.step()

        # loss 값을 Python float으로 반환 (tensor → 숫자)
        # .item() 없으면 tensor 객체가 반환되어 출력/비교 불편
        return loss.item()

    def predict(self, src_words):
        self.eval()
        src_ids = torch.tensor([[self.src_stoi[w] for w in src_words]])
        with torch.no_grad():
            logits, attn_weights = self.forward(src_ids)

            # 05.py
            # predicted_idx = torch.argmax(output).item() # 가장 높은 점수 인덱스 1개
            # predicted_word = self.candidates[predicted_idx] # 인덱스 → 단어 1개

            # 05, 06   단어 1개 입력 → 정답 1개
            #   "추가" → "insert"
            #
            # 07       문장 전체 입력 → 정답 2개
            #   ["버그", "수정"] → ["bug", "fix"]

            # # 07  문장 전체 한 번에 처리
            # logits = self.fc(attn_out)                   # shape: (1, 2, 5)  단어 2개 × 후보 5개
            # pred_ids = logits.argmax(dim=-1)             # shape: (1, 2)     단어 2개의 정답 인덱스,  (정답: ['bug', 'fix'])
            # pred_words = [self.tgt_itos[i.item()] for i in pred_ids[0]]  # 인덱스 2개 → 단어 2개

            pred_ids = logits.argmax(dim=-1)
            pred_words = [self.tgt_itos[i.item()] for i in pred_ids[0]]
        return pred_words, attn_weights, src_words


bot = CommitBot()

train_data = [
    (['버그', '수정'], ['bug', 'fix']),
    (['코드', '수정'], ['code', 'refactor']),
    (['리팩토링', '코드'], ['refactor', 'code']),
]

# ---------- 학습 전 ----------
print("🧪 학습 전 예측:")
for src_words, _ in train_data:
    words, _, _ = bot.predict(src_words)
    print(f"  {src_words} → {words}")

# ---------- 학습 ----------
print("\n📚 300번 학습 시작...")


# def to_ids(bot, src_words, tgt_words):
#     src_ids = torch.tensor([[bot.src_stoi[w] for w in src_words]])
#     tgt_ids = torch.tensor([[bot.tgt_stoi[w] for w in tgt_words]])
#     return src_ids, tgt_ids

def to_ids(bot, src_words, tgt_words):
    src_list = []
    for w in src_words:
        src_list.append(bot.src_stoi[w])  # ["버그", "수정"] → [1, 2]
    src_ids = torch.tensor([src_list])  # [1, 2] → tensor([[1, 2]])

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

# ---------- 학습 후 ----------
print("\n✅ 학습 후 예측:")
for src_words, tgt_words in train_data:
    words, attn_weights, _ = bot.predict(src_words)
    correct = words == tgt_words
    print(f"  {src_words} → {words}  {'✅' if correct else '❌'} (정답: {tgt_words})")
