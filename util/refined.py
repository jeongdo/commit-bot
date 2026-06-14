import json
import os
import random
from collections import defaultdict

current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root -> .../프로젝트폴더
project_root = os.path.dirname(current_dir)

# 파이참 프로젝트 루트 기준 경로 설정
input_file_path = os.path.join(project_root, "data", "commit_dataset_50000.jsonl")
output_file_path = os.path.join(project_root, "data", "commit_dataset_10000_refined.jsonl")

# 저장할 data 폴더가 존재하지 않으면 자동으로 생성하는 코드 추가
output_dir = os.path.dirname(output_file_path)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 정제에 필요한 변수들
unique_data = defaultdict(list)
seen_src = set()
seen_translation = set()

print(f"1단계: '{input_file_path}' 데이터 읽기 및 노이즈 필터링 시작...")

try:
    with open(input_file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                item = json.loads(line.strip())

                src = item.get("src", "").strip()
                translation = item.get("translation", "").strip()
                category = item.get("category", "").strip()
                action = item.get("action", [])

                # [노이즈 필터] 빈 값이나 너무 짧은 비정상 데이터 제거
                if not src or len(src) < 2 or not translation or not category or not action:
                    continue

                # [중복 제거] 의미 없는 중복 커밋 및 번역 패턴 원천 차단
                if src in seen_src or translation in seen_translation:
                    continue

                seen_src.add(src)
                seen_translation.add(translation)

                # 카테고리별로 데이터를 분류하여 저장
                unique_data[category].append(item)

            except json.JSONDecodeError:
                continue
except FileNotFoundError:
    print(f"❌ 에러: '{input_file_path}' 파일을 찾을 수 없습니다.")
    print("파이참 왼쪽 프로젝트 창에서 data 폴더 안에 파일이 올바르게 들어있는지 확인해주세요.")
    exit()

# 2단계: 분포를 보존하는 계층적 샘플링 (Stratified Sampling)
target_total = 10000
total_available = sum(len(items) for items in unique_data.values())

print(f"\n중복 제거 후 남은 고품질 데이터 수: {total_available}개")
print("2단계: 데이터 분포 정렬 및 1만 건 균형 샘플링 시작...")

refined_dataset = []

if total_available <= target_total:
    # 데이터가 부족하면 정제된 전체 데이터 사용
    for items in unique_data.values():
        refined_dataset.extend(items)
else:
    # 결과 재현성을 위해 랜덤 시드 고정
    random.seed(42)

    # 각 카테고리(feat, fix 등)의 원본 비율을 유지하며 1만 건 분할 추출
    for category, items in unique_data.items():
        proportion = len(items) / total_available
        category_target = int(target_total * proportion)

        # 해당 카테고리 내부에서 무작위 샘플링
        sampled_items = random.sample(items, min(len(items), category_target))
        refined_dataset.extend(sampled_items)

    # 소수점 연산 오차로 인해 10,000건에 미달할 경우 부족한 만큼 무작위 보충
    if len(refined_dataset) < target_total:
        remaining_target = target_total - len(refined_dataset)
        all_remaining_items = [
            item for items in unique_data.values() for item in items
            if item not in refined_dataset
        ]
        refined_dataset.extend(random.sample(all_remaining_items, remaining_target))
    # 초과하는 경우 단면 절단
    elif len(refined_dataset) > target_total:
        refined_dataset = refined_dataset[:target_total]

# 학습 시 특정 카테고리가 쏠리지 않도록 무작위 셔플
random.shuffle(refined_dataset)

# 3단계: 정제된 데이터 저장
print(f"\n3단계: 정제된 파일 저장 중 -> {output_file_path}")
with open(output_file_path, "w", encoding="utf-8") as out_f:
    for item in refined_dataset:
        out_f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"🎉 정제 완료! 최종 {len(refined_dataset)}건이 성공적으로 저장되었습니다.")