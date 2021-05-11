import pyupbit
import pandas as pd
import mplfinance as mpf
import matplotlib as plt
import pymysql
from datetime import datetime

def update_code_info(cursor):
    tickers = pyupbit.get_tickers(fiat="KRW")  # KRW/BTC/ETH/USDT
    cursor.execute("select * from coin_info;")
    result = cursor.fetchall()
    code_list = [list(i)[0] for i in result]
    if sorted(tickers) != code_list:
        for i in range(len(tickers)):
            print("coin 목록 UPDATE")
            sql = f"REPLACE INTO coin_info(code) VALUES('{tickers[i]}');"
            cursor.execute(sql)

def update_price_week(today):
    df = pd.DataFrame(pyupbit.get_ohlcv("KRW-BTC", interval="week", count=100).drop('value', axis=1))
    for i in range(len(df)):
        print(df.iloc[i])
    # mpf.plot(df, type='candle')

connection = pymysql.connect(host='localhost', port=0, db='Coin', user='root', passwd='Rladmswhd@1', autocommit=True)
cursor = connection.cursor()
today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

#update_code_info(cursor)
#update_price_week(today)

connection.close()