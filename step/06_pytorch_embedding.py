import torch
import torch.nn as nn
import torch.optim as optim


class BabyBrainWithEmbedding(nn.Module):
    def __init__(self):
        super().__init__()

        self.word_to_idx = {
            "추가": 0, "수정": 1, "삭제": 2,
            "버그": 3, "로그인": 4, "회원가입": 5
        }
        self.candidates = ["add", "insert", "fix", "modify",
                           "remove", "delete", "bug", "login", "signup", "register"]

        # [05와 차이 1] _word_to_onehot() 삭제 → nn.Embedding으로 대체
        # one-hot: 단어 수만큼 차원 필요 (sparse), 단어 간 유사도 학습 불가
        # embedding: 차원 고정 (dense), 학습하면서 유사 단어가 가까워짐
        self.embedding = nn.Embedding(6, 8)   # 6개 단어 → 8차원 밀집 벡터

        # [05와 차이 2] Linear 입력 차원 6 → 8 (embedding 출력에 맞춤)
        self.fc = nn.Linear(8, 10)            # (05) nn.Linear(6, 10) 에서 변경

        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.parameters(), lr=0.1)
        self.last_input_indices = []
        self.last_output = []

    def _word_to_index(self, word):
        # [핵심] onehot 벡터 대신 단순 인덱스만 넘김 → embedding이 알아서 벡터 lookup
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

            idx = self._word_to_index(w)
            emb = self.embedding(idx)   # 인덱스 → 8차원 벡터 (lookup)
            out = self.fc(emb)          # 8차원 → 10개 점수
            result_parts.append(self.candidates[torch.argmax(out).item()])
            self.last_input_indices.append(idx)
            self.last_output.append(out)

        return ' '.join(result_parts)

    def learn(self, correct_sentence: str):
        correct_words = correct_sentence.strip().split()
        total_loss = 0
        self.optimizer.zero_grad()

        for i, (idx, out) in enumerate(zip(self.last_input_indices, self.last_output)):
            if i >= len(correct_words) or correct_words[i] not in self.candidates:
                continue
            target = torch.tensor([self.candidates.index(correct_words[i])])
            total_loss += self.criterion(out, target)

        total_loss.backward()
        self.optimizer.step()
        return total_loss.item()

    def show_weights(self, word):
        if word not in self.word_to_idx:
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
    print("🧠 PyTorch 임베딩 버전")

    print("\n=== 학습 전 ===")
    brain.show_weights("추가")
    print(f"\n🤔 생각한 결과: {brain.think('추가')}")

    print("\n=== 학습: '추가' → 'insert' ===")
    for step in range(5):
        brain.think("추가")
        loss = brain.learn("insert")
        print(f"Step {step + 1}: loss = {loss:.4f}")

    print("\n=== 학습 후 ===")
    brain.show_weights("추가")
    print(f"\n🤔 생각한 결과: {brain.think('추가')}")
