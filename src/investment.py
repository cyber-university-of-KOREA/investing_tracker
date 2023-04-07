import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# OpenDart API Key
API_KEY = "f87775cfc0cd17c470518d177c4cab57d5321d84"

def get_stock_info(stock_code):
    # API 호출을 위한 URL 설정
    url = f"https://opendart.fss.or.kr/api/stock/{stock_code}.json"
    params = {
        "crtfc_key": API_KEY,
        "fin_gubun": "0",
        "bsns_year": datetime.now().year - 10,
        "reprt_code": "11011"
    }

    # API 호출
    response = requests.get(url, params=params)
    data = response.json()

    if "list" not in data:
        print("해당 종목에 대한 정보가 없습니다.")
        return

    data = data["list"]

    # 데이터프레임으로 변환
    df = pd.DataFrame(data, columns=["rcept_no", "cls_amt"])
    df["rcept_no"] = pd.to_datetime(df["rcept_no"])
    df = df.set_index("rcept_no")
    df = df.sort_index()

    # 현재 주가 정보 추가
    url = f"https://finance.naver.com/item/main.naver?code={stock_code}"
    response = requests.get(url)
    html = response.text

    start_pos = html.find("last\">") + 6
    end_pos = html.find("</td>", start_pos)
    current_price = int(html[start_pos:end_pos].replace(",", ""))
    current_date = datetime.now()
    current_df = pd.DataFrame({"date": [current_date], "cls_amt": [current_price]})
    current_df["date"] = pd.to_datetime(current_df["date"])
    current_df = current_df.set_index("date")

    # 데이터프레임 병합
    df = pd.concat([df, current_df])

    # 성장 가능성 분석
    mean_price_1 = df.tail(180)["cls_amt"].mean() # 최근 6개월 동안의 평균 주가
    mean_price_2 = df.tail(720)["cls_amt"].mean() # 최근 2년 동안의 평균 주가
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
    plt.plot(df.index, df["cls_amt"])
    plt.title(f"{stock_code} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

if __name__ == '__main__':
    # 사용자 입력 받기
    stock_code = input("한국 주식의 종목코드를 입력하세요: ")

    # 함수 호출
    get_stock_info(stock_code)
