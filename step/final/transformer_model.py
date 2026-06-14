"""
Seq2Seq Transformer - 한글 키워드 → 영어 커밋 메시지 번역 모델
=================================================================
[학습 흐름]
  한글 단어 시퀀스 (src)
      ↓ Encoder: 의미 압축 → memory
      ↓ Decoder: memory를 참고하며 영어 단어를 하나씩 생성
  영어 단어 시퀀스 (tgt)

[이전 예제와의 차이]
  위치 기반(Position-only) 예제  →  이 코드(Seq2Seq Transformer)
  - 단순 위치 인코딩만 사용      →  Self-Attention + Cross-Attention 추가
  - 번역 불가 (단방향 분류)       →  실제 번역 가능 (Encoder-Decoder 구조)
  - d_model=8, layer=1           →  d_model=64, layer=2, FFN 추가 (고도화)
"""

import torch
import torch.nn as nn
import torch.optim as optim
import math
import os
import json


# ================================================================
# 1. Positional Encoding (위치 인코딩)
# ================================================================
# Transformer는 RNN과 달리 단어 순서 정보가 없음.
# → sin/cos 함수로 각 위치(position)마다 고유한 벡터를 만들어 임베딩에 더해줌.
# 예) "버그 수정"에서 '버그'=위치0, '수정'=위치1 이 구별됨.
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=100, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        # 주파수를 로그 스케일로 분산시켜 짧은/긴 거리 패턴을 동시에 학습
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)  # 짝수 차원: sin
        pe[:, 1::2] = torch.cos(position * div_term)  # 홀수 차원: cos
        self.register_buffer('pe', pe.unsqueeze(0))   # (1, max_len, d_model)

    def forward(self, x):
        # x: (batch, seq_len, d_model)
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


# ================================================================
# 2. Feed-Forward Network (FFN)
# ================================================================
# Attention이 "어떤 단어를 볼지" 결정한다면,
# FFN은 "그 정보로 무엇을 만들지" 비선형 변환으로 표현력을 높임.
# 구조: Linear(d_model → d_ff) → ReLU → Dropout → Linear(d_ff → d_model)
class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.net(x)


# ================================================================
# 3. Encoder Layer (인코더 레이어)
# ================================================================
# [역할] 입력 문장의 "문맥 표현(memory)" 생성
#
# [구조] 2개 서브레이어:
#   ① Self-Attention: 같은 문장 내 단어끼리 서로 참조
#      예) "로그인 버그 수정"에서 '수정'이 '버그'를 가장 많이 참조
#   ② FFN: 각 위치별 비선형 변환
#
# [잔차 연결 + LayerNorm]
#   각 서브레이어 출력에 입력을 더함(residual) → 기울기 소실 방지
#   LayerNorm으로 학습 안정화
class EncoderLayer(nn.Module):
    def __init__(self, d_model, nhead, d_ff, dropout=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(d_model, nhead, dropout=dropout, batch_first=True)
        self.ffn = FeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, src_key_padding_mask=None):
        # ① Self-Attention + 잔차
        attn_out, _ = self.self_attn(x, x, x, key_padding_mask=src_key_padding_mask)
        x = self.norm1(x + self.dropout(attn_out))
        # ② FFN + 잔차
        x = self.norm2(x + self.ffn(x))
        return x


# ================================================================
# 4. Decoder Layer (디코더 레이어)
# ================================================================
# [역할] memory(인코더 출력)를 참고하여 영어 단어를 순서대로 생성
#
# [구조] 3개 서브레이어:
#   ① Masked Self-Attention: 지금까지 생성한 단어끼리만 참조
#      → 미래 단어를 미리 보지 못하게 상삼각 마스크 적용
#      예) 'fix'를 생성할 때 아직 안 나온 'bug'는 못 봄
#   ② Cross-Attention: 디코더가 인코더 출력(memory)을 참조
#      → 한글 문맥과 현재 생성 중인 영어 단어를 연결하는 핵심
#   ③ FFN: 비선형 변환
class DecoderLayer(nn.Module):
    def __init__(self, d_model, nhead, d_ff, dropout=0.1):
        super().__init__()
        # ① Masked Self-Attention (디코더 자체)
        self.self_attn = nn.MultiheadAttention(d_model, nhead, dropout=dropout, batch_first=True)
        # ② Cross-Attention (인코더 memory 참조)
        self.cross_attn = nn.MultiheadAttention(d_model, nhead, dropout=dropout, batch_first=True)
        self.ffn = FeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, memory, tgt_mask=None, tgt_key_padding_mask=None):
        # ① Masked Self-Attention
        self_out, _ = self.self_attn(x, x, x, attn_mask=tgt_mask,
                                     key_padding_mask=tgt_key_padding_mask)
        x = self.norm1(x + self.dropout(self_out))

        # ② Cross-Attention: query=디코더, key/value=인코더 memory
        cross_out, _ = self.cross_attn(x, memory, memory)
        x = self.norm2(x + self.dropout(cross_out))

        # ③ FFN
        x = self.norm3(x + self.ffn(x))
        return x


