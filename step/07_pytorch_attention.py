import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import matplotlib


# 한글 폰트 설정 (환경에 따라 변경 필요)
# matplotlib.rcParams['font.family'] = 'AppleGothic'  # Mac
matplotlib.rcParams['font.family'] = 'Malgun Gothic'  # Windows


class CommitBot(nn.Module):
    def __init__(self):
        super().__init__()

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

        # 8차원 → 출력 단어 수만큼 점수
        self.fc = nn.Linear(8, len(self.tgt_vocab))

        self.criterion = nn.CrossEntropyLoss(ignore_index=0)
        self.optimizer = optim.Adam(self.parameters(), lr=0.05)

    def forward(self, src_ids):
        emb = self.embedding(src_ids)                               # (1, seq, 8)
        attn_out, attn_weights = self.attention(emb, emb, emb)     # self-attention
        logits = self.fc(attn_out)                                  # (1, seq, vocab)
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

        # loss = self.criterion(output.unsqueeze(0), target)
        # 손실 계산
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
            pred_ids = logits.argmax(dim=-1)
            pred_words = [self.tgt_itos[i.item()] for i in pred_ids[0]]
        return pred_words, attn_weights, src_words


def show_attention(attn_weights, src_words):
    attn = attn_weights[0].numpy()
    plt.figure(figsize=(4, 3))
    plt.imshow(attn, cmap='Blues', vmin=0, vmax=1)
    plt.xticks(range(len(src_words)), src_words)
    plt.yticks(range(len(src_words)), src_words)
    plt.xlabel('참조한 단어 (Key)')
    plt.ylabel('현재 단어 (Query)')
    plt.title('Self-Attention: 단어 간 관계')
    for i in range(len(src_words)):
        for j in range(len(src_words)):
            plt.text(j, i, f"{attn[i, j]:.2f}", ha='center', va='center', color='red')
    plt.colorbar()
    plt.tight_layout()
    plt.show()


# ---------- 학습 데이터 ----------
# [핵심] "수정"이 앞 단어에 따라 fix vs refactor로 달라지는 걸 학습
#   버그 수정   → bug fix
#   코드 수정   → code refactor  ← "수정"의 번역이 문맥에 따라 다름
#   리팩토링 코드 → refactor code
bot = CommitBot()

train_data = [
    (['버그', '수정'],      ['bug', 'fix']),
    (['코드', '수정'],      ['code', 'refactor']),
    (['리팩토링', '코드'],  ['refactor', 'code']),
]

def to_ids(bot, src_words, tgt_words):
    src_ids = torch.tensor([[bot.src_stoi[w] for w in src_words]])
    tgt_ids = torch.tensor([[bot.tgt_stoi[w] for w in tgt_words]])
    return src_ids, tgt_ids


# ---------- 학습 전 ----------
print("🧪 학습 전 예측:")
for src_words, _ in train_data:
    words, _, _ = bot.predict(src_words)
    print(f"  {src_words} → {words}")

# ---------- 학습 ----------
print("\n📚 300번 학습 시작...")
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

# ---------- Attention 시각화 ----------
# [핵심 확인] "코드 수정"에서 '수정'이 '코드'를 얼마나 참조했는지 확인
print("\n🔍 '코드 수정' Attention 시각화")
_, attn_weights, src_words = bot.predict(['코드', '수정'])
show_attention(attn_weights, src_words)