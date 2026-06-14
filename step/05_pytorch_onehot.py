import torch
import torch.nn as nn
import torch.optim as optim


class BabyBrain(nn.Module):
    def __init__(self):
        super().__init__()

        self.word_to_idx = {
            "추가": 0, "수정": 1, "삭제": 2,
            "버그": 3, "로그인": 4, "회원가입": 5
        }
        self.candidates = ["add", "insert", "fix", "modify",
                           "remove", "delete", "bug", "login", "signup", "register"]

        # [04와 차이] 수동 가중치 dict → PyTorch 신경망으로 대체
        # 6차원 one-hot 입력 → 10개 후보 점수 출력
        self.fc = nn.Linear(6, 10)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.parameters(), lr=0.1)

        self.last_input = []
        self.last_output = []

    def _word_to_onehot(self, word):
        # [핵심] 단어 → sparse 벡터 (예: '추가' → [1,0,0,0,0,0])
        tensor = torch.zeros(6)
        tensor[self.word_to_idx[word]] = 1.0
        return tensor

    def think(self, sentence: str) -> str:
        words = sentence.strip().split()
        result_parts = []
        self.last_input = []
        self.last_output = []

        for w in words:
            if w not in self.word_to_idx:
                result_parts.append(w)
                continue

            inp = self._word_to_onehot(w)
            out = self.fc(inp)  # 순전파
            result_parts.append(self.candidates[torch.argmax(out).item()])
            self.last_input.append(inp)
            self.last_output.append(out)

        return ' '.join(result_parts)

    def learn(self, correct_sentence: str):
        correct_words = correct_sentence.strip().split()
        total_loss = 0
        self.optimizer.zero_grad()

        for i, (inp, out) in enumerate(zip(self.last_input, self.last_output)):
            if i >= len(correct_words) or correct_words[i] not in self.candidates:
                continue
            target = torch.tensor([self.candidates.index(correct_words[i])])
            total_loss += self.criterion(out.unsqueeze(0), target)

        # [핵심] 수동 _adjust() 전체를 이 두 줄이 대체
        total_loss.backward()   # 기울기 자동 계산 (역전파)
        self.optimizer.step()   # 가중치 자동 업데이트
        return total_loss.item()

    def show_weights(self, word):
        if word not in self.word_to_idx:
            return
        inp = self._word_to_onehot(word)
        with torch.no_grad():
            scores = self.fc(inp)
        print(f"\n'{word}'에 대한 각 후보 점수:")
        for i, c in enumerate(self.candidates):
            print(f"  {c:10} : {scores[i].item():.3f}")


if __name__ == "__main__":
    brain = BabyBrain()
    print("🧠 PyTorch 신경망 (one-hot 입력)")

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