# ================================================================
# 5. Encoder (인코더 전체)
# ================================================================
# EncoderLayer를 num_layers개 쌓아 점점 깊은 문맥 표현 생성
# 레이어가 깊어질수록 단어 간 복잡한 관계 학습 가능
class Encoder(nn.Module):
    def __init__(self, src_vocab_size, d_model, nhead, d_ff, num_layers, dropout=0.1):
        super().__init__()
        # 단어 → 벡터 변환 (padding_idx=0: <pad> 토큰은 학습 제외)
        self.embedding = nn.Embedding(src_vocab_size, d_model, padding_idx=0)
        self.pos_enc = PositionalEncoding(d_model, dropout=dropout)
        self.layers = nn.ModuleList([
            EncoderLayer(d_model, nhead, d_ff, dropout) for _ in range(num_layers)
        ])
        self.norm = nn.LayerNorm(d_model)

    def forward(self, src_ids, src_key_padding_mask=None):
        x = self.embedding(src_ids) * math.sqrt(self.embedding.embedding_dim)
        x = self.pos_enc(x)
        for layer in self.layers:
            x = layer(x, src_key_padding_mask)
        return self.norm(x)  # memory: (batch, src_len, d_model)


# ================================================================
# 6. Decoder (디코더 전체)
# ================================================================
class Decoder(nn.Module):
    def __init__(self, tgt_vocab_size, d_model, nhead, d_ff, num_layers, dropout=0.1):
        super().__init__()
        self.embedding = nn.Embedding(tgt_vocab_size, d_model, padding_idx=0)
        self.pos_enc = PositionalEncoding(d_model, dropout=dropout)
        self.layers = nn.ModuleList([
            DecoderLayer(d_model, nhead, d_ff, dropout) for _ in range(num_layers)
        ])
        self.norm = nn.LayerNorm(d_model)
        # 최종 출력: d_model → tgt_vocab_size (각 단어의 확률 점수)
        self.fc = nn.Linear(d_model, tgt_vocab_size)

    def forward(self, tgt_ids, memory, tgt_mask=None):
        x = self.embedding(tgt_ids) * math.sqrt(self.embedding.embedding_dim)
        x = self.pos_enc(x)
        for layer in self.layers:
            x = layer(x, memory, tgt_mask)
        x = self.norm(x)
        return self.fc(x)  # logits: (batch, tgt_len, tgt_vocab_size)


