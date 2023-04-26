"""
Main class for the technical indicator (TI) BollingerBands.
The script contains a backtest of a BB based trading
strategy.
"""

import yfinance as yf
import pandas as pd
import numpy as np
# pylint: disable=import-error.
from finance_database import Database

class BollingerBandsStrategy:

    def __init__(self, ticker, start_date, end_date, window=20, dev_factor=2,transaction_cost=0.1):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.window = window
        self.dev_factor = dev_factor
        self.transaction_cost = transaction_cost
        self.data = self.get_data()

    def get_data(self)->pd.DataFrame:
        """
        Retrieves price data from a database and calculates the moving average, upper
        and lower bands for a given ticker within a specific date range.
        Returns the resulting DataFrame with NaN values dropped.

        Returns:
        -------
        pandas.DataFrame: A DataFrame object containing the price data, moving average, upper
        and lower bands.

        Raises:
        -------
        ValueError: If the start date is after the end date.

        Examples:
        # Initialize an instance of the class with the required parameters
        instance = BollingerBandsStrategy(start_date='2022-01-01',
        end_date='2022-01-31', ticker='AAPL', window=20, dev_factor=2)

        # Call the method to retrieve the data
        data = instance.get_data()
        """
        data = Database.get_price_data(self,start=self.start_date, end=self.end_date,ticker=self.ticker)
        data['MA'] = data['Close'].rolling(self.window).mean()
        data['Upper'] = data['MA'] + self.dev_factor * data['Close'].rolling(self.window).std()
        data['Lower'] = data['MA'] - self.dev_factor * data['Close'].rolling(self.window).std()
        return data.dropna()

    def backtest(self) -> pd.DataFrame:
        """
        Simulates a trading strategy using the previously calculated price data, generates buy and sell signals based on the
        upper and lower bands, and calculates returns based on transaction costs. Returns a DataFrame containing the cumulative
        returns of the strategy and a boolean variable indicating if there is a buying signal for the given day.

        Returns:
        -------
        pandas.DataFrame: A DataFrame object containing the cumulative returns and buying signal variable.

        Examples:
        # Initialize an instance of the class with the required parameters
        instance = BollingerBandsStrategy(start_date='2022-01-01', end_date='2022-01-31', ticker='AAPL', window=20, dev_factor=2, transaction_cost=0.01)

        # Call the method to backtest the strategy
        data = instance.backtest()
        """
        self.data['Position'] = np.nan
        self.data.loc[self.data['Close'] < self.data['Lower'], 'Position'] = 1
        self.data.loc[self.data['Close'] > self.data['Upper'], 'Position'] = -1
        self.data['Transaction Cost'] = self.transaction_cost * self.data['Close'].diff().abs()
        self.data['Returns'] = (self.data['Close'].pct_change() - self.data['Transaction Cost']).shift(1) * self.data['Position']
        self.data['Cumulative Returns'] = (1 + self.data['Returns']).cumprod()

        data = self.data[['Cumulative Returns']]
        data['Buying Signal'] = self.data['Position'] == 1
        data['Selling Signal'] = self.data['Position'] == -1

        if self.data['Position'].iloc[-1] == 1:
            print("ALERT: Buying signal today")
        elif self.data['Position'].iloc[-1] == -1:
            print("ALERT: Selling signal today")

        return data


if __name__ == '__main__':
    k = BollingerBandsStrategy(ticker = 'TSLA', start_date='2022-01-01', end_date='2023-04-25')
    f = k.backtest()
