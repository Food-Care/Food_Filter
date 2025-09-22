import json

def find_ingredients_with_keywords(data_path, keywords_to_find):
    """
    JSON 데이터 파일에서 특정 키워드를 포함하는 모든 원재료명을 찾아 출력합니다.

    :param data_path: 원본 식품 데이터 JSON 파일 경로
    :param keywords_to_find: 검색할 키워드 리스트
    """
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            food_data = json.load(f)
        print(f"✅ '{data_path}' 파일을 성공적으로 불러왔습니다.")
    except FileNotFoundError:
        print(f"🚨 파일 오류: '{data_path}' 파일을 찾을 수 없습니다. 파일명을 확인해주세요.")
        return

    found_ingredients = set()

    for product in food_data:
        ingredients = product.get("원재료명", [])
        if not ingredients:
            continue

        for ingredient in ingredients:
            for keyword in keywords_to_find:
                if keyword in ingredient:
                    found_ingredients.add(ingredient)
                    break

    if found_ingredients:
        print(f"\n--- 🔍 총 {len(found_ingredients)}개의 원재료명을 찾았습니다 ---")
        for item in sorted(list(found_ingredients)):
            print(item)
    else:
        print("\n--- 해당 키워드를 포함하는 원재료를 찾지 못했습니다. ---")


if __name__ == "__main__":
    SEARCH_KEYWORDS = ["빵"]

    print(f"지정한 키워드: {SEARCH_KEYWORDS}")
    
    input_file = "./Data_Storage/정제 데이터/식품데이터_최종_표준화_완료.json"

    find_ingredients_with_keywords(input_file, SEARCH_KEYWORDS)