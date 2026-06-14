"""
10. FFN (Feed-Forward Network) 추가
=====================================
[09와 달라진 점]
  - Encoder, Decoder 각각에 FFN 추가
  - 동작 결과는 09보다 더 정확해짐 (표현력 증가)

[FFN이란?]
  Attention이 "어떤 단어를 볼지" 결정했다면
  FFN은 "그 정보로 뭘 만들지" 비선형 변환으로 처리

  구조: Linear(d_model → d_ff) → ReLU → Linear(d_ff → d_model)
        8차원 → 32차원으로 늘렸다가 → 다시 8차원으로 줄임
        중간에 늘리는 이유: 더 복잡한 패턴을 학습하기 위해

[왜 필요한가?]
  Attention만 있으면:
    "버그" + "수정" → 두 단어 정보를 섞는 것까지만 가능
  FFN까지 있으면:
    섞인 정보를 비선형 변환 → 더 복잡한 의미 표현 가능

  비선형이 중요한 이유:
    Linear만 쌓으면 아무리 깊어도 결국 Linear 1개랑 동일
    ReLU 같은 비선형 함수가 있어야 진짜 "깊은" 학습이 됨
"""

import torch
import torch.nn as nn
import torch.optim as optim
import math


# ================================================================
# Positional Encoding (09와 동일)
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
# [신규] FFN 클래스
# ================================================================
class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        # d_model=8, d_ff=32 기준:
        #
        # Linear(8 → 32): 8차원을 32차원으로 확장
        #   → 더 넓은 공간에서 복잡한 패턴 학습
        #
        # ReLU: 음수는 0으로, 양수는 그대로
        #   → 비선형성 추가 (이게 없으면 Linear 2개는 Linear 1개랑 동일)
        #   → 예) [-0.3, 0.5, -0.1, 0.8] → [0, 0.5, 0, 0.8]
        #
        # Linear(32 → 8): 다시 원래 차원으로 복원
        #   → Attention 출력과 같은 shape 유지해야 다음 레이어에 전달 가능
        self.net = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model),
        )

    def forward(self, x):
        # x: (batch, seq_len, d_model)
        # 각 단어 위치(seq_len)마다 독립적으로 FFN 적용
        # Attention이 "단어 간 관계" 를 보는 것과 달리
        # FFN은 "각 단어를 개별적으로" 변환
        return self.net(x)  # (batch, seq_len, d_model)


# ================================================================
# Encoder (FFN 추가)
# ================================================================
class Encoder(nn.Module):
    def __init__(self, vocab_size, d_model=8, nhead=2, d_ff=32):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.pos_enc   = PositionalEncoding(d_model)
        self.self_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)

        # [신규] Attention 뒤에 FFN 추가
        self.ffn = FeedForward(d_model, d_ff)

    def forward(self, src_ids):
        emb = self.embedding(src_ids)
        emb = self.pos_enc(emb)

        # ① Self-Attention: 단어 간 관계 파악
        attn_out, _ = self.self_attn(emb, emb, emb)

        # ② FFN: 각 단어를 개별적으로 비선형 변환
        #    09: memory = attn_out  (Attention 출력 그대로)
        #    10: memory = ffn(attn_out)  (FFN 한 번 더 처리)
        memory = self.ffn(attn_out)

        return memory  # (batch, src_len, d_model)


# ================================================================
# Decoder (FFN 추가)
# ================================================================
class Decoder(nn.Module):
    def __init__(self, vocab_size, d_model=8, nhead=2, d_ff=32):
        super().__init__()
        self.embedding  = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.pos_enc    = PositionalEncoding(d_model)
        self.self_attn  = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.cross_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)

        # [신규] Cross-Attention 뒤에 FFN 추가
        self.ffn = FeedForward(d_model, d_ff)

        self.fc = nn.Linear(d_model, vocab_size)

    def forward(self, tgt_ids, memory):
        emb = self.embedding(tgt_ids)
        emb = self.pos_enc(emb)

        # ① Masked Self-Attention
        tgt_len = tgt_ids.size(1)
        causal_mask = torch.triu(
            torch.full((tgt_len, tgt_len), float('-inf')), diagonal=1
        )
        self_out, _ = self.self_attn(emb, emb, emb, attn_mask=causal_mask)

        # ② Cross-Attention: memory 참조
        cross_out, _ = self.cross_attn(self_out, memory, memory)

        # ③ FFN: Cross-Attention 출력을 비선형 변환
        #    09: logits = fc(cross_out)
        #    10: logits = fc(ffn(cross_out))  ← FFN 한 단계 추가
        ffn_out = self.ffn(cross_out)

        logits = self.fc(ffn_out)
        return logits


# ================================================================
# CommitBot (09와 동일, Encoder/Decoder만 업그레이드됨)
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
[10 핵심 정리]

  09: Attention → 출력
  10: Attention → FFN → 출력

  FFN 구조:
    Linear(8→32) → ReLU → Linear(32→8)
    늘렸다가 줄이는 이유: 넓은 공간에서 복잡한 패턴 학습

  Encoder, Decoder 둘 다 FFN 추가됨:
    Encoder: Self-Attention → FFN → memory
    Decoder: Self-Attention → Cross-Attention → FFN → fc

  다음 단계(11):
    LayerNorm + Residual 추가
    "Add & Norm" - 논문 원본 구조 완성
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")