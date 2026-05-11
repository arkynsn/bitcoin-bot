import pyupbit

# 업비트 API 키 입력
access = "HxzMreaqvtoc197sqiqluljcgIB4NNK79UKSB7WP"
secret = "I2ZDtT1EZqxswZFuDQg6u3qwXnII6GRSZNgi9U9Q"

# 업비트 연결
upbit = pyupbit.Upbit(access, secret)

# 현재 원화 잔고 확인
krw = upbit.get_balance("KRW")

print("현재 KRW 잔고:", krw)

# 6000원 이상 있을 때만 실행
# (수수료 때문에 5000보다 조금 여유 필요)
if krw > 6000:

    print("비트코인 5000원 자동 매수 시작")

    # 시장가 5000원 매수
    result = upbit.buy_market_order(
        "KRW-BTC",
        5000
    )

    print("주문 결과:")
    print(result)

else:

    print("잔고 부족")