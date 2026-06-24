import torch
import torch.nn as nn
import torch.optim as optim
import math

# =====================================================================
# [공통] Positional Encoding
# =====================================================================
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=100):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.pe = pe.unsqueeze(0)

    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]

# =====================================================================
# [최종 단계] 실무형 Seq2Seq 트랜스포머
# =====================================================================
class ProductionSeq2Seq(nn.Module):
    def __init__(self, src_vocab, tgt_vocab, d_model=16, nhead=2, num_layers=2):
        super().__init__()
        self.src_stoi = {w: i for i, w in enumerate(src_vocab)}
        self.tgt_stoi = {w: i for i, w in enumerate(tgt_vocab)}
        self.tgt_itos = {i: w for i, w in enumerate(tgt_vocab)}

        # 1. 임베딩 및 위치 인코딩
        self.src_emb = nn.Embedding(len(src_vocab), d_model, padding_idx=0)
        self.tgt_emb = nn.Embedding(len(tgt_vocab), d_model, padding_idx=0)
        self.pos_enc = PositionalEncoding(d_model)

        # 2. 파이토치 빌트인 트랜스포머 엔진
        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_layers,
            num_decoder_layers=num_layers,
            batch_first=True
        )

        # 3. 최종 출력층
        self.fc_out = nn.Linear(d_model, len(tgt_vocab))

        # 4. 채점기
        self.criterion = nn.CrossEntropyLoss(ignore_index=0)

        # 💡 [LR 스케줄러 1] 옵티마이저 초기 학습률을 살짝 높게(0.001) 잡습니다.
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)

        # 💡 [LR 스케줄러 2] StepLR: 100 에포크마다 학습률을 절반(0.5)으로 깎아냅니다.
        # 초반에는 성큼성큼 걷고(탐색), 후반에는 보폭을 줄여 최적점에 안정적으로 안착(수렴)하게 합니다.
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=100, gamma=0.5)

    def forward(self, src_ids, tgt_ids):
        # Boolean 마스크: <pad>(0)인 위치를 True로 만들어 연산에서 제외
        src_key_padding_mask = (src_ids == 0)

        # 💡 [배치 마스킹 대비]
        # 실무에서 Dataloader를 쓰면 <eos> 이후의 남는 공간은 전부 <pad>(0)로 채워집니다(Force Padding).
        # 따라서 여기서 (tgt_ids == 0)을 해주면 자연스럽게 <eos> 이후의 더미 데이터들이 모두 차단됩니다.
        tgt_key_padding_mask = (tgt_ids == 0)

        # 미래 커닝 방지 대각선 마스크
        tgt_mask = self.transformer.generate_square_subsequent_mask(tgt_ids.size(1)).to(src_ids.device)

        src_emb = self.pos_enc(self.src_emb(src_ids))
        tgt_emb = self.pos_enc(self.tgt_emb(tgt_ids))

        out = self.transformer(
            src=src_emb,
            tgt=tgt_emb,
            src_key_padding_mask=src_key_padding_mask,
            tgt_key_padding_mask=tgt_key_padding_mask,
            memory_key_padding_mask=src_key_padding_mask,
            tgt_mask=tgt_mask
        )

        return self.fc_out(out)

    def train_step(self, src_ids, tgt_ids):
        self.train()

        tgt_in = tgt_ids[:, :-1]   # <s> ...
        tgt_out = tgt_ids[:, 1:]   # ... <eos>

        logits = self.forward(src_ids, tgt_in)
        loss = self.criterion(logits.view(-1, logits.size(-1)), tgt_out.reshape(-1))

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0) # 기울기 폭발 방지
        self.optimizer.step()

        return loss.item()

    def translate(self, src_words, max_len=10):
        self.eval()

        # 💡 [OOV 방어 1] 사전에 없는 단어면 에러를 뿜는 대신 '<unk>' 토큰으로 치환하여 유연하게 대처합니다.
        unk_idx = self.src_stoi.get('<unk>', 0)  # <unk>가 없으면 <pad>(0)으로 fallback
        src_ids = torch.tensor([[self.src_stoi.get(w, unk_idx) for w in src_words]])

        src_key_padding_mask = (src_ids == 0)
        src_emb = self.pos_enc(self.src_emb(src_ids))

        # 인코더 실행 -> memory 추출
        memory = self.transformer.encoder(src_emb, src_key_padding_mask=src_key_padding_mask)

        # 디코더 초기 입력 <s> 장전
        tgt_ids = torch.tensor([[self.tgt_stoi['<s>']]])

        for _ in range(max_len):
            tgt_emb = self.pos_enc(self.tgt_emb(tgt_ids))
            tgt_mask = self.transformer.generate_square_subsequent_mask(tgt_ids.size(1)).to(src_ids.device)

            with torch.no_grad():
                out = self.transformer.decoder(
                    tgt=tgt_emb,
                    memory=memory,
                    tgt_mask=tgt_mask,
                    memory_key_padding_mask=src_key_padding_mask
                )
                logits = self.fc_out(out)

            next_id = logits[:, -1, :].argmax(dim=-1, keepdim=True)

            if next_id.item() == self.tgt_stoi.get('<eos>', -1):
                break

            tgt_ids = torch.cat([tgt_ids, next_id], dim=1)

        result_ids = tgt_ids[0, 1:].tolist()
        eos_id = self.tgt_stoi.get('<eos>', -1)
        return [self.tgt_itos[i] for i in result_ids if i not in (0, eos_id)]


