import pyupbit
import time

access = "HxzMreaqvtoc197sqiqluljcgIB4NNK79UKSB7WP"
secret = "I2ZDtT1EZqxswZFuDQg6u3qwXnII6GRSZNgi9U9Q"

upbit = pyupbit.Upbit(access, secret)

coin = "KRW-BTC"

while True:

    try:

        print("시장 확인 중...")

        price = pyupbit.get_current_price(coin)

        if price is None:
            print("가격 조회 실패")
            time.sleep(5)
            continue

        print("현재가:", round(price))

        btc_balance = upbit.get_balance("BTC")

        if btc_balance is None:
            btc_balance = 0

        print("BTC 수량:", btc_balance)

        time.sleep(10)

    except Exception as e:

        print("에러:", e)

        time.sleep(10)