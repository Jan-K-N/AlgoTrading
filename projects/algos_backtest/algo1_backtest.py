"""
Main script for algo1 backtest.
"""
import sys
import pandas as pd
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
            price_data.append(data["Open"])


        algo1_data = Algo1_backtest.run_algo1(self)

        df_buy_signals = pd.DataFrame(columns=['Ticker', 'Buy Signal'])
        df_sell_signals = pd.DataFrame(columns=['Ticker', 'Sell Signal'])

        for df in algo1_data:
            ticker = df['Ticker'][0]
            df_buy = df.loc[df['Buy'] == 1]
            df_sell = df.loc[df['Sell'] == -1]

            df_buy_signals = pd.concat(
                [df_buy_signals, pd.DataFrame({'Ticker': [ticker] * len(df_buy), 'Buy Signal': df_buy.index})])
            df_sell_signals = pd.concat(
                [df_sell_signals, pd.DataFrame({'Ticker': [ticker] * len(df_sell), 'Sell Signal': df_sell.index})])


        # We will now make the buy prices:
        buy_prices_list = []
        for ticker1 in self.tickers_list:
            for i in range(0,len(df_buy_signals)):
                if df_buy_signals['Ticker'].iloc[i] == ticker1:
                    # Now add the buy date:
                    df_buy_signals['Buy date'] = pd.to_datetime(df_buy_signals['Buy Signal']).dt.date + pd.DateOffset(days=1)

        for ticker1 in self.tickers_list:

            for j in range(0,len(df_buy_signals)):
                if df_buy_signals['Ticker'].iloc[j] == ticker1:
                    for i in range(0, len(self.tickers_list)):
                        # for ticker1 in self.tickers_list:
                        #     if df_buy_signals['Ticker'].iloc[j] == ticker1:
                        mask = df_buy_signals['Buy date'].iloc[j]  # Assuming 'Buy date' contains the condition
                        value = None  # Initialize value as None
                        while value is None:  # Loop until a non-weekend value is found
                            if mask.weekday() < 5:  # Check if the date is a weekday
                                if mask in price_data[i]:  # Check if the date is present in price_data[i]
                                    value = price_data[i][mask]  # Get the corresponding value from price_data
                                else:
                                    mask += pd.DateOffset(days=1)  # Move to the next day
                            else:
                                mask += pd.DateOffset(days=1)  # Move to the next day
                        df_buy_signals.loc[
                            df_buy_signals['Buy date'] == df_buy_signals['Buy date'].iloc[j], 'Buy price'] = value

        print("h")

        return

if __name__ == '__main__':
    instance = Algo1_backtest(start_date = '2020-01-01',end_date='2021-01-01',tickers_list=['TSLA','AAPL'])
    output = instance.run_algo1()
    backtest = instance.backtest()
