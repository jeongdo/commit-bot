"""
09. Decoder 추가 (Decoder + Cross-Attention 연결)
=================
[08과 달라진 점]
  - Decoder 클래스 신규 추가
  - fc()가 CommitBot에서 Decoder 안으로 이동
  - 번역 방식 변경:
      08: 입력 단어 수만큼 바로 출력  (["버그","수정"] → ["bug","fix"] 한번에)
      09: <s>부터 시작해서 단어를 하나씩 순서대로 생성

[Decoder 내부 구조]
  ① Self-Attention  : 지금까지 생성한 출력 단어끼리 참조
  ② Cross-Attention : Encoder의 memory를 참조  ← 핵심
  ③ fc              : 다음 단어 후보 점수 계산

[Cross-Attention이란?]
  Encoder:  "버그 수정" → memory (한글 문맥이 담긴 벡터)
  Decoder:  <s> 다음에 뭐가 올지 모름
            → memory를 참조(Cross-Attention)해서 "fix"를 선택
            → "fix" 다음엔? 또 memory 참조해서 "bug" 선택

  Q = 디코더가 지금까지 생성한 단어  ("나는 뭘 만들어야 하지?")
  K = Encoder memory                  ("한글 문맥 키워드들")
  V = Encoder memory                  ("실제로 가져올 정보")
"""

import torch
import torch.nn as nn
import torch.optim as optim
import math


# ================================================================
# Positional Encoding (08과 동일)
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
# Encoder (08과 동일)
# ================================================================
class Encoder(nn.Module):
    def __init__(self, vocab_size, d_model=8, nhead=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.pos_enc   = PositionalEncoding(d_model)
        self.self_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)

    def forward(self, src_ids):
        emb = self.embedding(src_ids)
        emb = self.pos_enc(emb)
        memory, _ = self.self_attn(emb, emb, emb)
        return memory  # (batch, src_len, d_model)


# ================================================================
# [신규] Decoder 클래스
# ================================================================
class Decoder(nn.Module):
    def __init__(self, vocab_size, d_model=8, nhead=2):
        super().__init__()

        # 출력 단어도 벡터로 변환 필요 (Encoder의 embedding과 별도)
        # Encoder: 한글 단어 → 벡터
        # Decoder: 영어 단어 → 벡터
        self.embedding = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.pos_enc   = PositionalEncoding(d_model)

        # ① Self-Attention
        # 지금까지 생성한 출력 단어끼리 참조
        # 예) "fix"를 생성한 뒤 → "fix"를 참고해서 다음 단어 결정
        # 단, 미래 단어는 보면 안 됨 → causal_mask로 차단
        self.self_attn  = nn.MultiheadAttention(d_model, nhead, batch_first=True)

        # ② Cross-Attention  ← Decoder에만 있는 핵심
        # Q: 디코더 현재 상태  (내가 지금 어디까지 생성했지?)
        # K: Encoder memory   (한글 문맥의 키워드)
        # V: Encoder memory   (실제로 가져올 정보)
        self.cross_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)

        # ③ fc: 최종 단어 후보 점수
        # 08에서 CommitBot에 있던 fc가 여기로 이동
        self.fc = nn.Linear(d_model, vocab_size)

    def forward(self, tgt_ids, memory):
        # tgt_ids: 지금까지 생성한 출력 토큰  예) [<s>] 또는 [<s>, fix]
        # memory : Encoder 출력              예) 버그/수정의 문맥 벡터

        # 출력 단어도 벡터로 변환
        emb = self.embedding(tgt_ids)   # (batch, tgt_len, d_model)
        emb = self.pos_enc(emb)

        # ① Self-Attention + causal_mask
        # causal_mask: 미래 단어 차단
        # 예) tgt_len=3일 때
        #   [[0,   -inf, -inf],   0번은 0번만 봄
        #    [0,    0,   -inf],   1번은 0~1번 봄
        #    [0,    0,    0  ]]   2번은 0~2번 봄
        tgt_len = tgt_ids.size(1)
        causal_mask = torch.triu(
            torch.full((tgt_len, tgt_len), float('-inf')), diagonal=1
        )
        self_out, _ = self.self_attn(emb, emb, emb, attn_mask=causal_mask)

        # ② Cross-Attention
        # Q=self_out (디코더 현재), K=V=memory (Encoder 출력)
        # "내가 지금 <s>fix까지 생성했는데, 한글 문맥 보고 다음 단어 뭐야?"
        cross_out, _ = self.cross_attn(self_out, memory, memory)

        # ③ 다음 단어 후보 점수
        logits = self.fc(cross_out)     # (batch, tgt_len, tgt_vocab_size)
        return logits


