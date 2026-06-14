import torch
import torch.nn as nn
import torch.optim as optim
import math

# -------------------------------
# 1. Positional Encoding
# -------------------------------
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

    def forward(self, src_ids):
        emb = self.embedding(src_ids)
        emb = self.pos_enc(emb)
        memory, _ = self.self_attn(emb, emb, emb)
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

    def forward(self, tgt_ids, memory, tgt_mask=None):
        emb = self.embedding(tgt_ids)
        emb = self.pos_enc(emb)
        self_out, _ = self.self_attn(emb, emb, emb, attn_mask=tgt_mask)
        cross_out, _ = self.cross_attn(self_out, memory, memory)
        logits = self.fc(cross_out)
        return logits


# -------------------------------
# 4. Seq2Seq Transformer
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
        self.optimizer = optim.Adam(self.parameters(), lr=0.05)

    def generate_mask(self, sz):
        mask = torch.triu(torch.ones(sz, sz) * float('-inf'), diagonal=1)
        return mask

    def forward(self, src_ids, tgt_ids):
        memory = self.encoder(src_ids)
        tgt_mask = self.generate_mask(tgt_ids.size(1)).to(src_ids.device)
        logits = self.decoder(tgt_ids, memory, tgt_mask)
        return logits

    def train_step(self, src_ids, tgt_ids):
        self.train()
        logits = self.forward(src_ids, tgt_ids[:, :-1])
        loss = self.criterion(logits.view(-1, logits.size(-1)), tgt_ids[:, 1:].reshape(-1))
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def translate(self, src_words, max_len=10):
        self.eval()
        src_ids = torch.tensor([[self.src_stoi[w] for w in src_words]])
        memory = self.encoder(src_ids)
        tgt_ids = torch.tensor([[self.tgt_stoi['<s>']]])

        for _ in range(max_len):
            tgt_mask = self.generate_mask(tgt_ids.size(1))
            with torch.no_grad():
                logits = self.decoder(tgt_ids, memory, tgt_mask)
            next_id = logits[:, -1, :].argmax(dim=-1, keepdim=True)
            if next_id.item() == self.tgt_stoi['<eos>']:
                break
            tgt_ids = torch.cat([tgt_ids, next_id], dim=1)

        result_ids = tgt_ids[0, 1:].tolist()
        return [self.tgt_itos[i] for i in result_ids if i not in [0, self.tgt_stoi['<eos>']]]


# -------------------------------
# 5. 학습 데이터 & 실행
# -------------------------------
if __name__ == "__main__":
    # 학습 데이터 먼저 정의
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

    # ✅ vocab을 학습 데이터에서 자동 추출
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

    print("\n🧪 학습 전 번역 테스트 (처음 3개):")
    for src_words, _ in train_data[:3]:
        print(f"  {src_words} → {model.translate(src_words)}")

    print("\n📚 1000 에폭 학습 시작...")
    for epoch in range(1000):
        total_loss = 0
        for src_words, tgt_words in train_data:
            src_ids, tgt_ids = make_tensors(model, src_words, tgt_words)
            total_loss += model.train_step(src_ids, tgt_ids)
        if epoch % 1000 == 0:
            print(f"  Epoch {epoch:5d} | Loss: {total_loss:.4f}")

    print("\n✅ 학습 후 번역 결과:")
    correct_count = 0
    for src_words, tgt_words in train_data:
        pred = model.translate(src_words)
        correct = pred == tgt_words
        if correct:
            correct_count += 1
        print(f"  {src_words} → {pred} {'✅' if correct else '❌'} (정답: {tgt_words})")

    print(f"\n🎯 정확도: {correct_count}/{len(train_data)} ({correct_count/len(train_data)*100:.1f}%)")