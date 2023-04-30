"""
Main script for algo1
"""

import pandas as pd
from rsi import RSIStrategy
from bb import BollingerBandsStrategy
from finance_database import Database


class Algo1:
    def __init__(self,ticker: str, start_date=None,end_date=None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
    def rsi(self)->pd.Series:
        rsi_instance = RSIStrategy(ticker = self.ticker,start_date=self.start_date,end_date=self.end_date)
        rsi_data = rsi_instance.get_data()['RSI']
        return rsi_data
    def BollingerBands(self):
        bollingerbands_instance = BollingerBandsStrategy(ticker = self.ticker,
                                                         start_date=self.start_date,end_date=self.end_date)
        bollingerbands_data = bollingerbands_instance.get_data()
        return bollingerbands_data

    def generate_signals(self):
        data = Database.get_price_data(self,ticker = self.ticker,start=self.start_date,end=self.end_date)['Adj Close']

        lower_band = Algo1.BollingerBands(self)['Lower']
        upper_band = Algo1.BollingerBands(self)['Upper']
        rsi = Algo1.rsi(self)

        buy_signal = (rsi < 30) & (data[1] < lower_band)
        sell_signal = (rsi > 70) & (data[1] > upper_band)

        signals = pd.DataFrame(buy_signal.index, columns=['Date'])

        buy_signal_list = buy_signal.astype(int).tolist()
        signals[self.ticker + '_Buy'] = buy_signal_list
        sell_signal_list = sell_signal.astype(int).tolist()
        signals[self.ticker + '_Sell'] = sell_signal_list

        k = print("h")



if __name__== '__main__':
    ticker_code = 'TSLA'
    k = Algo1(ticker=ticker_code,start_date='2020-02-01',end_date='2023-04-28')
    f=k.rsi()
    f1=k.BollingerBands()
    f2 = k.generate_signals()


