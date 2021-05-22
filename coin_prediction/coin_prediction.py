import pyupbit
from pyupbit import WebSocketManager as upWM
from pybithumb import Bithumb
from pybithumb import WebSocketManager as thWM
import pandas as pd
import matplotlib.pyplot as plt
import pymysql
from datetime import datetime

def interval_set_count(interval, last_update):
    if interval == "week":
        count = 400
        if last_update != None:
            day_diff = (datetime.now() - last_update).days
            count = int(day_diff // 7) + 1
        return count
    elif interval == "day":
        count = 2000
        if last_update != None:
            day_diff = (datetime.now() - last_update).seconds / 3600
            count = int(day_diff // 24) + 1
        return count
    elif interval == "minute240": #4시간
        count = 2000
        if last_update != None:
            day_diff = (datetime.now() - last_update).seconds / 3600
            count = int(day_diff // 4) + 1
        return count
    elif interval == "minute60": #1시간
        count = 2000
        if last_update != None:
            day_diff = (datetime.now() - last_update).seconds / 3600
            count = int(day_diff)+ 1
        return count

def update_price_each(code, cursor, interval):
    coin_symbol = code[code.index('-')+1:]
    table_name = coin_symbol+"_price_"+interval
    print(table_name+" UPDATE 중...")
    cursor.execute("select max(date) from "+table_name+";")
    last_update = cursor.fetchall()[0][0]

    count = interval_set_count(interval, last_update)
    if count == 1:
        print(table_name + " UPDATE 완료!")
        return
    df = pd.DataFrame(pyupbit.get_ohlcv(code, interval=interval, count=count))
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
        sql = f"INSERT INTO "+coin_symbol+"_price_"+interval+"(date, volumn, close, diff_rate) " \
              f"VALUES({date}, {df.iloc[i]['volume']}, {df.iloc[i]['close']}, {diff_rate});"
        cursor.execute(sql)
    print(table_name+" UPDATE 완료!")

def update_price_all():
    tickers = pyupbit.get_tickers(fiat="KRW")
    for interval in ["week", "day", "minute240", "minute60"]:
        count = 0
        connect = pymysql.connect(host='localhost', port=0, db='Coin_'+interval, user='root', passwd='Rladmswhd@1', autocommit=True)
        cursor = connect.cursor()
        for code in tickers:
            coin_symbol = code[code.index('-') + 1:]
            sql = "create table if not exists `"+coin_symbol+"_price_"+interval+"` (" \
                  "`date` datetime, " \
                  "`volumn` int unsigned default 0 not null," \
                  "`close` decimal(11,2)," \
                  "`diff_rate` decimal(10,5)," \
                  "PRIMARY KEY(`date`));"
            cursor.execute(sql)
            update_price_each(code, cursor, interval)
            if count == 1:
                break
            count += 1
        connect.close()

def drop_all_tables():
    connect = pymysql.connect(host='localhost', port=0, db='Coin_week',
                                user='root', passwd='Rladmswhd@1', autocommit=True)
    for interval in ["week", "day", "minute240", "minute60"]:
        cursor = connect.cursor()
        sql = "DROP DATABASE `Coin_"+interval+"`;"
        cursor.execute(sql)
        sql = "CREATE DATABASE `Coin_"+interval+"`;"
        cursor.execute(sql)
    connect.close()

def plot_chart():
    connect = pymysql.connect(host='localhost', port=0, db='Coin_week', user='root', passwd='Rladmswhd@1',
                              autocommit=True)
    cursor = connect.cursor()
    sql = "select * from BTC_price_week"
    cursor.execute(sql)
    result = cursor.fetchall()
    price_list = list()
    for i in result:
        price_list.append(float(i[2]))
    plt.plot(price_list)
    plt.show()
    connect.close()
