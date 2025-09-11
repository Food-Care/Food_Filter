import pandas as pd
import json
from fuzzywuzzy import fuzz
import sys

file_path = '정제된_식품데이터.json'
output_path = '2차_정제_식품데이터.json'
# 유사도 매칭을 위한 기준치 (0-100 사이)
SIMILARITY_THRESHOLD = 90

try:
    df = pd.read_json(file_path)
    print("JSON 파일을 성공적으로 불러왔습니다.")
except FileNotFoundError:
    print(f"오류: '{file_path}' 파일을 찾을 수 없습니다. 파일 경로와 이름을 다시 확인해주세요.")
    sys.exit()
except Exception as e:
    print(f"파일을 읽는 도중 오류가 발생했습니다: {e}")
    sys.exit()

df['원재료명'] = df['원재료명'].apply(lambda x: [] if isinstance(x, str) and x == '[]' else x)
df['원재료명'] = df['원재료명'].fillna(value='').apply(lambda x: [] if x == '' else x)
initial_rows = len(df)
df = df[df['원재료명'].map(lambda d: len(d) > 0)]
removed_rows = initial_rows - len(df)
print(f"1. 원재료명이 없는 {removed_rows}개의 항목을 제거했습니다.")

def explore_standardization(data_series, column_name):
    """
    주어진 키워드를 기반으로 유사한 문자열을 찾아내어 JSON으로 저장하는 함수
    """
    if column_name == '원재료명':
        all_items = [item for sublist in data_series.dropna() for item in sublist]
        unique_items = sorted(list(set(all_items)))
    else:
        unique_items = data_series.dropna().unique()
    
    standardization_groups = {}
    processed_items = set()

    print(f"\n[{column_name}] 열 유사어 그룹을 검색합니다...")

    for item in unique_items:
        if item in processed_items:
            continue

        similar_items = [item]
        for other_item in unique_items:
            if item != other_item and fuzz.ratio(str(item), str(other_item)) >= SIMILARITY_THRESHOLD:
                similar_items.append(other_item)

        if len(similar_items) > 1:
            keyword = sorted(similar_items)[0]
            standardization_groups[keyword] = sorted(list(set(similar_items)))
            for similar_item in similar_items:
                processed_items.add(similar_item)

    if not standardization_groups:
        print(f"  - {column_name}에서 유사도가 높은 그룹이 발견되지 않았습니다.")
    else:
        output_filename = f"{column_name}_유사어_그룹.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(standardization_groups, f, indent=4, ensure_ascii=False)
        print(f"  - 유사어 그룹이 '{output_filename}' 파일로 저장되었습니다.")
        
try:
    df.to_json(output_path, orient='records', force_ascii=False, indent=4)
    print(f"\n변환된 데이터가 '{output_path}' 파일로 성공적으로 저장되었습니다.")
except Exception as e:
    print(f"오류: JSON 파일 저장 중 오류가 발생했습니다: {e}")