# ================================================================
# 7. Seq2Seq Transformer (최종 모델)
# ================================================================
class Seq2SeqTransformer(nn.Module):
    def __init__(self, src_vocab, tgt_vocab,
                 d_model=64, nhead=4, d_ff=256, num_layers=2, dropout=0.1):
        super().__init__()
        # 단어 ↔ 인덱스 변환 딕셔너리
        self.src_stoi = {w: i for i, w in enumerate(src_vocab)}
        self.tgt_stoi = {w: i for i, w in enumerate(tgt_vocab)}
        self.tgt_itos = {i: w for i, w in enumerate(tgt_vocab)}

        self.encoder = Encoder(len(src_vocab), d_model, nhead, d_ff, num_layers, dropout)
        self.decoder = Decoder(len(tgt_vocab), d_model, nhead, d_ff, num_layers, dropout)

        # <pad>=0 인덱스는 loss 계산에서 제외
        self.criterion = nn.CrossEntropyLoss(ignore_index=0)
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        # 학습률 스케줄러: 50 에폭마다 lr을 0.5배로 감소
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=50, gamma=0.5)

        self._init_weights()

    def _init_weights(self):
        """Xavier 초기화: 레이어 깊어져도 기울기가 안정적으로 흐르게 함"""
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

    def generate_causal_mask(self, sz):
        """
        Causal(인과) 마스크: 디코더가 미래 토큰을 보지 못하게 차단
        예) sz=3일 때:
            [[0,   -inf, -inf],
             [0,    0,   -inf],
             [0,    0,    0  ]]
        → 위치 i는 위치 0~i까지만 참조 가능
        """
        return torch.triu(torch.full((sz, sz), float('-inf')), diagonal=1)

    def forward(self, src_ids, tgt_ids):
        memory = self.encoder(src_ids)
        tgt_mask = self.generate_causal_mask(tgt_ids.size(1)).to(src_ids.device)
        return self.decoder(tgt_ids, memory, tgt_mask)

    def train_step(self, src_ids, tgt_ids):
        """
        Teacher Forcing 학습:
        - 입력: tgt_ids[:, :-1]  → <s> fix bug  (마지막 제외)
        - 정답: tgt_ids[:, 1:]   →  fix bug <eos> (처음 제외)
        → 모델이 틀려도 정답을 다음 입력으로 강제 제공 → 빠른 수렴
        """
        self.train()
        logits = self.forward(src_ids, tgt_ids[:, :-1])
        loss = self.criterion(
            logits.reshape(-1, logits.size(-1)),
            tgt_ids[:, 1:].reshape(-1)
        )
        self.optimizer.zero_grad()
        loss.backward()
        # Gradient Clipping: 기울기 폭발 방지 (max_norm=1.0)
        nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0)
        self.optimizer.step()
        return loss.item()

    def translate(self, src_words, max_len=10):
        """
        Greedy Decoding (추론):
        매 스텝마다 가장 확률 높은 단어 1개 선택
        → <eos> 나오거나 max_len 도달하면 종료
        """
        self.eval()
        with torch.no_grad():
            src_ids = torch.tensor([[self.src_stoi.get(w, 0) for w in src_words]])
            memory = self.encoder(src_ids)
            tgt_ids = torch.tensor([[self.tgt_stoi['<s>']]])

            for _ in range(max_len):
                tgt_mask = self.generate_causal_mask(tgt_ids.size(1))
                logits = self.decoder(tgt_ids, memory, tgt_mask)
                next_id = logits[:, -1, :].argmax(dim=-1, keepdim=True)
                if next_id.item() == self.tgt_stoi['<eos>']:
                    break
                tgt_ids = torch.cat([tgt_ids, next_id], dim=1)

        result_ids = tgt_ids[0, 1:].tolist()
        return [self.tgt_itos[i] for i in result_ids
                if i not in (0, self.tgt_stoi.get('<eos>', -1))]

    def save(self, path):
        torch.save({
            'state_dict': self.state_dict(),
            'src_stoi': self.src_stoi,
            'tgt_stoi': self.tgt_stoi,
            'tgt_itos': self.tgt_itos,
        }, path)
        print(f"💾 모델 저장: {path}")

    @classmethod
    def load(cls, path):
        ckpt = torch.load(path, map_location='cpu')
        src_vocab = [w for w, _ in sorted(ckpt['src_stoi'].items(), key=lambda x: x[1])]
        tgt_vocab = [w for w, _ in sorted(ckpt['tgt_stoi'].items(), key=lambda x: x[1])]
        model = cls(src_vocab, tgt_vocab)
        model.load_state_dict(ckpt['state_dict'])
        print(f"✅ 모델 로드: {path}")
        return model


