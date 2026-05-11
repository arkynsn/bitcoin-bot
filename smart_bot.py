import ccxt
import pandas as pd
import requests
import time
import random

# =========================
# 텔레그램 설정
# =========================

TOKEN = '8611639719:AAGkYy7e3sVqAn4Ozy6YOKhtqe-70wPUHls'
CHAT_ID = '8759965133'

# =========================
# 거래소 연결
# =========================

exchange = ccxt.binance()

# =========================
# 감시 코인
# =========================

coins = [
    'BTC/USDT',
    'ETH/USDT',
    'SOL/USDT',
    'XRP/USDT'
]

# =========================
# RSI 계산
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
# 텔레그램 전송
# =========================

def send_telegram(message):

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    data = {
        'chat_id': CHAT_ID,
        'text': message
    }

    requests.post(url, data=data)

# =========================
# AI 점수 흉내 함수
# =========================

def fake_ai_score(rsi, ma10, ma30):

    score = 50

    if ma10 > ma30:
        score += 20

    if rsi < 60:
        score += 20

    if rsi < 40:
        score += 10

    score += random.randint(-5, 5)

    return min(score, 100)

# =========================
# 시작 알림
# =========================

send_telegram("스마트 트레이딩 봇 시작")

# =========================
# 메인 루프
# =========================

while True:

    try:

        print("\n시장 감시 시작")

        for coin in coins:

            # 데이터 가져오기
            ohlcv = exchange.fetch_ohlcv(
                coin,
                timeframe='1h',
                limit=100
            )

            # 데이터프레임
            df = pd.DataFrame(
                ohlcv,
                columns=[
                    'time',
                    'open',
                    'high',
                    'low',
                    'close',
                    'volume'
                ]
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

            # AI 점수
            ai_score = fake_ai_score(
                rsi,
                ma10,
                ma30
            )

            print(f'\n{coin}')
            print('가격:', round(price, 2))
            print('RSI:', round(rsi, 2))
            print('AI 점수:', ai_score)

            # 강한 매수 조건
            if (
                ma10 > ma30
                and rsi < 65
                and ai_score >= 75
            ):

                message = f'''
강한 매수 신호

코인: {coin}

가격: {round(price,2)}

RSI: {round(rsi,2)}

AI 점수: {ai_score}/100
'''

                print(message)

                send_telegram(message)

            else:

                print('대기')

        # 60초 대기
        print("\n다음 검사까지 60초 대기")

        time.sleep(60)

    except Exception as e:

        print('에러:', e)

        time.sleep(10)