"""
Main script for the algo1 backtest frontend.
"""
import sys
sys.path.insert(0,'/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos_backtest')

from algo1_backtest import Algo1Backtest

instance_backtest = Algo1Backtest(start_date = '2010-02-01',end_date='2023-01-01',
                                  tickers_list = ['TSLA'])

k = instance_backtest.backtest_returns()
