import time
import torch
import torch.nn as nn
import torch.optim as optim
import math
import json
import os


# -------------------------------
# 1. Positional Encoding (max_len=128로 안전하게 확장)
# -------------------------------
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=128):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.pe = pe.unsqueeze(0)  # (1, max_len, d_model)

    def forward(self, x):
        seq_len = x.size(1)
        return x + self.pe[:, :seq_len, :]


# -------------------------------
# 2. 인코더 (Encoder) – FFN + LayerNorm + Residual 적용
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
        emb = self.norm1(emb + attn_out)  # Residual + LayerNorm

        ffn_out = self.ffn(emb)
        emb = self.norm2(emb + ffn_out)  # Residual + LayerNorm

        return emb


# -------------------------------
# 3. 디코더 (Decoder) – FFN + LayerNorm + Residual 적용
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
# 4. 완성된 Seq2Seq Transformer
# -------------------------------
class Seq2SeqTransformer(nn.Module):
    def __init__(self, src_vocab, tgt_vocab, d_model=32, nhead=4):
        super().__init__()
        self.src_stoi = {w: i for i, w in enumerate(src_vocab)}
        self.tgt_stoi = {w: i for i, w in enumerate(tgt_vocab)}
        self.tgt_itos = {i: w for i, w in enumerate(tgt_vocab)}

        self.encoder = Encoder(len(src_vocab), d_model, nhead)
        self.decoder = Decoder(len(tgt_vocab), d_model, nhead)

        self.criterion = nn.CrossEntropyLoss(ignore_index=0)
        self.optimizer = optim.Adam(self.parameters(), lr=0.0005)

    def generate_mask(self, sz, device='cpu'):
        mask = torch.triu(torch.ones(sz, sz, device=device) * float('-inf'), diagonal=1)
        return mask

    def forward(self, src_ids, tgt_ids, src_pad_mask=None, tgt_pad_mask=None):
        memory = self.encoder(src_ids, src_pad_mask)
        tgt_mask = self.generate_mask(tgt_ids.size(1), src_ids.device)
        logits = self.decoder(tgt_ids, memory, tgt_mask, tgt_pad_mask, src_pad_mask)
        return logits

    # =====================================================================
    # 🔥🔥🔥 Scheduled Sampling 적용된 train_step 🔥🔥🔥
    # =====================================================================
    def train_step(self, src_ids, tgt_ids, teacher_forcing_ratio=0.7):
        self.train()
        src_pad_mask = (src_ids == 0).float().masked_fill(src_ids == 0, float('-inf'))

        # [1] 인코더 실행
        memory = self.encoder(src_ids, src_pad_mask)

        # [2] 디코더 초기 입력: <s> 토큰
        tgt_input = tgt_ids[:, :1]  # (batch, 1)
        tgt_out = tgt_ids[:, 1:]    # 정답 시퀀스 (첫 <s> 제외)

        total_loss = 0

        # [3] 타임스텝별 루프 (Scheduled Sampling을 위해 반복문 사용)
        for t in range(tgt_out.size(1)):
            tgt_pad_mask = (tgt_input == 0).float().masked_fill(tgt_input == 0, float('-inf'))
            tgt_mask = self.generate_mask(tgt_input.size(1), src_ids.device)

            logits = self.decoder(tgt_input, memory, tgt_mask, tgt_pad_mask, src_pad_mask)
            next_logits = logits[:, -1, :]  # 마지막 위치의 예측 점수
            target = tgt_out[:, t]          # 현재 타임스텝의 정답

            total_loss += self.criterion(next_logits, target)

            # ─────────────────────────────────────────────────
            # 🔥 Scheduled Sampling 핵심
            # 70% 확률 → 정답 사용, 30% 확률 → 모델 예측 사용
            # ─────────────────────────────────────────────────
            if self.training and torch.rand(1).item() > teacher_forcing_ratio:
                # 30%: 모델이 예측한 단어를 다음 입력으로
                next_token = next_logits.argmax(dim=-1, keepdim=True)
            else:
                # 70%: 정답 단어를 다음 입력으로
                next_token = target.unsqueeze(1)
            # ─────────────────────────────────────────────────

            tgt_input = torch.cat([tgt_input, next_token], dim=1)

        avg_loss = total_loss / tgt_out.size(1)

        self.optimizer.zero_grad()
        avg_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0)
        self.optimizer.step()

        return avg_loss.item()

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

    def eval_teacher_forcing(self, src_words, tgt_words):
        self.eval()
        src_ids = torch.tensor([[self.src_stoi[w] for w in src_words]])
        tgt_ids = torch.tensor([[self.tgt_stoi['<s>']] +
                                [self.tgt_stoi[w] for w in tgt_words] +
                                [self.tgt_stoi['<eos>']]])
        src_pad_mask = (src_ids == 0).float().masked_fill(src_ids == 0, float('-inf'))
        tgt_pad_mask = (tgt_ids[:, :-1] == 0).float().masked_fill(tgt_ids[:, :-1] == 0, float('-inf'))

        with torch.no_grad():
            logits = self.forward(src_ids, tgt_ids[:, :-1], src_pad_mask, tgt_pad_mask)
            pred_ids = logits.argmax(dim=-1)
            pred_tokens = [self.tgt_itos[i.item()] for i in pred_ids[0]]
        return pred_tokens


