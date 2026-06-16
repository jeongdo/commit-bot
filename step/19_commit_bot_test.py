# translate_interactive.py
# 실행하면 한글 커밋 메시지를 입력받아 영어로 번역합니다.
# 종료: 'exit' 또는 빈 엔터

import torch
import torch.nn as nn
import math
import os

# -------------------------------
# 1. Positional Encoding
# -------------------------------
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=128):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.pe = pe.unsqueeze(0)

    def forward(self, x):
        seq_len = x.size(1)
        return x + self.pe[:, :seq_len, :]

# -------------------------------
# 2. 인코더 (FFN + LayerNorm + Residual)
# -------------------------------
class Encoder(nn.Module):
    def __init__(self, src_vocab_size, d_model=32, nhead=4, dim_feedforward=64):
        super().__init__()
        self.embedding = nn.Embedding(src_vocab_size, d_model, padding_idx=0)
        self.pos_enc = PositionalEncoding(d_model)
        self.self_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, dim_feedforward),
            nn.ReLU(),
            nn.Linear(dim_feedforward, d_model)
        )

    def forward(self, src_ids, src_pad_mask=None):
        emb = self.embedding(src_ids)
        emb = self.pos_enc(emb)
        attn_out, _ = self.self_attn(emb, emb, emb, key_padding_mask=src_pad_mask)
        emb = self.norm1(emb + attn_out)
        ffn_out = self.ffn(emb)
        emb = self.norm2(emb + ffn_out)
        return emb

# -------------------------------
# 3. 디코더 (FFN + LayerNorm + Residual)
# -------------------------------
class Decoder(nn.Module):
    def __init__(self, tgt_vocab_size, d_model=32, nhead=4, dim_feedforward=64):
        super().__init__()
        self.embedding = nn.Embedding(tgt_vocab_size, d_model, padding_idx=0)
        self.pos_enc = PositionalEncoding(d_model)
        self.self_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.cross_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, dim_feedforward),
            nn.ReLU(),
            nn.Linear(dim_feedforward, d_model)
        )
        self.fc = nn.Linear(d_model, tgt_vocab_size)

    def forward(self, tgt_ids, memory, tgt_mask=None, tgt_pad_mask=None, mem_pad_mask=None):
        emb = self.embedding(tgt_ids)
        emb = self.pos_enc(emb)
        self_out, _ = self.self_attn(emb, emb, emb, attn_mask=tgt_mask, key_padding_mask=tgt_pad_mask)
        emb = self.norm1(emb + self_out)
        cross_out, _ = self.cross_attn(emb, memory, memory, key_padding_mask=mem_pad_mask)
        emb = self.norm2(emb + cross_out)
        ffn_out = self.ffn(emb)
        emb = self.norm3(emb + ffn_out)
        logits = self.fc(emb)
        return logits

# -------------------------------
# 4. 완전한 Seq2Seq Transformer
# -------------------------------
class Seq2SeqTransformer(nn.Module):
    def __init__(self, src_vocab, tgt_vocab, d_model=32, nhead=4):
        super().__init__()
        self.src_stoi = {w: i for i, w in enumerate(src_vocab)}
        self.tgt_stoi = {w: i for i, w in enumerate(tgt_vocab)}
        self.tgt_itos = {i: w for i, w in enumerate(tgt_vocab)}
        self.encoder = Encoder(len(src_vocab), d_model, nhead)
        self.decoder = Decoder(len(tgt_vocab), d_model, nhead)

    def generate_mask(self, sz, device='cpu'):
        mask = torch.triu(torch.ones(sz, sz, device=device) * float('-inf'), diagonal=1)
        return mask

    def forward(self, src_ids, tgt_ids, src_pad_mask=None, tgt_pad_mask=None):
        memory = self.encoder(src_ids, src_pad_mask)
        tgt_mask = self.generate_mask(tgt_ids.size(1), src_ids.device)
        logits = self.decoder(tgt_ids, memory, tgt_mask, tgt_pad_mask, src_pad_mask)
        return logits

    def translate(self, src_words, max_len=10):
        self.eval()
        src_ids = torch.tensor([[self.src_stoi.get(w, 0) for w in src_words]])
        src_pad_mask = (src_ids == 0).float().masked_fill(src_ids == 0, float('-inf'))
        memory = self.encoder(src_ids, src_pad_mask)

        tgt_ids = torch.tensor([[self.tgt_stoi['<s>']]])
        for _ in range(max_len):
            tgt_pad_mask = (tgt_ids == 0).float().masked_fill(tgt_ids == 0, float('-inf'))
            tgt_mask = self.generate_mask(tgt_ids.size(1), src_ids.device)
            with torch.no_grad():
                logits = self.decoder(tgt_ids, memory, tgt_mask, tgt_pad_mask, src_pad_mask)
            next_id = logits[:, -1, :].argmax(dim=-1, keepdim=True)
            if next_id.item() == self.tgt_stoi.get('<eos>', -1):
                break
            tgt_ids = torch.cat([tgt_ids, next_id], dim=1)

        result_ids = tgt_ids[0, 1:].tolist()
        return [self.tgt_itos[i] for i in result_ids if i not in (0, self.tgt_stoi.get('<eos>', -1))]

# -------------------------------
# 5. 대화형 번역 실행
# -------------------------------
if __name__ == "__main__":
    CHECKPOINT_PATH = "commit_bot_d32.pt"   # 학습이 저장된 파일 경로

    if not os.path.exists(CHECKPOINT_PATH):
        print(f"❌ 모델 파일을 찾을 수 없습니다: {CHECKPOINT_PATH}")
        exit(1)

    print("🧠 커밋봇 모델 로딩 중...")
    checkpoint = torch.load(CHECKPOINT_PATH, map_location='cpu')
    src_vocab = checkpoint['src_vocab']
    tgt_vocab = checkpoint['tgt_vocab']

    model = Seq2SeqTransformer(src_vocab, tgt_vocab, d_model=32, nhead=4)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    print("✅ 로딩 완료! 번역을 시작합니다.\n")

    while True:
        try:
            src_text = input("한글 커밋 메시지 (종료: exit 또는 빈 엔터): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 종료합니다.")
            break

        if not src_text or src_text.lower() == 'exit':
            print("👋 종료합니다.")
            break

        # 공백 기준으로 분리 (학습 데이터와 동일한 토큰화 방식)
        src_words = src_text.split()
        result_words = model.translate(src_words)
        print(f"👉 영어 번역: {' '.join(result_words)}\n")