import pyupbit
import time

# =========================
# 업비트 API 키
# =========================

access = "HxzMreaqvtoc197sqiqluljcgIB4NNK79UKSB7WP"
secret = "I2ZDtT1EZqxswZFuDQg6u3qwXnII6GRSZNgi9U9Q"

upbit = pyupbit.Upbit(access, secret)

# =========================
# 목표 설정
# =========================

take_profit = 1.02   # +2%
stop_loss = 0.99     # -1%

# =========================
# 비트코인 현재 보유량
# =========================

btc_balance = upbit.get_balance("BTC")

print("현재 BTC 보유량:", btc_balance)

# BTC 없으면 종료
if btc_balance == 0:

    print("BTC 보유 없음")

    quit()

# =========================
# 평균 매수가
# =========================

avg_buy_price = upbit.get_avg_buy_price("BTC")

print("평균 매수가:", avg_buy_price)

# 목표 가격 계산
target_price = avg_buy_price * take_profit
stop_price = avg_buy_price * stop_loss

print("익절 목표:", round(target_price))
print("손절 가격:", round(stop_price))

# =========================
# 무한 감시
# =========================

while True:

    try:

        # 현재 BTC 가격
        current_price = pyupbit.get_current_price("KRW-BTC")

        print("\n현재 가격:", current_price)

        # 익절 조건
        if current_price >= target_price:

            print("익절 매도 실행")

            result = upbit.sell_market_order(
                "KRW-BTC",
                btc_balance
            )

            print(result)

            break

        # 손절 조건
        elif current_price <= stop_price:

            print("손절 매도 실행")

            result = upbit.sell_market_order(
                "KRW-BTC",
                btc_balance
            )

            print(result)

            break

        else:

            print("보유 중...")

    except Exception as e:

        print("에러:", e)

    # 10초마다 확인
    time.sleep(10)