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
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

        for prediction_dataframe in algo1_signals:
            # Access the "buy" and "sell" columns by name
            ticker_column = prediction_dataframe.iloc[:, 0]
            buy_column = prediction_dataframe.iloc[:, 1]
            sell_column = prediction_dataframe.iloc[:, 2]

            # Create empty DataFrames to store the filtered buy and sell data
            filtered_buy_df = pd.DataFrame(columns=['Ticker', 'Buy_Date'])
            filtered_sell_df = pd.DataFrame(columns=['Ticker', 'Sell_Date'])

            # Iterate through buy and sell signals
            for date, ticker, buy_signal, sell_signal in zip(prediction_dataframe.index, ticker_column, buy_column, sell_column):
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
        returns = self.return_data()

        selected_buy_series_list = []
        selected_sell_series_list = []

        for prediction_dataframe, df1, df2 in zip(buy_dataframes, returns, sell_dataframes):
            buy_column = prediction_dataframe.iloc[:, 1]
            sell_column = df2.iloc[:, 1]

            for i in range(0, len(buy_column)):
                buy_date = buy_column[i]
                if buy_date in df1.index:
                    selected_buy_series = df1.loc[df1.index <= buy_date]
                    # Add a new column with the last index value
                    selected_buy_series['buy_signal_date'] = buy_date
                    selected_buy_series_list.append(selected_buy_series)
                else:
                    # If 'buy_date' is not in the DataFrame's index, append an empty series:
                    selected_buy_series_list.append(pd.Series())

            for j in range(0, len(sell_column)):
                sell_date = sell_column[j]
                if sell_date in df1.index:
                    selected_sell_series = df1.loc[df1.index <= sell_date]
                    # Add a new column with the last index value
                    selected_sell_series['sell_signal_date'] = sell_date
                    selected_sell_series_list.append(selected_sell_series)
                else:
                    selected_sell_series_list.append(pd.Series())

        for series in selected_buy_series_list:
            returns = series.iloc[:, 0].values
            price_movements = np.sign(np.diff(returns))
            price_movements = price_movements.reshape(-1,1)
            returns = returns[:-1]

            # Reshape "returns" to have two dimensions
            returns = returns.reshape(-1, 1)

            X_train, X_test, y_train, y_test = train_test_split(returns, price_movements, test_size=0.05, random_state=42)

            clf = RandomForestClassifier(n_estimators=1000,random_state=42)
            clf.fit(X_train,y_train)

            y_pred = clf.predict(X_test)
            y_pred = y_pred.reshape(-1,1)
            n = y_pred.shape[0]
            last_n_dates = series.index[-n:]
            # Create a structured array with two fields: "prediction" and "date"
            structured_array = np.empty(n, dtype=[('prediction', float), ('date', 'datetime64[ns]')])
            structured_array['prediction'] = y_pred[:, 0]
            structured_array['date'] = last_n_dates

            # Convert the structured array to a DataFrame
            prediction_dataframe = pd.DataFrame(structured_array)

            # Rename the columns if needed
            prediction_dataframe.columns = ['Prediction','Date']

        print(series)

if __name__ == '__main__':
    instance = Algo2(start_date='2023-01-01',end_date='2023-08-21',tickers_list=['TSLA','AAPL','AMZN'],
                     days_back=0)
    f = instance.random_forest()
    k = instance.return_data()
