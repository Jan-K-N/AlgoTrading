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
            filtered_df = df_buy_signals[df_buy_signals['Ticker'] == ticker1].copy()
            filtered_df['Buy date'] = pd.to_datetime(filtered_df['Buy Signal']).dt.date + pd.DateOffset(days=1)

            for j in range(len(filtered_df)):
                for i in range(0, len(price_data)):
                    mask = filtered_df['Buy date'].iloc[j]
                    value = None
                    while value is None:
                        if mask.weekday() < 5:
                            if mask in price_data[i]:
                                value = price_data[i][mask]
                                break
                        if value is None:
                            mask += pd.DateOffset(days=1)
                    else:
                        mask += pd.DateOffset(days=1)
                    filtered_df['Buy date'].iloc[j] = mask
                filtered_df.loc[filtered_df['Buy date'] == mask, 'Buy price'] = value

            # Append to the list
            buy_prices_list.append(filtered_df)

        print("k")

        return buy_prices_list

if __name__ == '__main__':
    instance = Algo1_backtest(start_date = '2015-01-01',end_date='2022-01-01',tickers_list=['TSLA','AAPL','FLS.CO'])
    output = instance.run_algo1()
    backtest = instance.backtest()
    print("k")
