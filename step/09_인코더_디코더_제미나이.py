import torch
import torch.nn as nn
import torch.optim as optim
import math


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
        seq_len = x.size(1)
        return x + self.pe[:, :seq_len, :]


class CommitBot(nn.Module):
    def __init__(self):
        super().__init__()

        self.pos_enc = PositionalEncoding(d_model=8, max_len=100)

        # [단어장 세팅]
        self.src_vocab = ['<pad>', '버그', '수정', '코드', '리팩토링']
        self.src_stoi = {w: i for i, w in enumerate(self.src_vocab)}

        self.tgt_vocab = ['<pad>', 'bug', 'fix', 'code', 'refactor']
        self.tgt_stoi = {w: i for i, w in enumerate(self.tgt_vocab)}

        # ----------------------------------------------------------------------
        # [1. 인코더 부품] (기존 동일)
        # 한국어(입력)를 8차원 벡터로 바꾸는 임베딩과 셀프 어텐션
        # ----------------------------------------------------------------------
        self.embedding = nn.Embedding(len(self.src_vocab), 8, padding_idx=0)
        self.encoder_attention = nn.MultiheadAttention(embed_dim=8, num_heads=2, batch_first=True)

        # ----------------------------------------------------------------------
        # [2. 디코더 부품] (✨ 신규 추가)
        # 영어(정답)를 다루기 위해 디코더 전용 임베딩과 어텐션 기계가 독립적으로 필요합니다.
        # ----------------------------------------------------------------------

        # 1) 디코더 전용 임베딩: 영어 단어장 크기(5)에 맞춰 8차원 공간을 새로 팝니다.
        self.tgt_embedding = nn.Embedding(len(self.tgt_vocab), 8, padding_idx=0)

        # 2) 디코더 셀프 어텐션: 번역된 영어 단어들끼리 문법적 호응(예: bug 다음에 fix가 오네?)을 파악하는 기계
        self.decoder_attention = nn.MultiheadAttention(embed_dim=8, num_heads=2, batch_first=True)

        # ----------------------------------------------------------------------
        # [3. 인코더-디코더 결합 (Cross-Attention)] (✨ 대망의 브릿지 추가)
        # 한국어 원문(인코더)과 현재까지 번역된 영어(디코더)를 융합하는 최종 믹서기입니다.
        # ----------------------------------------------------------------------
        self.cross_attention = nn.MultiheadAttention(embed_dim=8, num_heads=2, batch_first=True)

        # [4. 최종 점수판] 8차원 문맥을 5칸짜리 영어 단어장 점수로 뻥튀기 (기존 동일)
        self.fc = nn.Linear(8, len(self.tgt_vocab))
        self.criterion = nn.CrossEntropyLoss(ignore_index=0)
        self.optimizer = optim.Adam(self.parameters(), lr=0.05)

    # (순전파 단계)
    # 디코더가 추가되었으므로, 이제 시험을 치려면 '문제지(src_ids)' 뿐만 아니라
    # 현재까지 적은 '답안지(tgt_ids)'도 같이 인자로 받아야 합니다.
    def forward(self, src_ids, tgt_ids):
        # ==========================================
        # [Phase 1: 인코더 (Encoder)] - "문제 분석"
        # ==========================================
        # 1. 한국어 데이터 읽기 및 위치 융합
        src_emb = self.embedding(src_ids)
        src_emb = self.pos_enc(src_emb)

        # 2. 인코더 셀프 어텐션: [버그, 수정] 끼리 서로 바라보며 '한국어 문맥' 완성
        # Q, K, V 모두 src_emb(한국어)가 들어감
        enc_out, _ = self.encoder_attention(src_emb, src_emb, src_emb)
        # 결과물 enc_out Shape: [1, 2, 8] (배치 1, 단어 2개, 차원 8) -> 이게 한국어 요약본!

        # ==========================================
        # [Phase 2: 디코더 (Decoder)] - "답안 분석"
        # ==========================================
        # 1. 영어 데이터 읽기 및 위치 융합
        tgt_emb = self.tgt_embedding(tgt_ids)
        tgt_emb = self.pos_enc(tgt_emb)

        # 2. 디코더 셀프 어텐션: [bug, fix] 끼리 서로 바라보며 '영어 문법' 파악
        # (※ 실제 실무 모델에서는 미래 단어 커닝 방지용 Mask가 들어가지만, 여기선 장난감 뼈대이므로 생략)
        dec_out, _ = self.decoder_attention(tgt_emb, tgt_emb, tgt_emb)
        # 결과물 dec_out Shape: [1, 2, 8] -> 이게 영어 요약본!

        # ==========================================
        # [Phase 3: 크로스 어텐션 (Cross-Attention)] - "번역의 마법"
        # ==========================================
        # 여기가 트랜스포머의 꽃입니다. 데이터 출처가 서로 다릅니다!
        # Query(질문) : dec_out (디코더 / 영어) -> "나 지금 'bug' 번역했는데, 다음은 한국어 원문의 어디를 참고해야 해?"
        # Key(단서) : enc_out (인코더 / 한국어) -> "내 요약본을 봐, '수정' 이라는 단어 쪽에 가중치가 높아."
        # Value(내용) : enc_out (인코더 / 한국어) -> "'수정'의 8차원 핵심 의미(Value)를 디코더 너한테 넘겨줄게."

        # 내부 차원 연산 Q(영어) @ K(한국어)^T
        # [1, 2(영), 8] @ [1, 8, 2(한)] = [1, 2, 2] 크기의 어텐션 점수판이 생성됨!
        # 즉, 영어 단어 2개가 각각 한국어 단어 2개 중 어디에 눈길을 줄지 (확률) 결정.
        cross_out, cross_weights = self.cross_attention(query=dec_out, key=enc_out, value=enc_out)

        # cross_out은 마침내 한국어 문맥(V)과 영어 문맥(Q)이 완벽히 섞인 최종 8차원 텐서가 됩니다. Shape: [1, 2, 8]

        # ==========================================
        # [Phase 4: 출력층 (Output)] - "채점판 제출"
        # ==========================================
        # 혼종이 된 8차원 텐서를 5칸짜리 영어 단어장 크기로 쫙 펼침
        logits = self.fc(cross_out)  # Shape: [1, 2, 5]

        return logits, cross_weights

    def train_step(self, src_ids, tgt_ids):
        self.train()

        # 변경점: forward 파이프라인에 src_ids(문제지)와 tgt_ids(답안지)를 동시에 던짐
        logits, _ = self.forward(src_ids, tgt_ids)

        loss = self.criterion(logits.view(-1, len(self.tgt_vocab)), tgt_ids.view(-1))

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()


# ---------- 데이터 로드 및 빌드 런타임 ----------
bot = CommitBot()

train_data = [
    (['버그', '수정'], ['bug', 'fix']),
    (['코드', '수정'], ['code', 'refactor']),
    (['리팩토링', '코드'], ['refactor', 'code']),
]

print("\n📚 인코더+디코더 결합 완료! 300번 학습 시작...")

for epoch in range(300):
    total_loss = 0

    for src_words, tgt_words in train_data:

        # [단계 1] 한국어 단어를 숫자 ID로
        src_list = []
        for w in src_words:
            src_list.append(bot.src_stoi[w])
        src_ids = torch.tensor([src_list])

        # [단계 2] 영어 단어를 숫자 ID로
        tgt_list = []
        for w in tgt_words:
            tgt_list.append(bot.tgt_stoi[w])
        tgt_ids = torch.tensor([tgt_list])

        # [단계 3] 엔진룸 입장 (기존과 완벽히 동일한 루프)
        loss_value = bot.train_step(src_ids, tgt_ids)
        total_loss += loss_value

    if epoch % 60 == 0:
        print(f"  Epoch {epoch:3d} | Loss: {total_loss:.4f}")
