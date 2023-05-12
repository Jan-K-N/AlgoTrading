"""
Main script for algo1 backtest.
"""
import sys
sys.path.insert(0,'/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos')
sys.path.insert(1,'/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
from algo1 import Algo1
from finance_database import Database

class Algo1_backtest:
    """
    A class to backtest Algo1. The class uses the output from Algo1.
    """
    def __init__(self,start_date=None,end_date=None,tickers_list=None):
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list

    def run_algo1(self):
        instance_algo1 = Algo1(start_date=self.start_date,
                               end_date=self.end_date,
                               tickers_list=self.tickers_list)
        algo1_output = instance_algo1.algo1_loop()

        return algo1_output

    def backtest(self):
        price_data = []

        for ticker in self.tickers_list:

            data = Database.get_price_data(self,start=self.start_date,end=self.end_date,ticker=ticker)
            price_data.append(data["Adj Close"])


        algo1_data = Algo1_backtest.run_algo1(self)

        buy_signals = []
        sell_signals = []
        for i in range(0,len(algo1_data)):
            if algo1_data['Buy'] == 1:
                buy_signals.append(price_data.index[i])
            # Code here.


        # Calcuæate returns:
        returns = None
        


        return

if __name__ == '__main__':
    instance = Algo1_backtest(start_date = '2020-01-01',end_date='2021-01-01',tickers_list=['TSLA','AAPL'])
    output = instance.run_algo1()
    backtest = instance.backtest()

    print("k")