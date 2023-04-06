import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from datetime import datetime, timedelta

# OpenDart API 인증키
api_key = "your_api_key"

# 사용자 입력으로 종목 코드 받기
stock_code = input("한국 주식의 종목코드를 입력하세요: ")

# API 요청 URL 설정
url = "https://opendart.fss.or.kr/api/foramtData.do"
params = {
    "crtfc_key": api_key,
    "corp_code": stock_code,
    "bsns_year": "2022",
    "reprt_code": "11011",
    "fs_div": "CFS",
}

# API 요청 보내기
response = requests.get(url, params=params)

# API 요청이 성공적으로 수행되지 않은 경우, 에러 메시지 출력 후 프로그램 종료
if response.status_code != 200:
    print("API request error")
    exit()

# API에서 받아온 데이터를 DataFrame으로 변환하기
# data = pd.read_excel(BytesIO(response.content))
file_path = 'fsdata/00126380_annual.xlsx'
data = pd.read_excel(file_path, engine='openpyxl')

# DataFrame에서 종가 정보 가져오기
closing_price = data.loc[data['부채총계'] == '당기순이익(손실)', '2021.12'].values[0]

# 성장 가능성 분석하기
growth_potential = "높음" if closing_price > 0 else "낮음"

# 결과 출력하기
print(f"현재 종가: {closing_price}원")
print(f"성장 가능성: {growth_potential}")

# 그래프 그리기
date_range = pd.date_range(end=datetime.now(), periods=len(data.columns)-2, freq='M') # 2개 열은 코드명과 항목명이므로 제외
plt.plot(date_range, data.loc[4][2:], label="당기순이익(손실)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.title(f"{stock_code} 주식 가격 추이")
plt.legend()
plt.show()

