import pandas as pd
import requests
from datetime import datetime
import dart_fss as dart
import matplotlib.pyplot as plt

# OpenDart API Key 입력
api_key = "f87775cfc0cd17c470518d177c4cab57d5321d84"

# 종목 코드 입력
stock_code = "005930"

# API 호출 URL 생성
url = f"https://opendart.fss.or.kr/api/ipo/stock.json?crtfc_key={api_key}&isu_cd={stock_code}&page_count=10"

# API 호출
response = requests.get(url)
corp_list = dart.get_corp_list()
# 데이터 추출
data = response.json()[corp_list]
df = pd.DataFrame(data)

# 날짜 정보를 datetime 형태로 변환
df["dt"] = pd.to_datetime(df["dt"])

# 종가 정보 추출
prices = df["tdd_clsprc"].tolist()

# 현재 주가와 10년 전 주가를 추출
current_price = prices[-1]
past_price = prices[0]

# 현재 주가와 10년 전 주가의 비율을 계산하여 성장률을 구함
growth_rate = (current_price / past_price - 1) * 100

# 결과 출력
print("현재 주가:", current_price)
print("10년 전 주가:", past_price)
print("성장률:", growth_rate)

# 그래프 출력
plt.plot(df["dt"], prices)
plt.xlabel("날짜")
plt.ylabel("주가")
plt.title("주식 가격 정보")
plt.show()
