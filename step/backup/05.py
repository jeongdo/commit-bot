# 05.py
import torch
import torch.nn as nn
import torch.optim as optim


class BabyBrain(nn.Module):
    def __init__(self):
        super().__init__()

        # 단어 사전 만들기 (한글 단어 → 인덱스)
        self.word_to_idx = {
            "추가": 0, "수정": 1, "삭제": 2,
            "버그": 3, "로그인": 4, "회원가입": 5
        }
        self.idx_to_word = {v: k for k, v in self.word_to_idx.items()}

        # 영어 후보 (정답 후보들)
        self.candidates = ["add", "insert", "fix", "modify",
                           "remove", "delete", "bug", "login", "signup", "register"]

        # 신경망: 입력(한글 단어 인덱스) → 출력(각 영어 후보의 점수)
        # 6개 한글 단어 → 10개 영어 후보
        # 내부적으로 가중치를 랜덤하게 초기화함
        # (보통 균등분포 또는 정규분포에서 작은 랜덤 값)
        # 그래서 학습전은 랜덤값이 매핑됨.
        # add: -0.091
        # insert: -0.131
        # fix: 0.578
        # modify: 0.409
        # remove: -0.072
        # delete: -0.556
        # bug: -0.201
        # login: 0.391
        # signup: 0.345
        # register: -0.485
        self.fc = nn.Linear(6, 10)  # 6차원 입력, 10차원 출력 / 6개의 숫자를 입력받아 → 10개의 숫자를 출력하는 단순한 계산기
        #  parameters : 70개의 파라미터 + 내부메서드 생성

        #  6: 우리가 아는 한글 단어 개수 (추가, 수정, 삭제, 버그, 로그인, 회원가입)
        # 10: 영어 후보 개수 (add, insert, fix, modify, remove, delete, bug, login, signup, register)

        # 손실함수와 옵티마이저
        self.criterion = nn.CrossEntropyLoss() # 정답과 비교해서 오차 계산, 처음에 당연히 틀림.
        self.optimizer = optim.SGD(self.parameters(), lr=0.1)

        #SGD : 확률적 경사하강법(간단하고 빠른 업데이트 방식)
        # self.parameters() : 기본적으로 존재하고 있는 값 또는 범위: 10개 (bias) + (6*10의 연결강도 : 모든 경우의 수의 인식 + 그 상태값 증감함)

        # lr = 0.01(작은 걸음) → 천천히, 안정적으로 감 → 오래 걸림, but 잘감
        # lr = 0.9(큰 걸음)→ 빨리 감 → 근데 절벽으로 뛰어내릴 수도 있음(발산)

        # Step-03과 똑같이 학습 기록용
        self.last_input = None
        self.last_output = None

    def _word_to_onehot(self, word):
        """단어를 원-핫 벡터로 변환 (예: '추가' → [1,0,0,0,0,0])"""
        tensor = torch.zeros(6)  # 6개 단어만큼 길이의 텐서 생성 (모두 0으로 채움)
        tensor[self.word_to_idx[word]] = 1.0 # 해당 단어 위치만 1로 바꿈
        # 하나만 1 이고, 나머지는 0인 벡터 (GPU 연산 가능 + 자동 미분 지원)
        # "리스트랑 비슷한데, GPU에서 빠르게 계산 가능한 자료형" + 신호전달
        # 미분은 계속 증감이 아니라 학습 후반은 그 증감이 점점 감소하는 형태로 이어지는 가중지 조절 연산.
        return tensor

    def think(self, sentence: str) -> str:
        """문장을 입력받아 영어로 변환"""
        words = sentence.strip().split()
        result_parts = []
        self.last_input = []
        self.last_output = []

        for w in words:
            if w not in self.word_to_idx:
                result_parts.append(w)  # 모르는 단어는 그대로
                continue

            # 1. 입력을 텐서로 변환
            input_tensor = self._word_to_onehot(w)
            self.last_input.append(input_tensor)

            # 2. 신경망 통과 (순전파)
            output = self.fc(input_tensor)  # 10개의 점수(로짓)가 나옴

            # 3. 가장 높은 점수의 후보 선택
            predicted_idx = torch.argmax(output).item()
            predicted_word = self.candidates[predicted_idx]

            result_parts.append(predicted_word)
            self.last_output.append(output)

        return ' '.join(result_parts)

    def learn(self, correct_sentence: str):
        """정답을 보고 학습 (역전파)"""
        correct_words = correct_sentence.strip().split()

        total_loss = 0
        self.optimizer.zero_grad()
        # ✅ 기울기 초기화: 원래는 매 스텝 초기화가 기본
        # 💡 한 번에 던져야 하는 큰 AI 연산(대배치)에서는 누적할 수도 있음

        # self.last_input = [추가_텐서]           # 마지막에 생각했던 입력 단어 (1개)
        # self.last_output = [add_출력]          # think()가 출력한 영어 후보 (1개)
        # correct_words = ["insert"]            # 정답 단어 (1개)
        for i, (input_tensor, output) in enumerate(zip(self.last_input, self.last_output)):
            # 정답 개수보다 많으면 나머지는 학습 안 함 (버림)
            if i >= len(correct_words):
                break

            # 정답의 인덱스 찾기
            correct_word = correct_words[i]
            if correct_word not in self.candidates:
                continue # 후보에 없으면 그냥 넘어감 (학습도 안 함, 패널티도 없음)

            # 정답 단어("insert")가 후보 목록에서 몇 번째인지 찾기
            # self.candidates = ["add", "insert", "fix", "remove", ...] 라고 가정
            target_idx = self.candidates.index(correct_word)  # "insert" → 1 (두 번째)
            # PyTorch 텐서로 변환 (신경망이 이해하는 숫자 형태)
            target = torch.tensor([target_idx])

            # 1. 먼저 예측 (순전파)
            # output = brain.think("추가")
            # output = [0.2, 0.7, 0.05, ...]

            # ↑ "insert"에 대한 점수 = 0.7

            # 2. 손실(loss) 계산
            # output: 모델이 예측한 점수들 (예: "add":0.2, "insert":0.7, "fix":0.05, ...)
            # target: 정답은 "insert" (1번 인덱스)
            #
            # CrossEntropyLoss가 하는 일:
            # 1. output 점수들을 확률로 변환 (softmax)
            # 2. 정답 위치(1번)의 확률이 높을수록 loss는 작아짐
            #    - 정답 확률 0.7 → loss 0.35 (작음)
            #    - 정답 확률 0.9 → loss 0.10 (더 작음)
            #    - 정답 확률 0.3 → loss 1.20 (큼)

            # 즉, loss는 정답 확률이 올라갈수록 내려감 (반비례)
            # 손실 계산 (기울기) :  doc/(딥러닝) 역전파의_본질.md

            loss = self.criterion(output.unsqueeze(0), target) # 정답은 더 정답답게, 오답은 더 오답답게" 만들어주는 도구다.
            total_loss += loss # loss 값이 점점 줄어드는 걸 보여주기 위해 계산

        # 역전파 (PyTorch가 자동으로 가중치 업데이트!)
        # 이 단 한 줄의 코드가 실행되는 순간,
        # PyTorch는 수식 (p_i - y_i)를 계산하여 각 Logit의 기울기를 구합니다.
        # logits.grad 안에는 [-0.4, 0.2, 0.2] 라는 값이 꽂히게 됩니다.
        total_loss.backward()

        # 위해서 구한 기울기를 가져다가
        # optimizer.step() 로 전달되어, 최종적으로 신경망의 가중치를 정답은 밀어 올리고 오답은 끌어내리는 방향으로 수정
        self.optimizer.step()

        return total_loss.item()

    def show_weights(self, word):
        """특정 단어의 가중치(점수) 보여주기"""
        if word not in self.word_to_idx:
            print(f"'{word}'는 모르는 단어입니다")
            return

        input_tensor = self._word_to_onehot(word)
        with torch.no_grad():
            scores = self.fc(input_tensor)

        print(f"\n'{word}'에 대한 각 후보 점수:")
        for i, candidate in enumerate(self.candidates):
            print(f"  {candidate:10} : {scores[i].item():.3f}")


# 실행 데모
if __name__ == "__main__":
    brain = BabyBrain()

    # print("=" * 50)
    print("🧠 PyTorch 아기 뇌 (Step-04)")
    # print("=" * 50)

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
