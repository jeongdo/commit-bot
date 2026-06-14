"""
11. LayerNorm + Residual (Add & Norm)
======================================
[10과 달라진 점]
  - 각 서브레이어(Attention, FFN) 뒤에 Residual + LayerNorm 추가
  - "Add & Norm" = Transformer 논문 원본 구조 완성
  - 이걸로 08~11 단계가 끝나고 진짜 Transformer 구조가 됨

[Residual Connection (잔차 연결)이란?]
  서브레이어 출력에 입력을 그대로 더하는 것

  09/10:  output = Attention(x)
  11:     output = x + Attention(x)   ← x를 그대로 더함

  왜 필요한가?
    레이어가 깊어질수록 기울기가 역전파 시 점점 작아짐 (기울기 소실)
    x를 더해주면 기울기가 최소 1은 보장 → 깊어도 학습 가능

  쉬운 비유:
    Attention이 아무것도 못 배웠어도 x가 그대로 전달되니까
    "최소한 입력은 보존"됨 → 학습이 안정적

[LayerNorm이란?]
  각 레이어 출력값을 정규화 (평균=0, 분산=1로 맞춤)

  왜 필요한가?
    레이어 거칠수록 값이 폭발적으로 커지거나 0으로 죽음
    정규화로 항상 적당한 범위 유지 → 학습 안정화

[적용 순서 - Post-Norm]
  x = LayerNorm(x + Attention(x))   ← Add 먼저, Norm 나중
  x = LayerNorm(x + FFN(x))

  논문 원본은 Post-Norm이고
  실제 최신 모델은 Pre-Norm도 많이 씀 (여기선 Post-Norm으로)
"""

import torch
import torch.nn as nn
import torch.optim as optim
import math


# ================================================================
# Positional Encoding (10과 동일)
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
# FFN (10과 동일)
# ================================================================
class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model),
        )

    def forward(self, x):
        return self.net(x)


# ================================================================
# Encoder (Add & Norm 추가)
# ================================================================
class Encoder(nn.Module):
    def __init__(self, vocab_size, d_model=8, nhead=2, d_ff=32):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.pos_enc   = PositionalEncoding(d_model)
        self.self_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.ffn       = FeedForward(d_model, d_ff)

        # [신규] LayerNorm 2개: Attention 뒤, FFN 뒤 각각
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, src_ids):
        emb = self.embedding(src_ids)
        emb = self.pos_enc(emb)

        # ① Self-Attention + Add & Norm
        #    10: attn_out = Attention(emb)
        #    11: attn_out = LayerNorm(emb + Attention(emb))  ← x를 더하고 정규화
        attn_out, _ = self.self_attn(emb, emb, emb)
        emb = self.norm1(emb + attn_out)   # Residual + LayerNorm

        # ② FFN + Add & Norm
        #    10: memory = FFN(attn_out)
        #    11: memory = LayerNorm(emb + FFN(emb))
        ffn_out = self.ffn(emb)
        memory  = self.norm2(emb + ffn_out)  # Residual + LayerNorm

        return memory  # (batch, src_len, d_model)


# ================================================================
# Decoder (Add & Norm 추가)
# ================================================================
class Decoder(nn.Module):
    def __init__(self, vocab_size, d_model=8, nhead=2, d_ff=32):
        super().__init__()
        self.embedding  = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.pos_enc    = PositionalEncoding(d_model)
        self.self_attn  = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.cross_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.ffn        = FeedForward(d_model, d_ff)

        # [신규] LayerNorm 3개: Self-Attention, Cross-Attention, FFN 각각
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)

        self.fc = nn.Linear(d_model, vocab_size)

    def forward(self, tgt_ids, memory):
        emb = self.embedding(tgt_ids)
        emb = self.pos_enc(emb)

        # ① Masked Self-Attention + Add & Norm
        tgt_len = tgt_ids.size(1)
        causal_mask = torch.triu(
            torch.full((tgt_len, tgt_len), float('-inf')), diagonal=1
        )
        self_out, _ = self.self_attn(emb, emb, emb, attn_mask=causal_mask)
        emb = self.norm1(emb + self_out)   # Residual + LayerNorm

        # ② Cross-Attention + Add & Norm
        cross_out, _ = self.cross_attn(emb, memory, memory)
        emb = self.norm2(emb + cross_out)  # Residual + LayerNorm

        # ③ FFN + Add & Norm
        ffn_out = self.ffn(emb)
        emb = self.norm3(emb + ffn_out)    # Residual + LayerNorm

        logits = self.fc(emb)
        return logits


# ================================================================
# CommitBot (09/10과 동일)
# ================================================================
class CommitBot(nn.Module):
    def __init__(self):
        super().__init__()

        self.src_vocab = ['<pad>', '버그', '수정', '코드', '리팩토링']
        self.src_stoi  = {w: i for i, w in enumerate(self.src_vocab)}

        self.tgt_vocab = ['<pad>', '<s>', '<eos>', 'bug', 'fix', 'code', 'refactor']
        self.tgt_stoi  = {w: i for i, w in enumerate(self.tgt_vocab)}
        self.tgt_itos  = {i: w for i, w in enumerate(self.tgt_vocab)}

        self.encoder = Encoder(len(self.src_vocab), d_model=8, nhead=2, d_ff=32)
        self.decoder = Decoder(len(self.tgt_vocab), d_model=8, nhead=2, d_ff=32)

        self.criterion = nn.CrossEntropyLoss(ignore_index=0)
        self.optimizer = optim.Adam(self.parameters(), lr=0.05)

    def forward(self, src_ids, tgt_ids):
        memory = self.encoder(src_ids)
        logits = self.decoder(tgt_ids, memory)
        return logits

    def train_step(self, src_ids, tgt_ids):
        self.train()
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
        self.eval()
        with torch.no_grad():
            src_ids = torch.tensor([[self.src_stoi[w] for w in src_words]])
            memory  = self.encoder(src_ids)
            tgt_ids = torch.tensor([[self.tgt_stoi['<s>']]])

            result = []
            for _ in range(max_len):
                logits  = self.decoder(tgt_ids, memory)
                next_id = logits[:, -1, :].argmax(dim=-1, keepdim=True)
                if next_id.item() == self.tgt_stoi['<eos>']:
                    break
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
[11 핵심 정리]

  10: Attention → FFN → 출력
  11: Attention → Add&Norm → FFN → Add&Norm → 출력

  Add & Norm = Residual + LayerNorm
    Residual:  x + 서브레이어(x)   기울기 소실 방지
    LayerNorm: 값 범위 정규화      학습 안정화

  Encoder 서브레이어 2개:
    Self-Attention → Add&Norm
    FFN            → Add&Norm

  Decoder 서브레이어 3개:
    Self-Attention  → Add&Norm
    Cross-Attention → Add&Norm
    FFN             → Add&Norm

  여기까지가 논문 원본 Transformer 구조 완성
  ━━━━━━━━━━━━━━━━━━━━━━━━
  다음 단계(12):
    d_model 키우고 레이어 쌓기
    → transformer_model.py 코드가
      왜 그렇게 생겼는지 완전히 이해됨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")