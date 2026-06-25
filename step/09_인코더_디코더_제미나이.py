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
        # [1. 인코더] (기존 동일)
        # 한국어(입력)를 8차원 벡터로 바꾸는 임베딩과 셀프 어텐션
        # ----------------------------------------------------------------------
        self.embedding = nn.Embedding(len(self.src_vocab), 8, padding_idx=0)
        self.attention = nn.MultiheadAttention(embed_dim=8, num_heads=2, batch_first=True)

        # ----------------------------------------------------------------------
        # [2. 디코더 부품] (✨ 신규)
        # 영어(정답)를 다루기 위해 디코더 전용 임베딩과 어텐션 기계가 독립적으로 필요합니다.
        # ----------------------------------------------------------------------
        # 1) 디코더 전용 임베딩: 영어 단어장 크기(5)에 맞춰 8차원 공간을 새로 팝니다.
        self.tgt_embedding = nn.Embedding(len(self.tgt_vocab), 8, padding_idx=0)
        # 2) 디코더 셀프 어텐션: 번역된 영어 단어들끼리 문법적 호응(예: bug 다음에 fix가 오네?)을 파악하는 기계
        self.decoder_attention = nn.MultiheadAttention(embed_dim=8, num_heads=2, batch_first=True)

        # ----------------------------------------------------------------------
        # [3. 인코더-디코더 결합 (Cross-Attention)]
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

        # 1. 인코더 내부: [5 × 8]의 유지
        # 입력 문장이 5단어(['코드', '리팩토링', '후', '버그', '수정'])이고 임베딩 차원이 8차원이라면, N개의 인코더 층을 전부 다 통과하고 나온 최종 출력물(Memory 또는 Encoder_Out)의 크기는 [5 × 8]로 고정되어 있습니다.
        # 팩트: 10,000개 단어장이 있다고 해서 여기서 10000 × 8이 되지 않습니다. 단어 5개는 끝까지 5개입니다.
        # 상태: 이 [5 × 8] 텐서 내부의 실수(Float) 값들은 초기 임베딩 값과 완전히 달라져 있습니다. 셀프 어텐션을 거치며 5개 단어 간의 상관관계(문맥) 연산 결과가 벡터 안에 전부 합산된 상태입니다.

        # 2. 점수판 뻥튀기 (Linear Layer): [5 × 10,000]으로 확장
        # 개발자님이 언급하신 10000은 어텐션이 모두 끝난 후, 맨 마지막 출력층(분류기)에서 등장합니다. 이 [5 × 8] 텐서를 전체 10,000개 단어 중 어느 것이 정답인지 맞추는 확률판으로 변환해야 합니다.
        # 연산: [5 × 8] 텐서를 nn.Linear(8, 10000) 가중치 행렬과 곱합니다.
        # 결과 텐서: [5 × 10000] (Logits)
        # 의미: 5개의 각 단어 위치마다 10,000개의 객관식 보기에 대한 점수가 매겨진 거대한 행렬이 탄생합니다.

        # 3. 오차 계산 및 역전파 (Backward Pass)
        # 방금 만든 [5 × 10000] 점수판과 실제 정답 텐서(예: 5개 단어의 정답 ID)를 CrossEntropyLoss로 대조하여 오차(Loss) 값을 뽑아냅니다.
        # loss.backward()가 호출되면, 이 오차의 기울기(Gradient)가 최상단 선형 레이어부터 시작해서 트랜스포머 엔진룸을 거꾸로 타고 내려옵니다.

        # 4. 종착지: 임베딩 텐서 업데이트
        # 개발자님이 "기존 단어 벡터에 넣는다"라고 짚으신 부분이 바로 역전파의 가장 밑바닥, nn.Embedding 계층의 업데이트입니다.
        # 기울기가 맨 밑의 임베딩 층까지 도달하면, optimizer.step() 연산을 통해 마스터 사전에 있는 '버그', '수정'의 초기 8차원 좌표(Float 실수 배열) 자체가 미세하게 이동(수정)됩니다.
        # 결과: 다음에 똑같은 단어가 입력될 때는 예전의 바보 같던 좌표가 아니라, 오차를 줄이도록 한 걸음 최적화된 새로운 8차원 벡터에서 출발하게 되는 것입니다.

        # 문맥 파악 (Attention)     : [입력 단어 수 × 입력 단어 수]    -> 5개면 [5 × 5], 1만 개면 [10000 × 10000]
        # 최종 정답 고르기 (Linear)  : [입력 단어 수 × 전체 단어장 크기] -> 5개면 [5 × 10000]

        # 어탠션 : 입력 단어 사이의 연관도 를 가중치로 계산한 다음,  총 1000 개 단어 중 현재 문장의 5개의 단어만 정답을 예상하여, 이 5섯 단어의 예상 결과를 던진다.
        # 실제 정답이랑 맞추고 다시 역전파

        # 5. 연관도 계산 (Encoder 내부 연산)
        #    목적: 현재 들어온 5개 단어(한국어) 사이의 문맥 파악
        #    실제 연산: 입력된 5개 단어끼리 $Q$와 $K$를 곱해 [5 × 5] 크기의 어텐션 점수판을 만듭니다.
        #    이 비율대로 데이터를 섞어 [5 × 8] (5개 단어, 8차원) 크기의 최종 문맥 텐서를 뽑아냅니다.
        # 6. 정답 예상 (Linear 출력층)
        #    목적: 압축된 텐서를 바탕으로 실제 정답(단어)을 예측
        #    실제 연산: 인코더/디코더를 빠져나온 [5 × 8] 텐서를 [8 × 1000] 크기의 출력 가중치 행렬과 곱합니다.
        #    결과물: [5 × 1000] 크기의 최종 예측 점수판(Logits). 즉, 5개의 위치 각각에 대해 1,000개의 단어 중 무엇이 정답일지 예측한 확률 표가 나옵니다.
        # 7. 대조 및 역전파 (Loss & Backward)
        #    목적: 오차 수정
        #    실제 연산: 방금 만든 [5 × 1000] 예측 점수판을 실제 정답 ID 5개([5])와 1:1로 대조하여 오차(Loss)를 구합니다.
        #    마무리: loss.backward()가 실행되면, 이 오차 미분값이 [5 × 1000] 끄트머리에서부터 역주행하여 맨 앞의 입력 벡터 좌표까지 싹 다 업데이트합니다.

        src_emb = self.embedding(src_ids)
        src_emb = self.pos_enc(src_emb)

        # 2. 인코더 셀프 어텐션: [버그, 수정] 끼리 서로 바라보며 '한국어 문맥' 완성
        # Q, K, V 모두 src_emb(한국어)가 들어감
        enc_out, _ = self.attention(src_emb, src_emb, src_emb)
        # 결과물 enc_out Shape: [1, 2, 8] (배치 1, 단어 2개, 차원 8) -> 이게 한국어 요약본!

        # ==========================================
        # [Phase 2: 디코더 (Decoder)] - "답안 분석"
        # ==========================================

        # 인코더가 들어온 한국어 원본 문맥을 싹 다 파악해서 요약본(Memory)을 만들어주면,
        # 디코더는 그 요약본을 바탕으로 영어 문맥을 파악하며 단어를 하나씩 조립하는 기계입니다.
        #
        # 디코더의 역할을 가장 단순한 2단계 팩트로 쪼개면 이렇습니다.
        #
        # 1. 내가 쓴 영어 문맥 파악 (Self-Attention)
        # 상황: 디코더가 방금 전까지 fix라는 영어 단어를 뱉어냈습니다.
        # 생각: "음, 내가 방금 fix(동사)를 썼으니까, 문법적으로 다음엔 명사가 올 차례군."
        # 팩트: 자기가 지금까지 생성한 타겟 단어(영어)들끼리만 연관도를 계산합니다.
        #
        # 2. 한국어 원본 참조 (Cross-Attention)
        # 상황: 명사를 써야 하는 건 알겠는데, 어떤 명사를 써야 할지 결정해야 합니다.
        # 생각: "아까 인코더가 넘겨준 한국어 요약본(Memory) 좀 볼까? 아, 원본 단어가 '버그'였네! 그럼 bug를 써야겠다."
        # 팩트: 디코더의 상태(Q)를 가지고 인코더의 데이터(K, V)를 검색해서 가져옵니다.



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
