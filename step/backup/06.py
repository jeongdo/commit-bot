# 06.py
import torch
import torch.nn as nn
import torch.optim as optim


class BabyBrainWithEmbedding(nn.Module):
    def __init__(self):
        super().__init__()

        # 단어 사전 (한글 → 인덱스)
        self.word_to_idx = {
            "추가": 0, "수정": 1, "삭제": 2,
            "버그": 3, "로그인": 4, "회원가입": 5
        }
        self.idx_to_word = {v: k for k, v in self.word_to_idx.items()}

        # 영어 후보
        self.candidates = ["add", "insert", "fix", "modify",
                           "remove", "delete", "bug", "login", "signup", "register"]

        # def _word_to_onehot(self, word):
        #     """단어를 원-핫 벡터로 변환 (예: '추가' → [1,0,0,0,0,0])"""
        #     tensor = torch.zeros(6)  # 6개 단어만큼 길이의 텐서 생성 (모두 0으로 채움)
        #     tensor[self.word_to_idx[word]] = 1.0  # 해당 단어 위치만 1로 바꿈
        #     # 하나만 1 이고, 나머지는 0인 벡터 (GPU 연산 가능 + 자동 미분 지원)
        #     # "리스트랑 비슷한데, GPU에서 빠르게 계산 가능한 자료형" + 신호전달
        #     # 미분은 계속 증감이 아니라 학습 후반은 그 증감이 점점 감소하는 형태로 이어지는 가중지 조절 연산.
        #     return tensor

        # 변경된 부분: 임베딩 (6개 단어 → 8차원 벡터)

        # [
        #     [0.12, -0.45, ...],  # 단어0
        #     [1.33, 0.87, ...],  # 단어1
        #     ...
        # ]

        # 6×8 행렬이 생성됨.
        # 특별한 수학적 의미는 없고, 표현 공간의 크기(벡터 길이)를 정한 것뿐이다.
        # 예제에서는 단순화를 위해 8을 사용한 거고, 실제 모델에서는 256, 512, 768, 1024

        # 단어 1 만 개가 있다고 가정하면
        # 8 차원   -> 8 만개파라미터
        # 512 차원 -> 512 만개파라미터 파라미터

        # 원핫 인코딩의 한계: 단어가 10,000개라면 하나의 단어를 표현하기 위해 10,000차원의 벡터가 필요합니다(1개만 1, 나머지는 모두 0).
        # 이는 메모리 낭비가 매우 심하고, 벡터 간의 내적이 항상 0이 되어 단어 간의 의미적 유사성이나 관계를 전혀 학습할 수 없습니다.
        # nn.Embedding의 장점 (밀집 벡터): 단어의 개수와 상관없이 원하는 차원(예: 8, 256, 512)으로 크기를 고정할 수 있습니다.
        # 처음에는 무작위 값으로 채워져 있지만, 신경망이 학습(Backpropagation)을 진행하면서 의미가 비슷한 단어들은 벡터 공간 상에서 서로 가까운 위치로 이동하게 됩니다.
        # 수학적 관점에서의 팁내부적으로 nn.Embedding은 거대한 가중치 행렬 $W \in \mathbb{R}^{V \times D}$ (여기서 $V$는 단어 수, $D$는 차원 수)를 만드는 것입니다.
        # 특정 단어의 인덱스를 입력하면, 행렬 곱셈 연산 없이 단순히 행렬 $W$에서 해당 인덱스의 행(Row)을 쏙 빼오는 룩업 테이블(Lookup Table) 역할을 하기 때문에 연산 속도도 매우 빠릅니다.

        self.embedding = nn.Embedding(6, 8)  # _word_to_onehot 함수에서 변경됨.
        # 선형층: 8차원 입력 → 10개 후보
        # 선형 결합 레이어(Fully Connected Layer 또는 Dense Layer)
        self.fc = nn.Linear(8, 10)  # self.fc = nn.Linear(6, 10) 에서 변경됨

        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.parameters(), lr=0.1)

        self.last_input_indices = []  # 인덱스 저장 (텐서)
        self.last_output = []

    def _word_to_index(self, word):
        """단어를 인덱스 텐서로 변환"""
        return torch.tensor([self.word_to_idx[word]])

    def think(self, sentence: str) -> str:
        words = sentence.strip().split()
        result_parts = []
        self.last_input_indices = []
        self.last_output = []

        for w in words:
            if w not in self.word_to_idx:
                result_parts.append(w)
                continue

            idx = self._word_to_index(w)  # shape (1,)
            self.last_input_indices.append(idx)

            emb = self.embedding(idx)  # shape (1, 8)
            output = self.fc(emb)  # shape (1, 10)
            predicted_idx = torch.argmax(output).item()
            predicted_word = self.candidates[predicted_idx]

            result_parts.append(predicted_word)
            self.last_output.append(output)

        return ' '.join(result_parts)

    def learn(self, correct_sentence: str):
        correct_words = correct_sentence.strip().split()
        total_loss = 0
        self.optimizer.zero_grad()

        for i, (idx_tensor, output) in enumerate(zip(self.last_input_indices, self.last_output)):
            if i >= len(correct_words):
                break
            correct_word = correct_words[i]
            if correct_word not in self.candidates:
                continue
            target_idx = self.candidates.index(correct_word)
            target = torch.tensor([target_idx])

            loss = self.criterion(output, target)  # output shape (1,10), target (1,)
            total_loss += loss

        total_loss.backward()
        self.optimizer.step()
        return total_loss.item()

    def show_weights(self, word):
        if word not in self.word_to_idx:
            print(f"'{word}'는 모르는 단어입니다")
            return
        idx = self._word_to_index(word)
        with torch.no_grad():
            emb = self.embedding(idx)
            scores = self.fc(emb)
        print(f"\n'{word}'에 대한 각 후보 점수:")
        for i, c in enumerate(self.candidates):
            print(f"  {c:10} : {scores[0][i].item():.3f}")


if __name__ == "__main__":
    brain = BabyBrainWithEmbedding()
    print("🧠 Step 04 - 임베딩 버전 (Attention 없음)")
    print("\n=== 학습 전 ===")
    brain.show_weights("추가")
    print(f"\n🤔 생각한 결과: {brain.think('추가')}")

    print("\n=== 학습: '추가' → 'insert' 라고 알려줌 ===")
    for step in range(5):
        brain.think("추가")
        loss = brain.learn("insert")
        print(f"Step {step + 1}: loss = {loss:.4f}")

    print("\n=== 학습 후 ===")
    brain.show_weights("추가")
    print(f"\n🤔 생각한 결과: {brain.think('추가')}")