# =====================================================================
# [실행부] 데이터 로드 및 런타임 테스트
# =====================================================================
if __name__ == "__main__":
    train_data = [
        (['버그', '수정'],              ['fix', 'bug']),
        (['코드', '수정'],              ['refactor', 'code']),
        (['리팩토링', '코드'],          ['refactor', 'code']),
        (['기능', '추가'],              ['add', 'feature']),
        (['로그인', '오류', '수정'],    ['fix', 'login', 'error']),
        (['회원가입', '버그', '수정'],  ['fix', 'signup', 'bug']),
        (['오류', '수정'],              ['fix', 'error']),
        (['코드', '리팩토링'],          ['refactor', 'code']),
    ]

    src_words_all = {w for src, _ in train_data for w in src}
    tgt_words_all = {w for _, tgt in train_data for w in tgt}

    # 💡 [수정됨] tgt_vocab에 tgt_words_all을 포함시켜 실제 번역 단어를 예측 가능하게 함
    src_vocab = ['<pad>', '<unk>'] + sorted(src_words_all)
    tgt_vocab = ['<pad>', '<unk>'] + sorted(tgt_words_all) + ['<s>', '<eos>']

    print(f"📖 입력 사전 ({len(src_vocab)}): {src_vocab}")
    print(f"📖 출력 사전 ({len(tgt_vocab)}): {tgt_vocab}")

    # 모델 생성
    model = ProductionSeq2Seq(src_vocab, tgt_vocab, d_model=16, nhead=2, num_layers=2)

    def make_tensors(model, src_words, tgt_words):
        # 💡 [OOV 방어 3] 학습 데이터 전처리 시에도 방어 로직 적용
        src_unk = model.src_stoi.get('<unk>', 0)
        tgt_unk = model.tgt_stoi.get('<unk>', 0)

        src_ids = torch.tensor([[model.src_stoi.get(w, src_unk) for w in src_words]])
        tgt_ids = torch.tensor([[model.tgt_stoi['<s>']] +
                                 [model.tgt_stoi.get(w, tgt_unk) for w in tgt_words] +
                                 [model.tgt_stoi['<eos>']]])
        return src_ids, tgt_ids

    print("\n📚 500 에포크 실무형 엔진 학습 시작...")
    for epoch in range(1, 501):
        total_loss = 0
        for src_words, tgt_words in train_data:
            src_ids, tgt_ids = make_tensors(model, src_words, tgt_words)
            total_loss += model.train_step(src_ids, tgt_ids)

        # 💡 [LR 스케줄러 3] 1 에포크가 끝날 때마다 스케줄러를 한 발짝 진행시킵니다.
        model.scheduler.step()

        if epoch % 100 == 0:
            current_lr = model.optimizer.param_groups[0]['lr']
            print(f"  Epoch {epoch:3d} | Loss: {total_loss:.4f} | Current LR: {current_lr:.6f}")

    print("\n✅ 학습 완료! 정상 번역 테스트:")
    for src_words, tgt_words in train_data[:3]:
        pred = model.translate(src_words)
        print(f"  원본: {src_words}  →  번역: {pred} (정답: {tgt_words})")

    print("\n🚨 OOV(모르는 단어) 방어 테스트:")
    # '결제', '완료'는 학습 데이터에 없는 단어(OOV)입니다. 에러 없이 <unk>로 치환되어 처리됩니다.
    oov_test = ['결제', '오류', '완료']
    pred_oov = model.translate(oov_test)
    print(f"  모르는 단어 입력: {oov_test}  →  번역(에러 안 남): {pred_oov}")