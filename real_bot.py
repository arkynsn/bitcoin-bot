import pyupbit
import pandas as pd
import time

# =========================
# 업비트 API 키
# =========================

access = "HxzMreaqvtoc197sqiqluljcgIB4NNK79UKSB7WP"
secret = "I2ZDtT1EZqxswZFuDQg6u3qwXnII6GRSZNgi9U9Q"

upbit = pyupbit.Upbit(access, secret)

# =========================
# RSI 계산 함수
# =========================

def calculate_rsi(series, period=14):

    delta = series.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

# =========================
# 메인 반복
# =========================

while True:

    try:

        print("\n시장 확인 중...")

        # BTC 데이터 가져오기
        df = pyupbit.get_ohlcv(
            "KRW-BTC",
            interval="minute60",
            count=50
        )

        # 이동평균
        df['ma10'] = df['close'].rolling(10).mean()
        df['ma30'] = df['close'].rolling(30).mean()

        # RSI
        df['rsi'] = calculate_rsi(df['close'])

        latest = df.iloc[-1]

        price = latest['close']
        ma10 = latest['ma10']
        ma30 = latest['ma30']
        rsi = latest['rsi']

        print("현재가:", round(price))
        print("RSI:", round(rsi, 2))

        # =====================
        # 현재 BTC 보유량 확인
        # =====================

        btc_balance = upbit.get_balance("BTC")

        # =====================
        # BTC 없는 경우 → 매수 판단
        # =====================

        if btc_balance == 0:

            print("BTC 미보유 상태")

            # 매수 조건
            if ma10 > ma30 and rsi < 65:

                print("매수 조건 만족")

                krw = upbit.get_balance("KRW")

                if krw > 6000:

                    result = upbit.buy_market_order(
                        "KRW-BTC",
                        5000
                    )

                    print("자동 매수 완료")
                    print(result)

                else:

                    print("원화 부족")

            else:

                print("매수 조건 아님")

        # =====================
        # BTC 보유 중 → 매도 판단
        # =====================

        else:

            print("BTC 보유 중")

            avg_buy_price = upbit.get_avg_buy_price("BTC")

            target_price = avg_buy_price * 1.02
            stop_price = avg_buy_price * 0.99

            print("평균 매수가:", round(avg_buy_price))
            print("익절 목표:", round(target_price))
            print("손절 가격:", round(stop_price))

            # 익절
            if price >= target_price:

                print("익절 매도 실행")

                result = upbit.sell_market_order(
                    "KRW-BTC",
                    btc_balance
                )

                print(result)

            # 손절
            elif price <= stop_price:

                print("손절 매도 실행")

                result = upbit.sell_market_order(
                    "KRW-BTC",
                    btc_balance
                )

                print(result)

            else:

                print("보유 유지")

    except Exception as e:

        print("에러:", e)

    # 60초마다 반복
    time.sleep(60)