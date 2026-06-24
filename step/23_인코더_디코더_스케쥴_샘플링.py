import torch
import torch.nn as nn
import torch.optim as optim
import math


# -------------------------------
# [공통] Positional Encoding
# -------------------------------
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=100):
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
# 2. 인코더 (Encoder)
# -------------------------------
class Encoder(nn.Module):
    def __init__(self, src_vocab_size, d_model=8, nhead=2):
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
    def __init__(self, tgt_vocab_size, d_model=8, nhead=2):
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
# 4. 완성된 Seq2Seq Transformer
# -------------------------------
class Seq2SeqTransformer(nn.Module):
    def __init__(self, src_vocab, tgt_vocab, d_model=8, nhead=2):
        super().__init__()
        self.src_stoi = {w: i for i, w in enumerate(src_vocab)}
        self.tgt_stoi = {w: i for i, w in enumerate(tgt_vocab)}
        self.tgt_itos = {i: w for i, w in enumerate(tgt_vocab)}

        self.encoder = Encoder(len(src_vocab), d_model, nhead)
        self.decoder = Decoder(len(tgt_vocab), d_model, nhead)

        self.criterion = nn.CrossEntropyLoss(ignore_index=0)
        self.optimizer = optim.Adam(self.parameters(), lr=0.0002)

    def generate_mask(self, sz, device='cpu'):
        """미래를 가리는 상삼각 마스크. float형 (0: 허용, -inf: 차단)"""
        mask = torch.triu(torch.ones(sz, sz, device=device) * float('-inf'), diagonal=1)
        return mask

    def forward(self, src_ids, tgt_ids, src_pad_mask=None, tgt_pad_mask=None):
        memory = self.encoder(src_ids, src_pad_mask)
        tgt_mask = self.generate_mask(tgt_ids.size(1), src_ids.device)
        logits = self.decoder(tgt_ids, memory, tgt_mask, tgt_pad_mask, src_pad_mask)
        return logits

    # =====================================================================
    # 🔥 Scheduled Sampling 적용된 train_step
    # =====================================================================
    def train_step(self, src_ids, tgt_ids, teacher_forcing_ratio=0.7):
        """
        teacher_forcing_ratio: 정답을 사용할 확률 (1.0 = 기존 Teacher Forcing)
                               0.7이면 70%는 정답, 30%는 모델 자신의 예측을 다음 입력으로 사용
        """
        self.train()

        # [1] 패딩 마스크 생성 (float 타입)
        src_pad_mask = (src_ids == 0).float().masked_fill(src_ids == 0, float('-inf'))

        # [2] 인코더를 먼저 실행시켜 원본 문장의 문맥(memory)을 얻습니다.
        memory = self.encoder(src_ids, src_pad_mask)

        # [3] 디코더 입력 초기값: <s> 토큰 하나로 시작
        tgt_input = tgt_ids[:, :1]   # (batch, 1)
        tgt_out = tgt_ids[:, 1:]     # 정답 시퀀스 (첫 <s> 제외)

        total_loss = 0

        # [4] 각 타임스텝마다 한 단어씩 예측하며 손실을 누적합니다.
        for t in range(tgt_out.size(1)):
            # --- 마스크 생성 (현재까지 생성된 단어 기준) ---
            tgt_pad_mask = (tgt_input == 0).float().masked_fill(tgt_input == 0, float('-inf'))
            tgt_mask = self.generate_mask(tgt_input.size(1), src_ids.device)

            # --- 디코더 실행 (현재까지의 입력으로 다음 단어 예측) ---
            logits = self.decoder(tgt_input, memory, tgt_mask, tgt_pad_mask, src_pad_mask)

            # --- 마지막 위치의 예측 점수만 추출 ---
            next_logits = logits[:, -1, :]   # (batch, vocab_size)
            target = tgt_out[:, t]           # 현재 타임스텝의 정답 단어

            # --- 손실 누적 ---
            total_loss += self.criterion(next_logits, target)

            # =================================================================
            # 🔥🔥🔥 Scheduled Sampling 핵심 (여기가 그 유명한 '3번' 포인트!)
            # =================================================================
            # teacher_forcing_ratio 확률로 정답을 사용하고,
            # (1 - teacher_forcing_ratio) 확률로 모델이 예측한 단어를 사용합니다.
            if self.training and torch.rand(1).item() > teacher_forcing_ratio:
                # --- [추가 1] 모델이 예측한 단어를 다음 입력으로 사용 ---
                next_token = next_logits.argmax(dim=-1, keepdim=True)
            else:
                # --- [추가 2] 정답 단어를 다음 입력으로 사용 (기존 Teacher Forcing) ---
                next_token = target.unsqueeze(1)
            # =================================================================

            # --- [추가 3] 선택된 토큰을 기존 시퀀스 뒤에 연결하여 다음 스텝의 입력으로 만듦 ---
            tgt_input = torch.cat([tgt_input, next_token], dim=1)

        # [5] 평균 손실 계산
        avg_loss = total_loss / tgt_out.size(1)

        # [6] 역전파 및 가중치 업데이트
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
# 5. 학습 데이터 & 실행
# -------------------------------
if __name__ == "__main__":
    # 학습 데이터
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

    # 어휘 자동 생성
    src_words_all = {w for src, _ in train_data for w in src}
    tgt_words_all = {w for _, tgt in train_data for w in tgt}

    src_vocab = ['<pad>'] + sorted(src_words_all)
    tgt_vocab = ['<pad>'] + sorted(tgt_words_all) + ['<s>', '<eos>']

    print(f"📖 src_vocab ({len(src_vocab)}): {src_vocab}")
    print(f"📖 tgt_vocab ({len(tgt_vocab)}): {tgt_vocab}")

    model = Seq2SeqTransformer(src_vocab, tgt_vocab)

    def make_tensors(model, src_words, tgt_words):
        src_ids = torch.tensor([[model.src_stoi[w] for w in src_words]])
        tgt_ids = torch.tensor([[model.tgt_stoi['<s>']] +
                                 [model.tgt_stoi[w] for w in tgt_words] +
                                 [model.tgt_stoi['<eos>']]])
        return src_ids, tgt_ids

    # ===================== 학습 전 평가 =====================
    print("\n🧪 학습 전 번역 테스트 (처음 3개):")
    for src_words, _ in train_data[:3]:
        print(f"  {src_words} → {model.translate(src_words)}")

    # ===================== 학습 =====================
    print("\n📚 1000 에폭 학습 시작...")
    for epoch in range(1000):
        total_loss = 0
        for src_words, tgt_words in train_data:
            src_ids, tgt_ids = make_tensors(model, src_words, tgt_words)
            total_loss += model.train_step(src_ids, tgt_ids)
        if epoch % 200 == 0:
            print(f"  Epoch {epoch:5d} | Loss: {total_loss:.4f}")

    # ===================== 학습 후 평가 =====================
    print("\n✅ 학습 후 번역 결과:")
    correct_count = 0
    for src_words, tgt_words in train_data:
        pred = model.translate(src_words)
        correct = pred == tgt_words
        if correct:
            correct_count += 1
        print(f"  {src_words} → {pred} {'✅' if correct else '❌'} (정답: {tgt_words})")
    print(f"\n🎯 정확도: {correct_count}/{len(train_data)} ({correct_count/len(train_data)*100:.1f}%)")

    # ===================== Teacher Forcing 평가 =====================
    print("\n🔍 Teacher Forcing 평가 (처음 5개):")
    for src_words, tgt_words in train_data[:5]:
        tf_pred = model.eval_teacher_forcing(src_words, tgt_words)
        print(f"  {' '.join(src_words):15} → TF: {tf_pred}  (정답: {tgt_words})")