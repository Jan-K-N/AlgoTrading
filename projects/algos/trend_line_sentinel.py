"""
The term "Sentinel" generally refers to a guard or watchman,
someone or something that stands watch or keeps vigil.
In the context of the algorithm name "TrendLine Sentinel,"
it implies that the algorithm acts as a vigilant observer or guardian of trends,
making decisions based on the information derived from linear regression lines
to protect or optimize the trading strategy.
"""

import pandas as pd
import numpy as np
import matplotlib as plt
import sys
sys.path.append("..")
from sklearn.linear_model import LinearRegression
from data.finance_database import Database

class sentinel:

    def __init__(self,start_date=None,
                 end_date=None,ticker=None,
                 tickers_list=None,window=50):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
        self.window = window
        self.signals = None

    def sentinel_data(self):
        """
        Method for pulling data from the finance database.
        Returns:

        """
        data = Database.get_price_data(self,ticker=self.ticker,start=self.start_date,
                                       end=self.end_date)['Adj Close']
        data = pd.DataFrame(data.values, index=data.index, columns=[self.ticker])

        return data

    def generate_signals(self):
        """
        Method for generating signals.
        Returns:

        """
        data = self.sentinel_data()
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0


        return signals




if __name__ == "__main__":
    instance = sentinel(start_date="2022-01-01",end_date="2023-01-01",
                        ticker="TSLA")
    k = instance.sentinel_data()


