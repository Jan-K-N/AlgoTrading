"""
Main script for algo2. This algo will find signals in the same way
as algo1. However, after the signals are found, this algo1
will do some more analysis.
"""
from algo1 import Algo1

class Algo2:
    def __init__(self,ticker=None, start_date=None,end_date=None, tickers_list=None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list

    def run_algo1(self):
        instance_algo1 = Algo1(start_date=self.start_date,
                               end_date=self.end_date,
                               tickers_list=self.tickers_list)
        algo1_output = instance_algo1.algo1_loop()

        return algo1_output

    def corr_algo1(self):
        """
        Function for checking the correlation of the stocks with signals with economic variables.

        Returns:

        """
