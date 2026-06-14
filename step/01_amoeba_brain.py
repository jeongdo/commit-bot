import random


class Brain:
    def __init__(self):
        self.weights = [random.random() for _ in range(10)]

    # [핵심] 고정 dict 매핑 → 학습 없음, 항상 같은 결과
    def think(self, korean_word):
        simple_map = {
            "추가": "add",
            "수정": "fix",
            "삭제": "remove",
            "버그": "bug"
        }
        return simple_map.get(korean_word, korean_word)


brain = Brain()
print(brain.think("추가"))
print(brain.think("버그"))
