import pyupbit
import pandas as pd

tickers = pyupbit.get_tickers(fiat="KRW") # KRW/BTC/ETH/USDT
print(len(tickers), tickers)

df = pyupbit.get_ohlcv("KRW-BTC", interval="week", count=200)
df = pd.DataFrame(df).drop('value', axis=1)
print(df.head())