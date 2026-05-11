import ccxt
import pandas as pd

# 바이낸스 연결
exchange = ccxt.binance()

# 비트코인 1시간봉 50개 가져오기
ohlcv = exchange.fetch_ohlcv(
    'BTC/USDT',
    timeframe='1h',
    limit=50
)

# 데이터프레임 변환
df = pd.DataFrame(
    ohlcv,
    columns=['time', 'open', 'high', 'low', 'close', 'volume']
)

# 이동평균 계산
df['ma10'] = df['close'].rolling(10).mean()
df['ma30'] = df['close'].rolling(30).mean()

# 최신 데이터 가져오기
latest = df.iloc[-1]

print("현재 가격:", latest['close'])
print("10 이동평균:", latest['ma10'])
print("30 이동평균:", latest['ma30'])

# 매수 조건 판단
if latest['ma10'] > latest['ma30']:
    print("매수 신호")
else:
    print("대기")