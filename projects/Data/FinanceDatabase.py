"""
Main Finance Database script.
"""
import yfinance as yf
from datetime import date, timedelta

class Database():
    def __init__(self, start=None, end=None, ticker='TSLA'):
        if end is None:
            end = date.today().strftime("%Y-%m-%d")
        if start is None:
            start = (date.today() - timedelta(days=3*365)).strftime("%Y-%m-%d")
        self.start = start
        self.end = end
        self.ticker = ticker
        
    def get_price_data(self, start=None, end=None, ticker=None):
        if ticker is not None:
            self.ticker = ticker
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        ticker_data = yf.download(tickers=self.ticker, start=self.start, end=self.end)
        return ticker_data
    
    def get_dividend_data(self, start=None, end=None, ticker=None):
        if ticker is not None:
            self.ticker = ticker
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        ticker_info = yf.Ticker(self.ticker)
        ticker_div = ticker_info.dividends
        return ticker_div

if __name__ == '__main__':
    db = Database()
    print('Done')


    
db1 = Database()
db1.get_price_data(ticker = 'FLS.CO')
    
#class Database_Economic():
#    # Code here.
#        # Database containing economic variables from FRED etc.


