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

    def backtest_prices(self):
        """
        Method to compute/get the prices from the buy/sell signals from Algo1.
        :return:
        """

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

        # We will now make the buy/sell prices:
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

            # Append to the list:
            buy_prices_list.append(filtered_df)

        sell_prices_list = []

        for ticker1 in self.tickers_list:
            filtered_df_sell = df_sell_signals[df_sell_signals['Ticker'] == ticker1].copy()
            filtered_df_sell['Sell date'] = pd.to_datetime(filtered_df_sell['Sell Signal']).dt.date + pd.DateOffset(days=1)

            for j in range(len(filtered_df_sell)):
                for i in range(len(price_data)):
                    mask = filtered_df_sell['Sell date'].iloc[j]
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
                    filtered_df_sell['Sell date'].iloc[j] = mask
                filtered_df_sell.loc[filtered_df_sell['Sell date'] == mask,'Sell price'] = value

            # Append to list:
            sell_prices_list.append(filtered_df_sell)

        return [buy_prices_list, sell_prices_list]

    def backtest_returns(self):
        """
        Method to compute the backtested returns. The method contains a variable
        to "control" the different return cases. Algo1 gives gives to three return
        cases. Case 1: We only go long in the asset, Case 2: We only short the asset or
        Case 3 we do both.
        :return:
        """

        prices = Algo1_backtest.backtest_prices(self)

        # returns_list = []
        #
        # for df_buy in prices[0]:
        #     for ticker1 in self.tickers_list:
        #         if df_buy['Ticker'].iloc[0] == ticker1:
        #             returns_df = pd.DataFrame(columns=['Ticker', 'Returns'])  # Create an empty dataframe for returns
        #
        #             for j in range(len(df_buy)):
        #                 timestamp1 = df_buy['Buy date'].iloc[j]
        #                 # Find corresponding sell dataframe
        #                 for df_sell in prices[1]:  # Sell prices
        #                     if df_sell['Ticker'].iloc[0] == ticker1:
        #                         df_sell = pd.DataFrame(df_sell)  # Convert list_iterator to dataframe
        #                         # Compare timestamp with corresponding sell date
        #                         sell_date = df_sell['Sell date'].iloc[0]
        #                         if timestamp1 < sell_date:
        #                             # Drop sell dates before the first buy date
        #                             df_sell = df_sell[df_sell['Sell date'] <= timestamp1]
        #
        #                             # Compute returns
        #                             buy_price = df_buy.loc[df_buy['Buy date'] == timestamp1, 'Buy price'].iloc[0]
        #                             sell_price = None  # Initialize sell_price
        #                             if len(df_sell) > 0:
        #                                 sell_price = df_sell.loc[
        #                                     df_sell['Sell date'] == timestamp1, 'Sell price'].values
        #                                 if len(sell_price) > 0:
        #                                     sell_price = sell_price[0]
        #                                 else:
        #                                     sell_price = None
        #
        #                             if sell_price is not None:
        #                                 returns = (buy_price - sell_price) / buy_price
        #                                 returns_df = returns_df.append({'Ticker': ticker1, 'Returns': returns},
        #                                                                ignore_index=True)
        #
        #             returns_list.append(returns_df)

        import pandas as pd

        returns_list = []

        for ticker1 in self.tickers_list:
            for df_buy in prices[0]:
                if df_buy['Ticker'].iloc[0] == ticker1:
                    returns_df = pd.DataFrame(columns=['Ticker', 'Returns'])  # Create an empty dataframe for returns

                    for j in range(len(df_buy)):
                        timestamp1 = df_buy['Buy date'].iloc[j]
                        buy_price = df_buy.loc[df_buy['Buy date'] == timestamp1, 'Buy price'].iloc[0]
                        sell_price = None
                        units = 1  # Buy 1 unit of the stock

                        for df_sell in prices[1]:  # Sell prices
                            if df_sell['Ticker'].iloc[0] == ticker1:
                                df_sell = pd.DataFrame(df_sell)  # Convert list_iterator to dataframe
                                sell_date = df_sell[df_sell['Sell date'] == timestamp1]

                                if not sell_date.empty:
                                    sell_price = sell_date.iloc[0]['Sell price']
                                    break  # Exit the loop once sell_price is found

                        if sell_price is not None:
                            returns = (sell_price - buy_price) * units / buy_price
                            returns_df.loc[len(returns_df)] = [ticker1, returns]  # Append new row to returns_df

                    returns_list.append(returns_df)

        # Now the returns_list contains dataframes with returns for each ticker

        # Now the returns_list contains dataframes with returns for each ticker

        print("f")

        return k
if __name__ == '__main__':
    instance = Algo1_backtest(start_date = '2015-01-01',end_date='2022-01-01',tickers_list=['TSLA','AAPL','FLS.CO'])
    output = instance.run_algo1()
    backtest = instance.backtest_prices()
    backtest_returns1 = instance.backtest_returns()
