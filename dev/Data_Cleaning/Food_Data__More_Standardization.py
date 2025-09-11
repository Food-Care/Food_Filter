import pandas as pd
import json

if __name__ == "__main__":
    main_json_path = "식품데이터_카테고리_표준화.json"
    materials_json_path = "원재료명_유사어_그룹.json"

    with open(materials_json_path, 'r', encoding='utf-8') as f:
        materials_rules_dict = json.load(f)

    materials_map = {}
    for standard_word, synonym_list in materials_rules_dict.items():
        for synonym in synonym_list:
            materials_map[synonym] = standard_word

    def standardize_materials_list(materials_list):
        return [materials_map.get(item, item) for item in materials_list]

    df_food = pd.read_json(main_json_path)
    df_food['원재료명'] = df_food['원재료명'].apply(standardize_materials_list)

    output_path = "식품데이터_최종_표준화_완료.json"
    df_food.to_json(output_path, orient='records', force_ascii=False, indent=4)

    print(f"\n✅ 원재료명 표준화가 완료되어 '{output_path}' 파일로 저장되었습니다.")