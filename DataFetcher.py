from pytrends.request import TrendReq
from finvizfinance.quote import finvizfinance
import requests
from datetime import datetime, timedelta
"""
Pulls data on queried stock from google trends, finviz, and reddit 
"""
class DataFetcher:

    #init data fetcher object for a specific stock (ticker_symbol)
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol

    """
    Queries google trends api to fetch recent popularity data on requested stock

    Returns: DataFrame of requested trends data
    """ 
    def fetch_trends(self): 
        pytrends = TrendReq(hl='en-US', tz=360) 
        kw_list = [self.ticker_symbol] 

        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        one_month_ago = (datetime.today() - timedelta(days=31)).strftime("%Y-%m-%d")

        
        pytrends.build_payload(kw_list, cat=0, timeframe=' '.join([one_month_ago, yesterday]), geo='US', gprop='') 
        
        data = pytrends.interest_over_time()
        
        return data


    """
    Queries FinViz api to fetch information related to requested stock

    Datapoints:
        Short Float: % of shares which are currently short sold
        Short Ratio: Days needed for short sellers to buy back position
        Short Interest: Total number of short sold shares
        Rel Vol: FinViz attention metric
        Volatility W/M: weekly/monthly volatility
        ATR(14): another volatilty metric
        Change: stock price change for today only

    Returns: DataFrame news headlines(with links), list of short info
    """ 

    def fetch_finviz(self):
        
        stock = finvizfinance(self.ticker_symbol.lower()) #finviz object for stock

        fun = stock.ticker_fundament() #get the other datapoints

        data = [fun["Short Float"], fun["Short Ratio"], fun["Short Interest"], fun["Rel Volume"], fun["Change"], fun["Volatility W"], fun["Volatility M"], fun["ATR (14)"]]

        return data




    """
    Queries reddit public json endpoint over HTTP and grabs posts about queried stock

    returns json object of posts, with text
    """
    def fetch_reddit(self):

        #http headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        }
        
        url = f"https://www.reddit.com/search.json?q={self.ticker_symbol}&limit=30" #url

        data = requests.get(url, headers=headers).json() #make request and get json of body
        
        return data


    





