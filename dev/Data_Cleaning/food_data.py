import pandas as pd
import json
from fuzzywuzzy import fuzz
import sys
import itertools

file_path = 'C:/Users/94320/VsCode/Data/Data_storage/원시 데이터/전체_식품데이터.xlsx'
output_path = '0차_정제_식품데이터.json'

try:
    df = pd.read_excel(file_path, engine='openpyxl')
    print("파일을 성공적으로 불러왔습니다.")
except FileNotFoundError:
    print(f"오류: '{file_path}' 파일을 찾을 수 없습니다. 파일 경로와 이름을 다시 확인해주세요.")
    exit()
except Exception as e:
    print(f"파일을 읽는 도중 오류가 발생했습니다: {e}")
    print("인코딩 문제이거나 파일 형식이 올바르지 않을 수 있습니다.")
    exit()

def remove_duplicate_ingredients(ingredients_str):
    """
    RAWMTRL_NM 열의 문자열에서 중복된 원재료를 제거하는 함수
    """
    if pd.isna(ingredients_str):
        return ingredients_str

    ingredients_list = [item.strip() for item in ingredients_str.split(',')]
    
    unique_ingredients = sorted(list(set(ingredients_list)))
    
    return ', '.join(unique_ingredients)

df['RAWMTRL_NM'] = df['RAWMTRL_NM'].apply(remove_duplicate_ingredients)
print("1. RAWMTRL_NM 열에서 중복된 원재료를 제거했습니다.")


df = df[df['RAWMTRL_NM'] != '원재료미등록']
print("2. '원재료미등록'이 포함된 행을 삭제했습니다.")

categories_to_delete = [
    'L-시스틴', '글리세린호박산지방산에스테르', 'L-글루타민', 'L-글루타민산', 'L-글루타민산나트륨',
    'L-라이신염산염', 'L-로이신', 'l-멘톨', 'L-발린', 'L-세린', 'L-아르지닌', 'L-아르기닌',
    'L-아스코르빈산나트륨', 'L-아스파라긴', 'L-아스파트산', 'L-이소로이신', 'L-주석산수소칼륨',
    'L-트립토판', 'L-티로신', 'L-페닐알라닌', 'L-히스티딘', 'L-히스티딘염산염', '혼합제제',
    '천연착향료', '치자황색소', '커피', '커피원두', '향신료조제품', '산소', '아산화질소',
    'L-글루타민산나트륨제제', '타르색소제제', '차아염소산나트륨', '염산', 'L-글루탐산나트륨제제',
    '수산화나트륨액', '수산화나트륨', '식품첨가물과기구등의살균소독제', '치자청색소',
    '과산화수소제제', '과산화수소', '혼합제제와기구등의살균소독제', '기구등의 살균·소독제',
    '염화알킬(C12-C18)벤질디메틸암모늄제제', '에탄올제제', '5-리보뉴클레오티드칼슘', '황산',
    '인산', '글리세린지방산에스테르', '실리카겔', '커피원두건조', '빙초산', '베리류색소',
    '비트레드', '안나토색소', '오징어먹물색소', '치자적색소', '카카오색소', '향신료올레오레진류',
    '토마토색소', '홍국적색소', '홍화황색소', '차아염소산수미산성', '이산화염소(수)',
    '소르비탄지방산에스테르', '글리세린초산지방산에스테르', '글리세린구연산지방산에스테르',
    '글리세린젖산지방산에스테르', '스테아릴젖산칼슘', '스테아릴젖산나트륨',
    '폴리글리세린지방산에스테르', '메타인산나트륨', '아황산나트륨무수', '아황산나트륨',
    '카라멜색소 Ⅲ', 'D-소르비톨액', 'D-말티톨', 'D-소르비톨', 'D-자일로오스',
    'DL-주석산나트륨', 'DL-사과산', 'DL-알라닌', 'DL-주석산수소칼륨', '제삼인산나트륨',
    '스피룰리나색소', '홍국색소', '유동파라핀', '펙틴', '이산화규소',
    '기타기구등의 살균소독제', '펙티나아제', '활성탄', '폴리글리시톨시럽', '기타천연향료',
    '심황색소', '마리골드색소', '파프리카추출색소', '고량색소', '코치닐추출색소', '락색소',
    '홍국황색소', '프로필렌글리콜', '폴리소르베이트20', '폴리소르베이트80', '폴리소르베이트60',
    '면류첨가알칼리제', '산화칼슘', '차아염소산나트륨제제', '효소처리스테비아',
    '올레오레진 캪시컴', '폴리에틸렌테레프탈레이트', '프로필렌글리콜지방산에스테르',
    '판토텐산칼슘', '실리코알루민산나트륨', '이산화염소제제',
    '폴리(헥사메틸렌비구아니드)하이드로클로라이드제제', '과산화초산제제', 'L-라이신',
    '1제식합성팽창제', '합성착향료', '수산화나트륨무수', '조제해수염화마그네슘',
    '삭카린나트륨제제', '과산화초산', '어업용얼음', '구아검', '구연산', '구연산무수',
    '구연산삼나트륨2수염', '구연산삼나트륨', '구연산철', '구연산칼륨', '구연산칼슘',
    '과산화벤조일(희석)', '합성팽창제', '2제식팽창제제', '카라멜색소', '질소',
    '이소티오시안산알릴', '가티검', '쇼트닝', '청관제', '차아염소산수', '셀룰라아제',
    '수산화칼슘', '효소처리루틴', '레시틴', '감초추출물', '락타아제', '키토산',
    '침강실리카', '가공화분', '자주색고구마색소', '감초추출물 조제', '탄닌산',
    '옥타코사놀함유제품', '테아닌'
]
df = df[~df['PRDLST_DCNM'].isin(categories_to_delete)]
print("3. 삭제해야 할 카테고리 리스트에 해당하는 모든 제품을 삭제했습니다.")


cleaned_df = df[['PRDLST_NM', 'BSSH_NM', 'PRDLST_DCNM', 'RAWMTRL_NM']].copy()
cleaned_df.rename(columns={
    'PRDLST_NM': '제품명',
    'BSSH_NM': '회사명',
    'PRDLST_DCNM': '카테고리',
    'RAWMTRL_NM': '원재료명'
}, inplace=True)
print("4. 필요한 열만 선택하여 새로운 DataFrame을 생성했습니다.")

try:
    cleaned_df.to_json(output_path, orient='records', force_ascii=False, indent=4)
    print(f"정제된 데이터가 '{output_path}' 파일로 성공적으로 저장되었습니다.")
except Exception as e:
    print(f"오류: Json 파일 저장 중 오류가 발생했습니다: {e}")
