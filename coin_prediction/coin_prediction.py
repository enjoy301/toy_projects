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
        print("coin 목록 UPDATE 중...")
        for i in range(len(tickers)):
            sql = f"REPLACE INTO coin_info(code) VALUES('{tickers[i]}');"
            cursor.execute(sql)
        print("coin 목록 UPDATE 완료!")

def update_price_week_each(code, cursor, today): #REPLACE함수 때매 매번 전체다 reset을 로딩안된날짜만 추가하는 방법으로
    coin_symbol = code[code.index('-')+1:]
    print(coin_symbol+"_price_week UPDATE 중...")
    check_first = 1
    df = pd.DataFrame(pyupbit.get_ohlcv(code, interval="week", count=1000).drop('value', axis=1))
    for i in range(len(df)):
        if check_first != 1:
            today_close = float(df.iloc[i]['close'])
            yesterday_close = float(df.iloc[i-1]['close'])
            diff_rate = (today_close-yesterday_close)*100/yesterday_close
        else:
            diff_rate = 0
            check_first = 0
        date = datetime.strptime(str(df.index[i]), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        sql = f"REPLACE INTO "+coin_symbol+"_price_week(date, open, high, low, close, volumn, diff_rate) " \
              f"VALUES({date}, {df.iloc[i]['open']}, {df.iloc[i]['high']}, {df.iloc[i]['low']}, " \
              f"{df.iloc[i]['close']}, {df.iloc[i]['volume']}, {diff_rate});"
        cursor.execute(sql)
    print(coin_symbol+"_price_week UPDATE 완료!")
    #mpf.plot(df, type='candle')

def update_price_week_all(cursor): # update_code_info에서 tickers 받아오는 형식으로 변경 필요
    tickers = pyupbit.get_tickers(fiat="KRW")
    for code in tickers:
        coin_symbol = code[code.index('-') + 1:]
        sql = "create table if not exists `"+coin_symbol+"_price_week` (" \
              "`date` datetime, " \
              "`open` decimal(11,2)," \
              "`high` decimal(11,2)," \
              "`low` decimal(11,2)," \
              "`close` decimal(11,2)," \
              "`volumn` bigint," \
              "`diff_rate` decimal(10,5)," \
              "PRIMARY KEY(`date`));"
        cursor.execute(sql)
        update_price_week_each(code, cursor, today)


connection = pymysql.connect(host='localhost', port=0, db='Coin', user='root', passwd='Rladmswhd@1', autocommit=True)
cursor = connection.cursor()
today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

#update_code_info(cursor)
#update_price_week_all(cursor)

connection.close()