from .models import orderbook
import requests
import json
from datetime import datetime
import time

def parse_upbit():
    start_time = time.time()
    url = "https://api.upbit.com/v1/orderbook"
    querystring = {"markets": ["KRW-BTC"]}
    headers = {"Accept": "application/json"}
    while time.time()-start_time <= 59:
        response = (json.loads(requests.request("GET", url, headers=headers, params=querystring).text))[0]
        value = float(response['total_ask_size']) - float(response['total_bid_size'])
        data = (round(value, 5), datetime.fromtimestamp(response['timestamp'] / 1000))
        orderbook(amount_ask_bid=data[0], time=data[1]).save()


def crontab_job():
    #parse_upbit()
    pass