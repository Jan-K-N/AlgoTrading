"""
Main script for algo2. This algo will find signals in the same way
as algo1. However, after the signals are found, this algo1
will do some more analysis.
"""
import sys
from algo1 import Algo1
sys.path.insert(1,'/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
from finance_database import Database
from datetime import datetime,timedelta
import pandas as pd

class Algo2:
    def __init__(self,ticker=None, start_date=None,end_date=None, tickers_list=None,
                 days_back = None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
        self.days_back = days_back
        self.db_instance = Database(start=start_date, end=end_date, ticker=ticker)  # Create an instance of the Database class

    def run_algo1(self):
        instance_algo1 = Algo1(start_date=self.start_date,
                               end_date=self.end_date,
                               tickers_list=self.tickers_list)
        algo1_output = instance_algo1.algo1_loop()

        return algo1_output

    def return_data(self):
        """
        Private method for pulling return data from our finance database for multiple tickers.

        Returns:
            A list of DataFrames, where each DataFrame contains return data for a specific ticker.
        """
        return_data_list = []  # Create an empty list to store return data DataFrames for each ticker

        for ticker in self.tickers_list:
            # Calculate the start date based on self.days_back
            start_date = datetime.strptime(self.start_date, "%Y-%m-%d") - timedelta(days=self.days_back)
            start_date = start_date.strftime("%Y-%m-%d")  # Convert back to string format

            return_data = self.db_instance.compute_stock_return(start=start_date, end=self.end_date, ticker=ticker)

            return_data_list.append(return_data)  # Append return data DataFrame to the list

        return return_data_list

    def random_forest(self):
        """
        Function for creating a random forest for the stock return.
        Input to the rf should be the stock returns from the suggested
        stocks from algo1. If there is a buy/sell signal for a given date,
        we pull the return data for the given stock up till that day.
        Then we run a random forest model to predict the probability
        of a up/down movement.

        Returns:

        """
        algo1_signals = self.run_algo1()

        # Initialize empty lists to store DataFrames for buy and sell signals
        buy_dataframes = []
        sell_dataframes = []

        for df in algo1_signals:
            # Access the "buy" and "sell" columns by name
            ticker_column = df.iloc[:, 0]
            buy_column = df.iloc[:, 1]
            sell_column = df.iloc[:, 2]

            # Create empty DataFrames to store the filtered buy and sell data
            filtered_buy_df = pd.DataFrame(columns=['Ticker', 'Buy_Date'])
            filtered_sell_df = pd.DataFrame(columns=['Ticker', 'Sell_Date'])

            # Iterate through buy and sell signals
            for date, ticker, buy_signal, sell_signal in zip(df.index, ticker_column, buy_column, sell_column):
                if buy_signal == 1:
                    buy_date = date  # Update buy_date when a "buy" signal is found
                    ticker_name = ticker
                    filtered_buy_df = pd.concat(
                        [filtered_buy_df, pd.DataFrame({'Ticker': [ticker_name], 'Buy_Date': [buy_date]})],
                        ignore_index=True)
                if sell_signal == -1:
                    sell_date = date  # Update sell_date when a "sell" signal is found
                    ticker_name = ticker
                    filtered_sell_df = pd.concat(
                        [filtered_sell_df, pd.DataFrame({'Ticker': [ticker_name], 'Sell_Date': [sell_date]})],
                        ignore_index=True)

            # Append the filtered buy and sell DataFrames to their respective lists
            buy_dataframes.append(filtered_buy_df)
            sell_dataframes.append(filtered_sell_df)

        # Now we can create some return vectors, where the end-date point is given by
        # the last date, which we get from buy_dataframes and sell_dataframes.

        print("k")
if __name__ == '__main__':
    instance = Algo2(start_date='2023-01-01',end_date='2023-08-21',tickers_list=['TSLA','AAPL','AMZN'],
                     days_back=0)
    f = instance.random_forest()
    k = instance.return_data()
