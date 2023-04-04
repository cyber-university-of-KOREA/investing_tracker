# 여러 API 중에서 FinanceData.KR의 API를 활용
# 먼저 필요한 라이브러리와 API 키를 설정합니다.

import requests
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

API_KEY = 'f87775cfc0cd17c470518d177c4cab57d5321d84'


def get_stock_info(stock_code="QQQ"):
    # API 호출을 위한 URL 설정
    url = f"https://api.finance-data.kr/v1/stock/{stock_code}/price"
    params = {
        "apikey": API_KEY,
        "freq": "day",
        "start": datetime.now() - timedelta(days=3650), # 10년치 데이터를 가져옴
        "end": datetime.now()
    }

    # API 호출
    response = requests.get(url, params=params)
    data = response.json()["data"]

    # 데이터프레임으로 변환
    df = pd.DataFrame(data, columns=["date", "close_price"])
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    df = df.sort_index()

    # 현재 주가 정보 추가
    url = f"https://api.finance-data.kr/v1/stock/{stock_code}/price"
    params = {"apikey": API_KEY}
    response = requests.get(url, params=params)
    current_price = response.json()["last_price"]
    current_date = datetime.now()
    current_df = pd.DataFrame({"date": [current_date], "close_price": [current_price]})
    current_df["date"] = pd.to_datetime(current_df["date"])
    current_df = current_df.set_index("date")

    # 데이터프레임 병합
    df = pd.concat([df, current_df])

    # 성장 가능성 분석
    mean_price_1 = df.tail(180)["close_price"].mean() # 최근 6개월 동안의 평균 주가
    mean_price_2 = df.tail(720)["close_price"].mean() # 최근 2년 동안의 평균 주가
    growth_rate = (mean_price_1 - mean_price_2) / mean_price_2 * 100



    # 결과 출력
    print(f"최근 6개월 동안의 주가 평균: {mean_price_1:.2f}")
    print(f"최근 2년 동안의 주가 평균: {mean_price_2:.2f}")
    print(f"성장률: {growth_rate:.2f}%")
    if growth_rate > 0:
        print("성장 가능성이 있습니다.")
    else:
        print("성장 가능성이 낮습니다.")

    # 그래프 출력
    plt.plot(df.index, df["close_price"])
    plt.title(f"{stock_code} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

if __name__ == "__main__":
    get_stock_info("QQQ")