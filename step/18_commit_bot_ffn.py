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
# 2. 인코더 (Encoder) – [업그레이드] FFN + LayerNorm + Residual 적용
# -------------------------------
class Encoder(nn.Module):
    def __init__(self, src_vocab_size, d_model=32, nhead=4, dim_feedforward=64):
        super().__init__()
        self.embedding = nn.Embedding(src_vocab_size, d_model, padding_idx=0)
        self.pos_enc = PositionalEncoding(d_model)
        self.self_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)

        # === [신규] FFN + LayerNorm 추가 ===
        # LayerNorm: 각 층의 출력 분포를 안정화하여 학습 속도를 높이고 Gradient 소실을 방지합니다.
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        # FFN (Feed-Forward Network): Attention이 찾은 관계를 비선형 변환하여 더 복잡한 패턴을 표현합니다.
        self.ffn = nn.Sequential(
            nn.Linear(d_model, dim_feedforward),
            nn.ReLU(),
            nn.Linear(dim_feedforward, d_model)
        )

    def forward(self, src_ids, src_pad_mask=None):
        emb = self.embedding(src_ids)
        emb = self.pos_enc(emb)

        # 1. Self-Attention + Residual Connection + LayerNorm
        # [핵심] 입력(emb)을 Attention 출력에 그대로 더해줌으로써 정보 소실을 막습니다.
        attn_out, _ = self.self_attn(emb, emb, emb, key_padding_mask=src_pad_mask)
        emb = self.norm1(emb + attn_out)  # Residual + LayerNorm

        # 2. FFN (깊이 생각하기) + Residual Connection + LayerNorm
        # [핵심] 비선형 변환을 통해 더 복잡한 의미를 학습합니다.
        ffn_out = self.ffn(emb)
        emb = self.norm2(emb + ffn_out)  # Residual + LayerNorm

        return emb


