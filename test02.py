from dart_fss import get_corp_list
import dart_fss as dart

api_key='your_api_key'

dart.set_api_key(api_key=api_key)

# 모든 상장된 기업 리스트 불러오기
crp_list = get_corp_list()

# 삼성전자를 이름으로 찾기 ( 리스트 반환 )
samsung = crp_list.find_by_corp_name('삼성전자', exactly=True)[0]

# 증권 코드를 이용한 찾기
samsung = crp_list.find_by_stock_code('005930')

# 다트에서 사용하는 회사코드를 이용한 찾기
samsung = crp_list.find_by_corp_code('00126380')

# "삼성"을 포함한 모든 공시 대상중 코스피 및 코스닥 시장에 상장된 공시 대상 검색(Y: 코스피, K: 코스닥, N:코넥스, E:기타)
# corps = crp_list.find_by_name('삼성', market=['Y','K']) # 아래와 동일
#corps = crp_list.find_by_name('삼성', market='YK')

# "휴대폰" 생산품과 연관된 공시 대상
corps = crp_list.find_by_product('휴대폰')

# "휴대폰" 생산품과 연관된 공시 대상 중 코스피 시장에 상장된 대상만 검색
corps = crp_list.find_by_product('휴대폰', market='Y')

# 섹터 리스트 확인
crp_list.sectors

# "텔레비전 방송업" 섹터 검색
corps = crp_list.find_by_sector('텔레비전 방송업')

crp_list = samsung.extract_fs(bgn_de='20120101')

crp_list.save()


