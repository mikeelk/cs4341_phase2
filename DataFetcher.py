from pytrends.request import TrendReq
import yfinance as yf
import pandas
import time
import random


def fetch_yfin():
    ticker_symbol = 'AAPL'

    data = yf.download(ticker_symbol, start='2024-01-01', end='2024-12-31')

    print(data.head())

def fetch_trends(): 
    pytrends = TrendReq(hl='en-US', tz=360) 
    kw_list = ["TSLA"] 
    
    pytrends.build_payload(kw_list, cat=0, timeframe='today 1-m', geo='', gprop='') 
    
    data = pytrends.interest_over_time()
    
    print(data)

def main():
    fetch_yfin()





if __name__ == "__main__":
    main()


