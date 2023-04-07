import requests
import pandas as pd
import matplotlib.pyplot as plt

# API 키
api_key = 'your_api_key'

# 요청할 URL
url = "http://dart.fss.or.kr/dsab002/search.ax?reportName=%EC%A3%BC%EC%8B%9D%EC%8B%9C%EC%84%B8%EB%8D%B0%EC%9D%B4%ED%84%B0&textCrpNm=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&startDate=19990101&endDate=20220403&currentPage=1&maxResults=100"
response = requests.get(url)

# HTML 데이터를 파싱해서 pandas DataFrame으로 저장
dfs = pd.read_html(response.content)

if not dfs:
    print("No table found in the HTML data!")
else:
    df = dfs[0]  # 첫 번째 테이블 선택
    print(df.head())

# 요청할 파라미터
params = {
    'serviceKey': api_key,
    'secnNm': '삼성전자', # 주식 종목명
    'pagePath': '/finance/stocks/market-info/market-summary', # 페이지 경로
    'idx': '1' # 페이지 인덱스
}

# API에 GET 요청 보내기
response = requests.get(url, params=params)

# XML 데이터를 DataFrame 형식으로 변환
df = pd.read_html(response.content)[0]

# DataFrame을 엑셀 파일로 저장
df.to_excel('stock_prices.xlsx', index=False)

# 엑셀 파일에서 데이터 불러오기
df = pd.read_excel('stock_prices.xlsx')

# 종가 데이터만 추출
closing_prices = df['종가']

# 종가 데이터의 추이 그래프 그리기
plt.plot(closing_prices)
plt.title('Stock Price Trend')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
