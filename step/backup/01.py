# amoeba_brain.py - 내 첫 AI의 시작
import random


class Brain:
    def __init__(self):
        # 뉴런 10개 만들기
        # random.random() : 0.0 ~ 1.0  사이의 랜덤한 실수(예: 0.473, 0.892, 0.124...)
        # for _ in range(10)  10번 반복해라
        # [...] 리스트로 만들어라
        self.weights = [random.random() for _ in range(10)]

    def think(self, korean_word):
        # 아주 단순한 사고
        simple_map = {
            "추가": "add",
            "수정": "fix",
            "삭제": "remove",
            "버그": "bug"
        }
        return simple_map.get(korean_word, korean_word)


brain = Brain()
print(brain.think("추가"))  # "add"
print(brain.think("버그"))  # "bug"