import ccxt
import pandas as pd

from backtesting import Backtest, Strategy

# 바이낸스 연결
exchange = ccxt.binance()

# 데이터 가져오기
ohlcv = exchange.fetch_ohlcv(
    'BTC/USDT',
    timeframe='1h',
    limit=500
)

# 데이터프레임 생성
df = pd.DataFrame(
    ohlcv,
    columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
)

# 시간 변환
df['Time'] = pd.to_datetime(df['Time'], unit='ms')

# 인덱스 설정
df.set_index('Time', inplace=True)

# RSI 계산 함수
def calculate_rsi(series, period=14):

    delta = pd.Series(series).diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

# 전략 클래스
class MyStrategy(Strategy):

    def init(self):

        # 이동평균
        self.ma10 = self.I(
            lambda x: pd.Series(x).rolling(10).mean(),
            self.data.Close
        )

        self.ma30 = self.I(
            lambda x: pd.Series(x).rolling(30).mean(),
            self.data.Close
        )

        # RSI
        self.rsi = self.I(
            calculate_rsi,
            self.data.Close
        )

    def next(self):

        price = self.data.Close[-1]

        # 매수 조건
        if (
            self.ma10[-1] > self.ma30[-1]
            and self.rsi[-1] < 70
        ):

            if not self.position:

                # 손절 -3%
                stop_loss = price * 0.97

                self.buy(sl=stop_loss)

        # 매도 조건
        elif self.ma10[-1] < self.ma30[-1]:

            if self.position:
                self.position.close()

# 백테스트 실행
bt = Backtest(
    df,
    MyStrategy,
    cash=10000,
    commission=.002
)

result = bt.run()

print(result)

bt.plot()