# ================================================================
# CommitBot
# ================================================================
class CommitBot(nn.Module):
    def __init__(self):
        super().__init__()

        self.src_vocab = ['<pad>', '버그', '수정', '코드', '리팩토링']
        self.src_stoi  = {w: i for i, w in enumerate(self.src_vocab)}

        # <s> = 시작 토큰, <eos> = 종료 토큰 추가
        # Decoder는 <s>부터 시작해서 <eos>가 나올 때까지 생성
        self.tgt_vocab = ['<pad>', '<s>', '<eos>', 'bug', 'fix', 'code', 'refactor']
        self.tgt_stoi  = {w: i for i, w in enumerate(self.tgt_vocab)}
        self.tgt_itos  = {i: w for i, w in enumerate(self.tgt_vocab)}

        self.encoder = Encoder(len(self.src_vocab), d_model=8, nhead=2)

        # [변경] 08의 fc() → Decoder 안으로 이동
        self.decoder = Decoder(len(self.tgt_vocab), d_model=8, nhead=2)

        self.criterion = nn.CrossEntropyLoss(ignore_index=0)
        self.optimizer = optim.Adam(self.parameters(), lr=0.05)

    def forward(self, src_ids, tgt_ids):
        # 1. Encoder: 한글 문장 → memory
        memory = self.encoder(src_ids)

        # 2. Decoder: memory 참고하며 출력 단어 순서대로 생성
        #    tgt_ids: Teacher Forcing 입력
        #    예) 정답이 [fix, bug, <eos>] 라면
        #        입력:  [<s>, fix, bug]       (마지막 제외)
        #        정답:  [fix, bug, <eos>]     (처음 제외)
        logits = self.decoder(tgt_ids, memory)
        return logits

    def train_step(self, src_ids, tgt_ids):
        """
        Teacher Forcing:
          정답을 미리 알려주면서 학습
          입력: [<s>, fix, bug]  → 정답: [fix, bug, <eos>]
          모델이 틀려도 다음 입력은 정답으로 강제 제공 → 빠른 수렴
        """
        self.train()
        # tgt_ids[:, :-1] → <s>부터 마지막 직전까지  (디코더 입력)
        # tgt_ids[:, 1:]  → 두번째부터 끝까지        (정답)
        logits = self.forward(src_ids, tgt_ids[:, :-1])
        loss = self.criterion(
            logits.reshape(-1, len(self.tgt_vocab)),
            tgt_ids[:, 1:].reshape(-1)
        )
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def predict(self, src_words, max_len=10):
        """
        Greedy Decoding:
          <s>부터 시작해서 매 스텝 가장 확률 높은 단어 1개 선택
          <eos> 나오면 종료
        """
        self.eval()
        with torch.no_grad():
            src_ids = torch.tensor([[self.src_stoi[w] for w in src_words]])
            memory  = self.encoder(src_ids)

            # 시작 토큰 <s>로 시작
            tgt_ids = torch.tensor([[self.tgt_stoi['<s>']]])

            result = []
            for _ in range(max_len):
                logits  = self.decoder(tgt_ids, memory)
                # 마지막 위치의 점수만 보고 다음 단어 선택
                next_id = logits[:, -1, :].argmax(dim=-1, keepdim=True)

                if next_id.item() == self.tgt_stoi['<eos>']:
                    break  # <eos> 나오면 종료

                result.append(self.tgt_itos[next_id.item()])
                tgt_ids = torch.cat([tgt_ids, next_id], dim=1)

        return result


# ================================================================
# 실행
# ================================================================
bot = CommitBot()

train_data = [
    (['버그', '수정'],     ['fix', 'bug']),
    (['코드', '수정'],     ['refactor', 'code']),
    (['리팩토링', '코드'], ['refactor', 'code']),
]

def to_ids(bot, src_words, tgt_words):
    src_ids = torch.tensor([[bot.src_stoi[w] for w in src_words]])
    # Teacher Forcing용: <s> + 정답 + <eos>
    tgt_ids = torch.tensor([[
        bot.tgt_stoi['<s>']] +
        [bot.tgt_stoi[w] for w in tgt_words] +
        [bot.tgt_stoi['<eos>']]
    ])
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
    pred    = bot.predict(src_words)
    correct = pred == tgt_words
    print(f"  {src_words} → {pred}  {'✅' if correct else '❌'} (정답: {tgt_words})")

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[09 핵심 정리]

  08: Encoder → memory → fc → 끝
  09: Encoder → memory
                  ↓
      Decoder (<s> → fix → bug → <eos>)
        ① Self-Attention  : 출력 단어끼리 참조
        ② Cross-Attention : memory 참조  ★
        ③ fc              : 다음 단어 선택

  새로 추가된 개념:
    <s>/<eos>  : 시작/종료 토큰
    causal_mask: 미래 단어 차단
    Teacher Forcing: 학습 시 정답을 입력으로 강제 제공
    Greedy Decoding: 추론 시 확률 높은 단어를 하나씩 선택
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")