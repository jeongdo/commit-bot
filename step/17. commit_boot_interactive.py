# translate_interactive.py
# 실행하면 직접 한글 커밋 메시지를 입력받아 영어로 번역합니다.
# 종료하려면 'exit' 또는 빈 엔터를 입력하세요.

import torch
import torch.nn as nn
import math

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
# 2. 인코더 (Encoder)
# -------------------------------
class Encoder(nn.Module):
    def __init__(self, src_vocab_size, d_model=32, nhead=4):
        super().__init__()
        self.embedding = nn.Embedding(src_vocab_size, d_model, padding_idx=0)
        self.pos_enc = PositionalEncoding(d_model)
        self.self_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)

    def forward(self, src_ids, src_pad_mask=None):
        emb = self.embedding(src_ids)
        emb = self.pos_enc(emb)
        memory, _ = self.self_attn(emb, emb, emb, key_padding_mask=src_pad_mask)
        return memory

# -------------------------------
# 3. 디코더 (Decoder)
# -------------------------------
class Decoder(nn.Module):
    def __init__(self, tgt_vocab_size, d_model=32, nhead=4):
        super().__init__()
        self.embedding = nn.Embedding(tgt_vocab_size, d_model, padding_idx=0)
        self.pos_enc = PositionalEncoding(d_model)
        self.self_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.cross_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.fc = nn.Linear(d_model, tgt_vocab_size)

    def forward(self, tgt_ids, memory, tgt_mask=None, tgt_pad_mask=None, mem_pad_mask=None):
        emb = self.embedding(tgt_ids)
        emb = self.pos_enc(emb)
        self_out, _ = self.self_attn(emb, emb, emb, attn_mask=tgt_mask, key_padding_mask=tgt_pad_mask)
        cross_out, _ = self.cross_attn(self_out, memory, memory, key_padding_mask=mem_pad_mask)
        logits = self.fc(cross_out)
        return logits

# -------------------------------
# 4. Seq2Seq Transformer
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
# 5. 대화형 번역기 실행
# -------------------------------
if __name__ == "__main__":
    CHECKPOINT_PATH = "commit_bot_d32.pt"

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

        src_words = src_text.split()
        result = model.translate(src_words)
        print(f"👉 영어 번역: {' '.join(result)}\n")