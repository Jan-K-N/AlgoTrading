import yfinance as yf
import pandas as pd
import numpy as np


class BollingerBandsStrategy:

    def __init__(self, ticker, start_date, end_date, window=20, dev_factor=2):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.window = window
        self.dev_factor = dev_factor
        self.df = self.get_data()

    def get_data(self):
        df = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        df['MA'] = df['Close'].rolling(self.window).mean()
        df['Upper'] = df['MA'] + self.dev_factor * df['Close'].rolling(self.window).std()
        df['Lower'] = df['MA'] - self.dev_factor * df['Close'].rolling(self.window).std()
        return df.dropna()

    def backtest(self):
        self.df['Position'] = np.nan
        self.df.loc[self.df['Close'] < self.df['Lower'], 'Position'] = 1
        self.df.loc[self.df['Close'] > self.df['Upper'], 'Position'] = -1
        self.df['Position'].ffill(inplace=True)
        self.df['Returns'] = self.df['Close'].pct_change() * self.df['Position'].shift(1)
        self.df['Cumulative Returns'] = (1 + self.df['Returns']).cumprod()
        self.df.dropna(inplace=True)
        return self.df['Cumulative Returns'].iloc[-1]
