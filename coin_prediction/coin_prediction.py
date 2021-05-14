import pyupbit
import pandas as pd
import mplfinance as mpf
import matplotlib as plt
import pymysql
from datetime import datetime

def update_code_info(cursor):
    tickers = pyupbit.get_tickers(fiat="KRW")
    cursor.execute("select * from coin_info;")
    result = cursor.fetchall()
    code_list = [list(i)[0] for i in result]
    if sorted(tickers) != code_list:
        print("coin 목록 UPDATE 중...")
        for i in range(len(tickers)):
            cursor.execute(f"REPLACE INTO coin_info(code) VALUES('{tickers[i]}');")
        print("coin 목록 UPDATE 완료!")

def update_price_week_each(code, cursor):
    coin_symbol = code[code.index('-')+1:]
    table_name = coin_symbol+"_price_week"
    print(table_name+" UPDATE 중...")
    cursor.execute("select max(date) from "+table_name+";")
    last_update = cursor.fetchall()[0][0]

    count = 500
    if last_update != None:
        day_diff = (datetime.now() - last_update).days
        count = day_diff//7+1
    df = pd.DataFrame(pyupbit.get_ohlcv(code, interval="week", count=count).drop('value', axis=1))

    check_first = 1
    for i in range(len(df)):
        if last_update != None and check_first == 1:
            check_first = 0
            continue
        elif check_first != 1 or last_update != None:
            today_close = float(df.iloc[i]['close'])
            yesterday_close = float(df.iloc[i-1]['close'])
            diff_rate = (today_close-yesterday_close)*100/yesterday_close
        else: #None이고 처음 들어왔을 때
            diff_rate = 0
        check_first = 0
        date = datetime.strptime(str(df.index[i]), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        sql = f"INSERT INTO "+coin_symbol+"_price_week(date, open, high, low, close, volumn, diff_rate) " \
              f"VALUES({date}, {df.iloc[i]['open']}, {df.iloc[i]['high']}, {df.iloc[i]['low']}, " \
              f"{df.iloc[i]['close']}, {df.iloc[i]['volume']}, {diff_rate});"
        cursor.execute(sql)
    print(table_name+" UPDATE 완료!")
    #mpf.plot(df, type='candle')

def update_price_week_all(cursor): # 최종때, update_code_info에서 tickers 받아오는 형식으로 변경 필요
    tickers = pyupbit.get_tickers(fiat="KRW")
    count = 0
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
        update_price_week_each(code, cursor)
        if count == 0:
            break
        count += 1


connection = pymysql.connect(host='localhost', port=0, db='Coin', user='root', passwd='Rladmswhd@1', autocommit=True)
cursor = connection.cursor()

#update_code_info(cursor)
#update_price_week_all(cursor)

connection.close()