# ================================================================
# 8. 학습 실행
# ================================================================
if __name__ == "__main__":
    train_data = [
        (['버그', '수정'],              ['fix', 'bug']),
        (['코드', '수정'],              ['refactor', 'code']),
        (['리팩토링', '코드'],          ['refactor', 'code']),
        (['기능', '추가'],              ['add', 'feature']),
        (['로그인', '오류', '수정'],    ['fix', 'login', 'error']),
        (['회원가입', '버그', '수정'],  ['fix', 'signup', 'bug']),
        (['버그', '수정', '코드'],      ['fix', 'bug', 'code']),
        (['기능', '삭제'],              ['remove', 'feature']),
        (['로그인', '버그'],            ['login', 'bug']),
        (['회원가입', '기능', '추가'],  ['add', 'signup', 'feature']),
        (['오류', '수정'],              ['fix', 'error']),
        (['코드', '리팩토링'],          ['refactor', 'code']),
        (['버그', '추가'],              ['add', 'bug']),
        (['기능', '수정'],              ['modify', 'feature']),
        (['로그인', '기능', '추가'],    ['add', 'login', 'feature']),
        (['회원가입', '오류'],          ['signup', 'error']),
        (['삭제', '기능'],              ['remove', 'feature']),
        (['추가', '기능'],              ['add', 'feature']),
        (['수정', '버그'],              ['fix', 'bug']),
        (['수정', '코드'],              ['refactor', 'code']),
        (['코드', '추가'],              ['add', 'code']),
        (['리팩토링', '로그인'],        ['refactor', 'login']),
        (['버그', '리팩토링'],          ['refactor', 'bug']),
        (['회원가입', '수정'],          ['fix', 'signup']),
        (['로그인', '수정'],            ['fix', 'login']),
        (['오류', '추가'],              ['add', 'error']),
        (['코드', '오류', '수정'],      ['fix', 'code', 'error']),
        (['리팩토링', '오류'],          ['refactor', 'error']),
        (['기능', '오류'],              ['feature', 'error']),
        (['버그', '회원가입'],          ['signup', 'bug']),
        (['로그인', '리팩토링'],        ['refactor', 'login']),
        (['회원가입', '리팩토링'],      ['refactor', 'signup']),
        (['삭제', '버그'],              ['remove', 'bug']),
        (['삭제', '코드'],              ['delete', 'code']),
        (['수정', '로그인', '오류'],    ['fix', 'login', 'error']),
        (['추가', '로그인'],            ['add', 'login']),
        (['추가', '회원가입'],          ['add', 'signup']),
        (['오류', '회원가입'],          ['signup', 'error']),
        (['코드', '버그'],              ['code', 'bug']),
        (['리팩토링', '버그'],          ['refactor', 'bug']),
        (['기능', '로그인'],            ['login', 'feature']),
        (['기능', '회원가입'],          ['signup', 'feature']),
        (['버그', '코드', '수정'],      ['fix', 'code', 'bug']),
        (['오류', '코드'],              ['code', 'error']),
        (['수정', '회원가입', '버그'],  ['fix', 'signup', 'bug']),
        (['추가', '버그'],              ['add', 'bug']),
        (['삭제', '로그인'],            ['remove', 'login']),
        (['삭제', '회원가입'],          ['delete', 'signup']),
        (['리팩토링', '기능'],          ['refactor', 'feature']),
        (['수정', '기능', '오류'],      ['fix', 'feature', 'error']),
        (['코드', '회원가입'],          ['signup', 'code']),
        (['로그인', '삭제'],            ['remove', 'login']),
        (['회원가입', '삭제'],          ['delete', 'signup']),
        (['오류', '삭제'],              ['remove', 'error']),
        (['버그', '삭제'],              ['delete', 'bug']),
        (['코드', '삭제'],              ['remove', 'code']),
        (['리팩토링', '삭제'],          ['delete', 'refactor']),
        (['기능', '리팩토링'],          ['refactor', 'feature']),
        (['로그인', '버그', '수정'],    ['fix', 'login', 'bug']),
        (['회원가입', '코드', '수정'],  ['refactor', 'signup', 'code']),
        (['기능', '버그'],              ['feature', 'bug']),
        (['오류', '리팩토링'],          ['refactor', 'error']),
        (['수정', '오류', '로그인'],    ['fix', 'login', 'error']),
        (['추가', '오류'],              ['add', 'error']),
        (['버그', '기능', '수정'],      ['fix', 'feature', 'bug']),
        (['코드', '기능', '추가'],      ['add', 'feature', 'code']),
        (['로그인', '코드'],            ['login', 'code']),
        (['회원가입', '기능'],          ['signup', 'feature']),
        (['리팩토링', '회원가입'],      ['refactor', 'signup']),
        (['오류', '기능'],              ['feature', 'error']),
        (['버그', '로그인'],            ['login', 'bug']),
        (['삭제', '오류'],              ['delete', 'error']),
        (['수정', '리팩토링'],          ['refactor', 'fix']),
        (['추가', '리팩토링'],          ['refactor', 'add']),
        (['코드', '로그인', '오류'],    ['fix', 'login', 'code', 'error']),
        (['회원가입', '오류', '수정'],  ['fix', 'signup', 'error']),
        (['기능', '삭제', '버그'],      ['remove', 'bug', 'feature']),
        (['로그인', '기능', '삭제'],    ['delete', 'login', 'feature']),
        (['리팩토링', '수정'],          ['fix', 'refactor']),
        (['버그', '오류'],              ['bug', 'error']),
        (['코드', '추가', '기능'],      ['add', 'feature', 'code']),
        (['회원가입', '추가'],          ['add', 'signup']),
        (['로그인', '추가'],            ['add', 'login']),
        (['삭제', '기능', '로그인'],    ['remove', 'login', 'feature']),
        (['수정', '추가'],              ['fix', 'add']),
        (['오류', '버그', '수정'],      ['fix', 'bug', 'error']),
        (['리팩토링', '코드', '버그'],  ['refactor', 'bug', 'code']),
        (['기능', '코드'],              ['feature', 'code']),
        (['회원가입', '코드'],          ['signup', 'code']),
        (['로그인', '리팩토링', '오류'],['refactor', 'login', 'error']),
        (['버그', '리팩토링', '수정'],  ['fix', 'refactor', 'bug']),
        (['코드', '수정', '로그인'],    ['fix', 'login', 'code']),
        (['삭제', '리팩토링'],          ['delete', 'refactor']),
        (['추가', '코드', '수정'],      ['fix', 'add', 'code']),
        (['기능', '수정', '버그'],      ['fix', 'bug', 'feature']),
        (['오류', '추가', '로그인'],    ['add', 'login', 'error']),
        (['회원가입', '삭제', '오류'],  ['delete', 'signup', 'error']),
        (['로그인', '버그', '리팩토링'],['refactor', 'login', 'bug']),
        (['리팩토링', '기능', '추가'],  ['add', 'feature', 'refactor']),
        (['버그', '코드', '리팩토링'],  ['refactor', 'code', 'bug']),
    ]

    # vocab 자동 추출
    src_words_all = {w for src, _ in train_data for w in src}
    tgt_words_all = {w for _, tgt in train_data for w in tgt}
    src_vocab = ['<pad>'] + sorted(src_words_all)
    tgt_vocab = ['<pad>'] + sorted(tgt_words_all) + ['<s>', '<eos>']

    print(f"📖 src_vocab ({len(src_vocab)}개): {src_vocab}")
    print(f"📖 tgt_vocab ({len(tgt_vocab)}개): {tgt_vocab}")

    # 고도화된 하이퍼파라미터
    model = Seq2SeqTransformer(
        src_vocab, tgt_vocab,
        d_model=64,    # 임베딩 차원 (이전: 8 → 8배 확장)
        nhead=4,       # Attention 헤드 수 (이전: 2 → 2배)
        d_ff=256,      # FFN 내부 차원 (d_model의 4배)
        num_layers=2,  # 인코더/디코더 레이어 수 (이전: 1 → 2)
        dropout=0.1,
    )
    total_params = sum(p.numel() for p in model.parameters())
    print(f"🔢 모델 파라미터 수: {total_params:,}")

    def make_tensors(src_words, tgt_words):
        src_ids = torch.tensor([[model.src_stoi[w] for w in src_words]])
        tgt_ids = torch.tensor([[model.tgt_stoi['<s>']] +
                                 [model.tgt_stoi[w] for w in tgt_words] +
                                 [model.tgt_stoi['<eos>']]])
        return src_ids, tgt_ids

    print("\n📚 학습 시작...")
    EPOCHS = 3000
    for epoch in range(EPOCHS):
        total_loss = 0
        for src_words, tgt_words in train_data:
            src_ids, tgt_ids = make_tensors(src_words, tgt_words)
            total_loss += model.train_step(src_ids, tgt_ids)
        model.scheduler.step()
        if epoch % 300 == 0 or epoch == EPOCHS - 1:
            lr = model.optimizer.param_groups[0]['lr']
            print(f"  Epoch {epoch:4d} | Loss: {total_loss:.4f} | LR: {lr:.6f}")

    # 모델 저장
    model.save("commit_model.pt")

    print("\n✅ 학습 후 번역 결과:")
    correct_count = 0
    for src_words, tgt_words in train_data:
        pred = model.translate(src_words)
        correct = pred == tgt_words
        if correct:
            correct_count += 1
        status = '✅' if correct else '❌'
        print(f"  {status} {src_words} → {pred}  (정답: {tgt_words})")

    print(f"\n🎯 정확도: {correct_count}/{len(train_data)} ({correct_count/len(train_data)*100:.1f}%)")
