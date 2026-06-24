import torch
import torch.nn as nn
import torch.optim as optim
import math

# =====================================================================
# [공통 부품] Positional Encoding (위치 지문 생성기)
# =====================================================================
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=100):
        super().__init__()
        # max_len(100)은 문장의 최대 길이 버퍼입니다. (단어장 크기와 무관)
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)

        # 삼각함수 주파수 계산 (수학적 팩트: 차원이 깊어질수록 파동이 느려짐)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))

        # 짝수 방에는 sin, 홀수 방에는 cos 지문을 채워 넣습니다.
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        # [Batch, Seq_len, d_model] 규격에 맞추기 위해 차원 승격 (unsqueeze)
        self.pe = pe.unsqueeze(0)

    def forward(self, x):
        # 들어온 문장의 실제 길이(x.size(1))만큼만 메모리 뷰(View)를 열어서 더해줍니다. (비용 0원)
        return x + self.pe[:, :x.size(1), :]

# =====================================================================
# [메인 엔진] 실무형 Seq2Seq 트랜스포머 (2단계 SFT 챗봇 모델)
# =====================================================================
class ProductionSeq2Seq(nn.Module):
    def __init__(self, src_vocab, tgt_vocab, d_model=16, nhead=2, num_layers=2):
        super().__init__()

        # 단어 <-> ID 매핑 딕셔너리 (자바의 HashMap 역할)
        self.src_stoi = {w: i for i, w in enumerate(src_vocab)}
        self.tgt_stoi = {w: i for i, w in enumerate(tgt_vocab)}
        self.tgt_itos = {i: w for i, w in enumerate(tgt_vocab)}

        # 1. 임베딩 계층 (단어를 16차원 실수 벡터로 변환)
        # padding_idx=0: <pad> 토큰은 학습하지 않고 항상 0으로 유지합니다.
        self.src_emb = nn.Embedding(len(src_vocab), d_model, padding_idx=0)
        self.tgt_emb = nn.Embedding(len(tgt_vocab), d_model, padding_idx=0)

        # 2. 위치 인코더 (단어의 순서 정보를 벡터에 더함)
        self.pos_enc = PositionalEncoding(d_model)

        # 3. 파이토치 빌트인 트랜스포머 엔진 (어텐션, Add&Norm, FFN이 모두 포함된 블랙박스)
        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_layers,
            num_decoder_layers=num_layers,
            batch_first=True # 입력 텐서의 첫 번째 차원이 Batch임을 명시 [Batch, Seq, Feature]
        )

        # 4. 최종 출력층 (16차원을 전체 정답 단어장 크기로 뻥튀기하는 점수판)
        self.fc_out = nn.Linear(d_model, len(tgt_vocab))

        # 5. 채점기 (CrossEntropyLoss)
        # ignore_index=0: <pad> 토큰을 맞추는 것은 무의미하므로 채점에서 아예 제외시킵니다.
        self.criterion = nn.CrossEntropyLoss(ignore_index=0)

        # 6. 최적화 및 학습률 스케줄러 (Adam -> StepLR)
        # 초반에는 0.001의 큰 보폭으로 탐색하고, 100 에포크마다 보폭을 반(0.5)으로 줄여 미세조정합니다.
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=100, gamma=0.5)

    def forward(self, src_ids, tgt_ids):
        # ---------------------------------------------------------------------
        # [마스킹 1] 패딩 가림막 (Padding Mask)
        # 값이 0(<pad>)인 위치를 True로 체크하여, 어텐션 가중합에서 제외시킵니다.
        # ---------------------------------------------------------------------
        src_key_padding_mask = (src_ids == 0)
        tgt_key_padding_mask = (tgt_ids == 0)

        # ---------------------------------------------------------------------
        # [마스킹 2] 미래 커닝 방지 가림막 (Causal Mask)
        # 디코더가 현재 단어를 생성할 때, 뒤에 나올 단어를 훔쳐보지 못하게 우상단을 -inf로 덮습니다.
        # ---------------------------------------------------------------------
        tgt_mask = self.transformer.generate_square_subsequent_mask(tgt_ids.size(1)).to(src_ids.device)

        # 단어를 벡터로 바꾸고 위치 지문을 더합니다.
        src_emb = self.pos_enc(self.src_emb(src_ids))
        tgt_emb = self.pos_enc(self.tgt_emb(tgt_ids))

        # ---------------------------------------------------------------------
        # 엔진 구동 (순방향 전진)
        # memory_key_padding_mask: 디코더가 인코더 정보(Memory)를 참고할 때, 
        # 원본 문장의 <pad> 부분은 무시하도록 지시합니다.
        # ---------------------------------------------------------------------
        out = self.transformer(
            src=src_emb,
            tgt=tgt_emb,
            src_key_padding_mask=src_key_padding_mask,
            tgt_key_padding_mask=tgt_key_padding_mask,
            memory_key_padding_mask=src_key_padding_mask,
            tgt_mask=tgt_mask
        )

        # 16차원 출력물을 전체 단어장 크기(Vocab Size)의 점수판(Logits)으로 변환하여 반환
        return self.fc_out(out)

    def train_step(self, src_ids, tgt_ids):
        """1회 학습(에포크 내 1 스텝)을 수행하는 함수"""
        self.train() # 모델을 훈련 모드로 전환 (드롭아웃 등 활성화)

        # ---------------------------------------------------------------------
        # [핵심] 교사 강요 (Teacher Forcing) 데이터 분할
        # 정답이 [<s>, fix, bug, <eos>] 라면:
        # tgt_in  (입력용): [<s>, fix, bug] -> 디코더에게 제공할 힌트
        # tgt_out (채점용): [fix, bug, <eos>] -> 디코더가 맞춰야 할 정답
        # ---------------------------------------------------------------------
        tgt_in = tgt_ids[:, :-1]
        tgt_out = tgt_ids[:, 1:]

        # 순방향 전진: 점수판 획득
        logits = self.forward(src_ids, tgt_in)

        # 채점: 입체 배열(3D)을 평면(2D)으로 펴서 파이토치 채점기에 밀어 넣습니다.
        # logits: [배치 * 단어길이, 전체 단어장 크기]
        # tgt_out: [배치 * 단어길이]
        loss = self.criterion(logits.view(-1, logits.size(-1)), tgt_out.reshape(-1))

        # ---------------------------------------------------------------------
        # 역전파 및 나사 조이기 (Backpropagation & Update)
        # ---------------------------------------------------------------------
        self.optimizer.zero_grad() # 이전 기울기 캐시 청소
        loss.backward()            # 오차 미분 (점수판 -> 엔진 -> 임베딩까지 거꾸로)

        # [기울기 폭발 방지] 오차 미분값이 너무 크면 가중치가 우주로 날아가므로 최대 1.0으로 컷오프
        torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0)

        self.optimizer.step()      # 계산된 미분값을 바탕으로 실제 가중치 업데이트

        return loss.item()

    def translate(self, src_words, max_len=10):
        """실제 추론(채팅)을 수행하는 함수 - 한 글자씩 순차적으로 뱉어냅니다."""
        self.eval() # 평가 모드로 전환

        # [OOV 방어] 사전에 없는 단어가 들어오면 에러 대신 '<unk>' 토큰으로 우회
        unk_idx = self.src_stoi.get('<unk>', 0)
        src_ids = torch.tensor([[self.src_stoi.get(w, unk_idx) for w in src_words]])

        src_key_padding_mask = (src_ids == 0)
        src_emb = self.pos_enc(self.src_emb(src_ids))

        # ---------------------------------------------------------------------
        # [추론 1단계] 인코더 캐싱 (Memory 추출)
        # 입력 문장(질문)은 바뀌지 않으므로, 인코더는 단 한 번만 돌려서 문맥을 압축해 둡니다.
        # ---------------------------------------------------------------------
        with torch.no_grad():
            memory = self.transformer.encoder(src_emb, src_key_padding_mask=src_key_padding_mask)

        # 디코더의 첫 시작 단어는 무조건 '<s>' (Start of String)
        tgt_ids = torch.tensor([[self.tgt_stoi['<s>']]])

        # ---------------------------------------------------------------------
        # [추론 2단계] 디코더 순환 루프 (Auto-Regressive)
        # ---------------------------------------------------------------------
        for _ in range(max_len):
            tgt_emb = self.pos_enc(self.tgt_emb(tgt_ids))

            # 현재까지 만들어진 단어 길이에 맞춰 미래 커닝 방지 마스크를 매번 새로 생성
            tgt_mask = self.transformer.generate_square_subsequent_mask(tgt_ids.size(1)).to(src_ids.device)

            with torch.no_grad():
                # 디코더 실행: Q는 현재까지 만든 단어들(tgt_emb), K와 V는 아까 뽑아둔 memory!
                out = self.transformer.decoder(
                    tgt=tgt_emb,
                    memory=memory,
                    tgt_mask=tgt_mask,
                    memory_key_padding_mask=src_key_padding_mask
                )
                logits = self.fc_out(out) # 10,000개짜리 점수판 생성

            # 가장 마지막에 예측된 단어 자리(:, -1, :)에서 확률이 제일 높은 단어 1개의 ID를 추출
            next_id = logits[:, -1, :].argmax(dim=-1, keepdim=True)

            # 예측한 단어가 문장의 끝을 알리는 '<eos>' 라면 즉시 루프 탈출
            if next_id.item() == self.tgt_stoi.get('<eos>', -1):
                break

            # 아니면 현재까지 만든 문장 뒤에 방금 뽑은 단어를 이어 붙임 (cat)
            tgt_ids = torch.cat([tgt_ids, next_id], dim=1)

        # 최종 텐서에서 맨 앞의 '<s>' 토큰을 떼어내고, 사람이 읽을 수 있는 텍스트 리스트로 변환
        result_ids = tgt_ids[0, 1:].tolist()
        eos_id = self.tgt_stoi.get('<eos>', -1)
        return [self.tgt_itos[i] for i in result_ids if i not in (0, eos_id)]