# -------------------------------
# 5. 학습 데이터 로드 & 실행
# -------------------------------
if __name__ == "__main__":

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    JSONL_PATH = os.path.join(project_root, "data", "commit_dataset_20000_final.jsonl")

    if not os.path.exists(JSONL_PATH):
        print(f"❌ {JSONL_PATH} 파일을 찾을 수 없습니다. 드롭박스 경로를 확인하세요.")
        exit()

    train_data = []
    all_src_words = set()
    all_tgt_words = set()

    print(f"📦 {JSONL_PATH} 로드 중...")
    with open(JSONL_PATH, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line.strip())
            src_words = item["src"].split()
            tgt_words = item["translation"].split()
            train_data.append((src_words, tgt_words))
            all_src_words.update(src_words)
            all_tgt_words.update(tgt_words)

    print(f"✅ 로드된 학습 데이터: {len(train_data)}건")

    src_vocab = ['<pad>'] + sorted(all_src_words)
    tgt_vocab = ['<pad>'] + sorted(all_tgt_words) + ['<s>', '<eos>']

    print(f"📖 src_vocab 크기: {len(src_vocab)}")
    print(f"📖 tgt_vocab 크기: {len(tgt_vocab)}")

    model = Seq2SeqTransformer(src_vocab, tgt_vocab, d_model=32, nhead=4)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"🧠 모델 파라미터 수: {total_params:,}")

    def make_tensors(model, src_words, tgt_words):
        src_ids = torch.tensor([[model.src_stoi.get(w, 0) for w in src_words]])
        tgt_ids = torch.tensor([[model.tgt_stoi['<s>']] +
                                [model.tgt_stoi.get(w, 0) for w in tgt_words] +
                                [model.tgt_stoi['<eos>']]])
        return src_ids, tgt_ids

    N_EPOCHS = 1000
    CHECKPOINT_PATH = "commit_bot_d32.pt"

    start_time = time.time()
    print(f"⏱️ 학습 시작 시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

    print(f"\n🧪 학습 전 번역 테스트 (처음 3개):")
    for src_words, _ in train_data[:3]:
        print(f"  {src_words} → {model.translate(src_words)}")

    print(f"\n📚 {N_EPOCHS} 에폭 학습 시작 (Scheduled Sampling 적용)...")
    for epoch in range(N_EPOCHS):
        total_loss = 0
        for src_words, tgt_words in train_data:
            src_ids, tgt_ids = make_tensors(model, src_words, tgt_words)
            total_loss += model.train_step(src_ids, tgt_ids)

        if epoch % 50 == 0 or epoch == N_EPOCHS - 1:
            avg_loss = total_loss / len(train_data)
            print(f"  Epoch {epoch:4d} | Avg Loss: {avg_loss:.6f}")

            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': model.optimizer.state_dict(),
                'src_vocab': src_vocab,
                'tgt_vocab': tgt_vocab,
            }, CHECKPOINT_PATH)

    print(f"\n💾 모델 저장 완료: {CHECKPOINT_PATH}")

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"\n⏱️ 학습 종료 시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print(f"⏱️ 총 소요 시간: {elapsed / 60:.1f} 분 ({elapsed / 3600:.2f} 시간)")

    print("\n✅ 학습 후 번역 결과 (100건 샘플):")
    correct_count = 0
    sample = train_data[:100]
    for src_words, tgt_words in sample:
        pred = model.translate(src_words)
        correct = pred == tgt_words
        if correct:
            correct_count += 1
        if not correct:
            print(f"  ❌ {src_words} → {pred} (정답: {tgt_words})")
    print(f"\n🎯 샘플 정확도: {correct_count}/{len(sample)} ({correct_count / len(sample) * 100:.1f}%)")

    print("\n🔍 Teacher Forcing 평가 (처음 5개):")
    for src_words, tgt_words in train_data[:5]:
        tf_pred = model.eval_teacher_forcing(src_words, tgt_words)
        print(f"  {' '.join(src_words):20} → TF: {tf_pred}  (정답: {tgt_words})")