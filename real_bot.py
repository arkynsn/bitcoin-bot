import pyupbit
import time

# 업비트 API 키
access = "HxzMreaqvtoc197sqiqluljcgIB4NNK79UKSB7WP"
secret = "I2ZDtT1EZqxswZFuDQg6u3qwXnII6GRSZNgi9U9Q"

upbit = pyupbit.Upbit(access, secret)

# 설정
coin = "KRW-BTC"

take_profit = 1.5   # 익절 %
stop_loss = -1.0    # 손절 %

while True:

    try:
        print("시장 확인 중...")

        # 현재가
        price = pyupbit.get_current_price(coin)

        if price is None:
            print("가격 조회 실패")
            time.sleep(5)
            continue

        print("현재가:", round(price))

        # 보유 수량 확인
        balances = upbit.get_balances()

        btc_balance = 0
        avg_buy_price = 0

        for b in balances:

            if b['currency'] == 'BTC':

                btc_balance = float(b['balance'])

                if b['avg_buy_price'] is not None:
                    avg_buy_price = float(b['avg_buy_price'])

        # BTC 보유 중
        if btc_balance > 0:

            print("BTC 보유 중")

            profit_rate = ((price - avg_buy_price) / avg_buy_price) * 100

            print(f"현재 수익률: {profit_rate:.2f}%")

            # 익절
            if profit_rate >= take_profit:

                print("익절 매도 실행")

                upbit.sell_market_order(coin, btc_balance)

            # 손절
            elif profit_rate <= stop_loss:

                print("손절 매도 실행")

                upbit.sell_market_order(coin, btc_balance)

            else:
                print("보유 유지")

        # BTC 미보유
        else:

            print("BTC 없음")

            krw = upbit.get_balance("KRW")

            if krw is not None and krw > 5000:

                buy_amount = krw * 0.3

                print(f"{round(buy_amount)}원 매수")

                upbit.buy_market_order(coin, buy_amount)

        time.sleep(10)

    except Exception as e:

        print("에러:", e)

        time.sleep(10)