# -------------------------------
# 3. 디코더 (Decoder) – [업그레이드] FFN + LayerNorm + Residual 적용
# -------------------------------
class Decoder(nn.Module):
    def __init__(self, tgt_vocab_size, d_model=32, nhead=4, dim_feedforward=64):
        super().__init__()
        self.embedding = nn.Embedding(tgt_vocab_size, d_model, padding_idx=0)
        self.pos_enc = PositionalEncoding(d_model)
        self.self_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.cross_attn = nn.MultiheadAttention(d_model, nhead, batch_first=True)

        # === [신규] FFN + LayerNorm 추가 ===
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

        # 1. Masked Self-Attention + Residual + LayerNorm
        self_out, _ = self.self_attn(emb, emb, emb, attn_mask=tgt_mask, key_padding_mask=tgt_pad_mask)
        emb = self.norm1(emb + self_out)

        # 2. Cross-Attention + Residual + LayerNorm
        # [핵심] 디코더가 인코더의 정보를 참조한 후에도 원래 정보를 잃지 않도록 Residual을 적용합니다.
        cross_out, _ = self.cross_attn(emb, memory, memory, key_padding_mask=mem_pad_mask)
        emb = self.norm2(emb + cross_out)

        # 3. FFN (깊이 생각하기) + Residual + LayerNorm
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
        # [핵심] Transformer는 작은 학습률에서 안정적으로 학습됩니다.
        self.optimizer = optim.Adam(self.parameters(), lr=0.0005)

    def generate_mask(self, sz, device='cpu'):
        """상삼각 마스크 (미래 차단). 0: 허용, -inf: 차단"""
        mask = torch.triu(torch.ones(sz, sz, device=device) * float('-inf'), diagonal=1)
        return mask

    def forward(self, src_ids, tgt_ids, src_pad_mask=None, tgt_pad_mask=None):
        memory = self.encoder(src_ids, src_pad_mask)
        tgt_mask = self.generate_mask(tgt_ids.size(1), src_ids.device)
        logits = self.decoder(tgt_ids, memory, tgt_mask, tgt_pad_mask, src_pad_mask)
        return logits

    def train_step(self, src_ids, tgt_ids):
        self.train()
        # [핵심] 마스크 타입을 float형으로 통일 (MultiheadAttention 요구사항)
        src_pad_mask = (src_ids == 0).float().masked_fill(src_ids == 0, float('-inf'))
        tgt_in = tgt_ids[:, :-1]  # <s> ... 마지막 앞까지
        tgt_out = tgt_ids[:, 1:]  # 첫 정답 ... <eos>
        tgt_pad_mask = (tgt_in == 0).float().masked_fill(tgt_in == 0, float('-inf'))

        logits = self.forward(src_ids, tgt_in, src_pad_mask, tgt_pad_mask)
        loss = self.criterion(logits.view(-1, logits.size(-1)), tgt_out.reshape(-1))

        self.optimizer.zero_grad()
        loss.backward()
        # [핵심] 기울기 폭발 방지
        torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0)
        self.optimizer.step()
        return loss.item()

    def translate(self, src_words, max_len=10):
        """실제 번역 (추론)"""
        self.eval()
        src_ids = torch.tensor([[self.src_stoi.get(w, 0) for w in src_words]])  # OOV는 <pad>로
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
        # <eos>나 <pad> 제외
        return [self.tgt_itos[i] for i in result_ids if i not in (0, self.tgt_stoi.get('<eos>', -1))]

    def eval_teacher_forcing(self, src_words, tgt_words):
        """Teacher Forcing 평가 – 학습이 제대로 되었는지 진단"""
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

    # ── vocab 자동 생성 ──
    src_vocab = ['<pad>'] + sorted(all_src_words)
    tgt_vocab = ['<pad>'] + sorted(all_tgt_words) + ['<s>', '<eos>']

    print(f"📖 src_vocab 크기: {len(src_vocab)}")
    print(f"📖 tgt_vocab 크기: {len(tgt_vocab)}")

    # ── 모델 생성 (d_model=32, nhead=4) ──
    model = Seq2SeqTransformer(src_vocab, tgt_vocab, d_model=32, nhead=4)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"🧠 모델 파라미터 수: {total_params:,}")


    def make_tensors(model, src_words, tgt_words):
        # 모르는 단어는 <pad> (0)으로 처리
        src_ids = torch.tensor([[model.src_stoi.get(w, 0) for w in src_words]])
        tgt_ids = torch.tensor([[model.tgt_stoi['<s>']] +
                                [model.tgt_stoi.get(w, 0) for w in tgt_words] +
                                [model.tgt_stoi['<eos>']]])
        return src_ids, tgt_ids


    # ── 학습 루프 ──
    N_EPOCHS = 1000
    CHECKPOINT_PATH = "commit_bot_d32.pt"

    # 시작 시간 기록
    start_time = time.time()
    print(f"⏱️ 학습 시작 시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

    print(f"\n🧪 학습 전 번역 테스트 (처음 3개):")
    for src_words, _ in train_data[:3]:
        print(f"  {src_words} → {model.translate(src_words)}")

    print(f"\n📚 {N_EPOCHS} 에폭 학습 시작...")
    for epoch in range(N_EPOCHS):
        total_loss = 0
        for src_words, tgt_words in train_data:
            src_ids, tgt_ids = make_tensors(model, src_words, tgt_words)
            total_loss += model.train_step(src_ids, tgt_ids)

        if epoch % 50 == 0 or epoch == N_EPOCHS - 1:
            avg_loss = total_loss / len(train_data)
            print(f"  Epoch {epoch:4d} | Avg Loss: {avg_loss:.6f}")

            # 중간 저장 (만약을 위해)
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': model.optimizer.state_dict(),
                'src_vocab': src_vocab,
                'tgt_vocab': tgt_vocab,
            }, CHECKPOINT_PATH)

    print(f"\n💾 모델 저장 완료: {CHECKPOINT_PATH}")

    # 종료 시간 기록
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"\n⏱️ 학습 종료 시간: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print(f"⏱️ 총 소요 시간: {elapsed / 60:.1f} 분 ({elapsed / 3600:.2f} 시간)")

    # ── 학습 후 평가 ──
    print("\n✅ 학습 후 번역 결과 (100건 샘플):")
    correct_count = 0
    sample = train_data[:100]  # 전체를 다 찍기엔 많으니 100개만
    for src_words, tgt_words in sample:
        pred = model.translate(src_words)
        correct = pred == tgt_words
        if correct:
            correct_count += 1
        # 틀린 것만 출력 (옵션)
        if not correct:
            print(f"  ❌ {src_words} → {pred} (정답: {tgt_words})")
    print(f"\n🎯 샘플 정확도: {correct_count}/{len(sample)} ({correct_count / len(sample) * 100:.1f}%)")

    # ── Teacher Forcing 진단 ──
    print("\n🔍 Teacher Forcing 평가 (처음 5개):")
    for src_words, tgt_words in train_data[:5]:
        tf_pred = model.eval_teacher_forcing(src_words, tgt_words)
        print(f"  {' '.join(src_words):20} → TF: {tf_pred}  (정답: {tgt_words})")
