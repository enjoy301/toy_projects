import pyupbit
import pandas as pd
import mplfinance as mpf
import matplotlib as plt
import pymysql

tickers = pyupbit.get_tickers(fiat="KRW") # KRW/BTC/ETH/USDT
print(len(tickers), tickers)

df = pd.DataFrame(pyupbit.get_ohlcv("KRW-BTC", interval="week", count=10).drop('value', axis=1))
print(df.head())

#mpf.plot(df, type='candle')

connection = pymysql.connect(host='localhost', port=0, db='Coin', user='root', passwd='Rladmswhd@1', autocommit=True)
cursor = connection.cursor()
cursor.execute("SELECT VERSION();")
result = cursor.fetchone()
print(result)
connection.close()