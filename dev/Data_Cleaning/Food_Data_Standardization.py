import pandas as pd
import json
import sys

input_data_path = '2차_정제_식품데이터.json'
category_groups_path = '카테고리_유사어_그룹.json'
ingredient_groups_path = '원재료명_유사어_그룹.json'
output_path = '최종_표준화_식품데이터.json'

try:
    df = pd.read_json(input_data_path)
    print("2차 정제된 식품 데이터를 성공적으로 불러왔습니다.")
except FileNotFoundError:
    print(f"오류: '{input_data_path}' 파일을 찾을 수 없습니다. 파일 경로를 다시 확인해주세요.")
    sys.exit()
except Exception as e:
    print(f"파일을 읽는 도중 오류가 발생했습니다: {e}")
    sys.exit()

def load_standardization_groups(file_path):
    """
    유사어 그룹 JSON 파일을 읽어 매핑 사전을 생성하는 함수
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            groups = json.load(f)
        
        standardization_map = {}
        for canonical_name, aliases in groups.items():
            for alias in aliases:
                if alias != canonical_name:
                    standardization_map[alias] = canonical_name
        return standardization_map
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다. 유사어 그룹 파일을 먼저 생성해주세요.")
        sys.exit()
    except Exception as e:
        print(f"오류: 유사어 그룹 파일을 읽는 도중 오류가 발생했습니다: {e}")
        sys.exit()

category_map = load_standardization_groups(category_groups_path)
ingredient_map = load_standardization_groups(ingredient_groups_path)

def apply_standardization(item, mapping_dict):
    """
    단일 항목에 대해 표준화 매핑을 적용하는 함수
    """
    return mapping_dict.get(item, item)

def apply_standardization_list(items_list, mapping_dict):
    """
    원재료명 리스트에 대해 표준화 매핑을 적용하는 함수
    """
    return [mapping_dict.get(item, item) for item in items_list]

print("\n데이터 표준화를 시작합니다...")
df['카테고리'] = df['카테고리'].apply(lambda x: apply_standardization(x, category_map))

df['원재료명'] = df['원재료명'].apply(lambda x: apply_standardization_list(x, ingredient_map))

print("데이터 표준화가 완료되었습니다.")

try:
    df.to_json(output_path, orient='records', force_ascii=False, indent=4)
    print(f"\n표준화된 최종 데이터가 '{output_path}' 파일로 성공적으로 저장되었습니다.")
except Exception as e:
    print(f"오류: 최종 JSON 파일 저장 중 오류가 발생했습니다: {e}")
