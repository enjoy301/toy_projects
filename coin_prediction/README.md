# 코인 가격 예측 프로그램 제작
# 1. 주요 사용 모듈
***
## 1.1 pyupbit
***
### 1.1.1 설치 방법
```
pip install pyupbit
```
***
### 1.1.2 import 방법
```
import pyupbit
```
***
### 1.1.3 주요 함수들
* __get_tickers__
    ```
    print(pyupbit.get_tickers())
    ```
  *모든 암호화폐의 목록 얻어옴*
  
  *인자로 fiat를 주면 특정 시장만 얻어옴*
  ```
  print(pyupbit.get_tickers(fiat="KRW"))
  ```
  *KRW/BTC/USDT 가능*
  
* __get_ohlcv__
    ```
    df = pyupbit.get_ohlcv("KRW-BTC")
    ```
