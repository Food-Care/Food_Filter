import json

def add_allergy_tags_with_exceptions(food_data_path, allergy_rules_path, output_path):
    try:
        with open(allergy_rules_path, "r", encoding="utf-8") as f:
            allergen_rules = json.load(f)
        print("'Allergy.json' 규칙 파일을 성공적으로 불러왔습니다.")

        with open(food_data_path, "r", encoding="utf-8") as f:
            food_data = json.load(f)
        print(f"총 {len(food_data)}개의 제품 데이터를 불러왔습니다.")

    except FileNotFoundError as e:
        print(f"파일 오류: '{e.filename}' 파일을 찾을 수 없습니다.")
        return
    except json.JSONDecodeError:
        print("JSON 오류: 파일의 형식이 올바른 JSON이 아닙니다.")
        return

    for product in food_data:
        found_allergens = set()
        ingredients = product.get("원재료명", [])
        if not ingredients:
            continue

        for ingredient in ingredients:
            for allergen, rules in allergen_rules.items():
                if not isinstance(rules, dict):
                    continue

                keywords = rules.get("keywords", [])
                exclusions = rules.get("exclusions", [])

                is_keyword_match = any(keyword in ingredient for keyword in keywords)

                if is_keyword_match:
                    is_excluded = any(exclusion in ingredient for exclusion in exclusions)

                    if not is_excluded:
                        found_allergens.add(allergen)

        if found_allergens:
            product["알레르기_유발_물질"] = sorted(list(found_allergens))

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(food_data, f, ensure_ascii=False, indent=4)
    print(f"성공! 예외 처리가 적용된 '{output_path}' 파일이 생성되었습니다.")

if __name__ == "__main__":
    food_file = "식품데이터_최종_표준화_완료.json"
    allergy_file = "Allergy.json"
    output_file = "식품데이터_알레르기_태그완료_v2.json"

    add_allergy_tags_with_exceptions(food_file, allergy_file, output_file)