# =====================================================================
# [실행부] 데이터 전처리 및 훈련/테스트 런타임
# =====================================================================
if __name__ == "__main__":
    # 2단계 SFT(지도 미세조정)를 위한 Q&A 데이터셋
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

    # 입력과 출력의 고유 단어들을 긁어모아 마스터 사전(Vocabulary) 구축
    src_words_all = {w for src, _ in train_data for w in src}
    tgt_words_all = {w for _, tgt in train_data for w in tgt}

    # 특수 토큰(<pad>, <unk>, <s>, <eos>)을 무조건 맨 앞에 고정 할당
    src_vocab = ['<pad>', '<unk>'] + sorted(src_words_all)
    tgt_vocab = ['<pad>', '<unk>', '<s>', '<eos>'] + sorted(tgt_words_all)

    print(f"📖 입력 사전 ({len(src_vocab)}): {src_vocab}")
    print(f"📖 출력 사전 ({len(tgt_vocab)}): {tgt_vocab}")

    # 모델 메모리 할당 (엔진 가동 준비)
    model = ProductionSeq2Seq(src_vocab, tgt_vocab, d_model=16, nhead=2, num_layers=2)

    def make_tensors(model, src_words, tgt_words):
        """텍스트 데이터를 파이토치가 읽을 수 있는 텐서로 포장하는 헬퍼 함수"""
        src_unk = model.src_stoi.get('<unk>', 0)
        tgt_unk = model.tgt_stoi.get('<unk>', 0)

        # 소스 데이터 포장
        src_ids = torch.tensor([[model.src_stoi.get(w, src_unk) for w in src_words]])

        # 타겟 데이터 포장 (정답 앞뒤로 <s> 와 <eos> 샌드위치 패킹)
        tgt_ids = torch.tensor([[model.tgt_stoi['<s>']] +
                                 [model.tgt_stoi.get(w, tgt_unk) for w in tgt_words] +
                                 [model.tgt_stoi['<eos>']]])
        return src_ids, tgt_ids

    # ---------------------------------------------------------------------
    # 본격적인 훈련 루프 시작 (500 에포크)
    # ---------------------------------------------------------------------
    print("\n📚 500 에포크 SFT 실무형 엔진 학습 시작...")
    for epoch in range(1, 501):
        total_loss = 0
        for src_words, tgt_words in train_data:
            src_ids, tgt_ids = make_tensors(model, src_words, tgt_words)
            total_loss += model.train_step(src_ids, tgt_ids)

        # 1 에포크가 끝날 때마다 학습률 스케줄러 카운트 증가
        model.scheduler.step()

        # 100 에포크마다 진행 상황 및 현재 적용 중인 학습률(LR) 출력
        if epoch % 100 == 0:
            current_lr = model.optimizer.param_groups[0]['lr']
            print(f"  Epoch {epoch:3d} | Loss: {total_loss:.4f} | Current LR: {current_lr:.6f}")

    # ---------------------------------------------------------------------
    # 테스트 검증 (Inference)
    # ---------------------------------------------------------------------
    print("\n✅ 학습 완료! 정상 번역(채팅) 테스트:")
    for src_words, tgt_words in train_data[:3]:
        pred = model.translate(src_words)
        print(f"  사용자: {src_words}  →  봇: {pred} (정답: {tgt_words})")

    print("\n🚨 OOV(모르는 단어) 방어 테스트:")
    # '결제', '완료'는 학습 데이터에 한 번도 등장하지 않은 단어입니다.
    # 에러가 터지지 않고 내부적으로 <unk>로 치환되어 모델이 유연하게 넘깁니다.
    oov_test = ['결제', '오류', '완료']
    pred_oov = model.translate(oov_test)
    print(f"  모르는 단어 입력: {oov_test}  →  봇(에러 없이 처리): {pred_oov}")