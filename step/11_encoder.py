"""
08. Encoder 분리
=================
[이전 07과 달라진 점]
  - CommitBot.forward() 안에 섞여 있던 Embedding + PosEnc + Attention을
    Encoder 클래스로 분리
  - 동작 결과는 07과 완전히 동일
  - fc()는 Encoder가 아니라서 CommitBot에 남겨둠

[Encoder의 역할]
  입력 문장("버그 수정")을 받아서
  각 단어가 문맥을 반영한 벡터로 바뀐 memory를 출력

  "버그" → [0.3, -0.1, ...] (단순 단어 벡터)
       ↓  Self-Attention ("수정" 앞에 "버그"가 있다는 문맥 반영)
  "버그" → [0.7,  0.2, ...] (문맥이 담긴 벡터) ← memory
"""

import torch
import torch.nn as nn
import torch.optim as optim
import math


# ================================================================
# Positional Encoding (07과 동일)
# ================================================================
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=100):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.pe = pe.unsqueeze(0)

    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]


# ================================================================
# [신규] Encoder 클래스
# ================================================================
# 07에서 CommitBot.forward() 안에 흩어져 있던 코드를 여기로 모음
# Encoder가 하는 일:
#   1. 단어 인덱스 → 벡터 (Embedding)
#   2. 위치 정보 추가 (Positional Encoding)
#   3. 문맥 반영 (Self-Attention)
#   → 출력: memory (batch, seq_len, d_model)
#
# memory란?
#   각 단어가 "주변 단어를 참고한 뒤" 업데이트된 벡터
#   이걸 나중에 Decoder가 참고해서 번역함
class Encoder(nn.Module):
    def __init__(self, vocab_size, d_model=8, nhead=2):
        super().__init__()
        # 07의 self.embedding과 동일
        self.embedding = nn.Embedding(vocab_size, d_model, padding_idx=0)
        # 07의 self.pos_enc와 동일
        self.pos_enc = PositionalEncoding(d_model)
        # 07의 self.attention과 동일
        self.self_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)

    def forward(self, src_ids):
        # src_ids: (batch, src_len)  예) tensor([[1, 2]])  = [버그, 수정]

        # 1. 단어 인덱스 → 벡터
        emb = self.embedding(src_ids)       # (batch, src_len, d_model)

        # 2. 위치 정보 추가
        emb = self.pos_enc(emb)             # (batch, src_len, d_model)

        # 3. Self-Attention: 각 단어가 같은 문장 내 다른 단어를 참조
        #    Q=K=V=emb (자기 자신을 참조하므로 Self-Attention)
        memory, _ = self.self_attn(emb, emb, emb)  # (batch, src_len, d_model)

        # memory: 문맥이 담긴 벡터
        # 다음 단계(Decoder)에서 이 memory를 참고해서 번역함
        return memory


# ================================================================
# CommitBot (07에서 Encoder 부분만 분리됨)
# ================================================================
class CommitBot(nn.Module):
    def __init__(self):
        super().__init__()

        self.src_vocab = ['<pad>', '버그', '수정', '코드', '리팩토링']
        self.src_stoi  = {w: i for i, w in enumerate(self.src_vocab)}

        self.tgt_vocab = ['<pad>', 'bug', 'fix', 'code', 'refactor']
        self.tgt_stoi  = {w: i for i, w in enumerate(self.tgt_vocab)}
        self.tgt_itos  = {i: w for i, w in enumerate(self.tgt_vocab)}

        # [변경] 07에서 CommitBot 안에 있던 embedding, pos_enc, attention
        #        → Encoder 클래스로 분리
        self.encoder = Encoder(len(self.src_vocab), d_model=8, nhead=2)

        # fc는 Encoder의 역할이 아니라 "분류기"라서 CommitBot에 남김
        # (다음 단계에서 Decoder로 교체될 예정)
        self.fc = nn.Linear(8, len(self.tgt_vocab))

        self.criterion = nn.CrossEntropyLoss(ignore_index=0)
        self.optimizer = optim.Adam(self.parameters(), lr=0.05)

    def forward(self, src_ids):
        # 07: emb = embedding → pos_enc → attention  (CommitBot 안에서 직접)
        # 08: Encoder 클래스에 위임 → memory 받아옴
        memory = self.encoder(src_ids)      # (batch, src_len, d_model)

        # memory를 fc에 넣어 각 단어별 후보 점수 계산
        # (다음 단계에서 fc 대신 Decoder가 들어올 자리)
        logits = self.fc(memory)            # (batch, src_len, tgt_vocab_size)
        return logits

    def train_step(self, src_ids, tgt_ids):
        self.train()
        logits = self.forward(src_ids)
        loss = self.criterion(
            logits.view(-1, len(self.tgt_vocab)),
            tgt_ids.view(-1)
        )
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def predict(self, src_words):
        self.eval()
        src_ids = torch.tensor([[self.src_stoi[w] for w in src_words]])
        with torch.no_grad():
            logits = self.forward(src_ids)
            pred_ids   = logits.argmax(dim=-1)
            pred_words = [self.tgt_itos[i.item()] for i in pred_ids[0]]
        return pred_words


# ================================================================
# 실행
# ================================================================
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

print("🧪 학습 전:")
for src_words, _ in train_data:
    print(f"  {src_words} → {bot.predict(src_words)}")

print("\n📚 300 에폭 학습...")
for epoch in range(300):
    total_loss = 0
    for src_words, tgt_words in train_data:
        src_ids, tgt_ids = to_ids(bot, src_words, tgt_words)
        total_loss += bot.train_step(src_ids, tgt_ids)
    if epoch % 60 == 0:
        print(f"  Epoch {epoch:3d} | Loss: {total_loss:.4f}")

print("\n✅ 학습 후:")
for src_words, tgt_words in train_data:
    pred = bot.predict(src_words)
    correct = pred == tgt_words
    print(f"  {src_words} → {pred}  {'✅' if correct else '❌'} (정답: {tgt_words})")

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[08 핵심 정리]
  07과 동작은 완전히 동일
  달라진 건 구조뿐:

  07: CommitBot.forward()
        embedding → pos_enc → attention → fc

  08: CommitBot.forward()
        Encoder (embedding + pos_enc + attention)
          → memory
        fc(memory)
          → logits

  다음 단계(09):
    fc() 자리에 Decoder가 들어옴
    Decoder는 memory를 참고해서
    단어를 하나씩 순서대로 생성함
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")