"""
Main script for algo1
"""

import pandas as pd
# pylint: disable=import-error
from rsi import RSIStrategy
from bb import BollingerBandsStrategy
# pylint: disable=import-error
from finance_database import Database


class Algo1:
    """
    A class representing an algorithm for generating trading signals based on
    Relative Strength Index (RSI) and Bollinger Bands strategies.

    Attributes:
    -----------
    ticker : str
        The ticker symbol of the financial instrument.
    start_date : str or None
        The start date for retrieving price data. If None, the default is None.
    end_date : str or None
        The end date for retrieving price data. If None, the default is None.
    tickers_list : list or None
        A list of ticker symbols for multiple financial instruments. If None, the default is None.

    Methods:
    --------
    rsi() -> pd.Series:
        Calculates the Relative Strength Index (RSI) for the specified ticker and date range.

    BollingerBands() -> pd.DataFrame:
        Retrieves Bollinger Bands data for the specified ticker and date range.

    generate_signals() -> pd.DataFrame:
        Generates buy and sell signals based on RSI and Bollinger Bands strategies.

    Algo1_loop() -> list:
        Executes the algorithm for multiple tickers and returns a list of signals for each ticker.
    """
    def __init__(self,ticker: str, start_date=None,end_date=None, tickers_list=None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
    def rsi(self)->pd.Series:
        """
        Calculates the Relative Strength Index (RSI) for the specified ticker and date range.

        Returns:
        -------
        rsi_data : pd.Series
            Series containing the RSI values.
        """
        rsi_instance = RSIStrategy(ticker = self.ticker,
                                   start_date=self.start_date,
                                   end_date=self.end_date)
        rsi_data = rsi_instance.get_data()['RSI']
        return rsi_data
    def bollinger_bands(self):
        """
        Retrieves Bollinger Bands data for the specified ticker and date range.

        Returns:
        -------
        bollingerbands_data : pd.DataFrame
            DataFrame containing the Bollinger Bands data.
        """
        bollingerbands_instance = BollingerBandsStrategy(ticker = self.ticker,
                                                         start_date=self.start_date,
                                                         end_date=self.end_date)
        bollingerbands_data = bollingerbands_instance.get_data()
        return bollingerbands_data

    def generate_signals(self):
        """
        Generates buy and sell signals based on RSI and Bollinger Bands strategies.

        Returns:
        -------
        signals : pd.DataFrame
            DataFrame containing the buy and sell signals.
        """
        data = Database.get_price_data(self,ticker = self.ticker,
                                       start=self.start_date,
                                       end=self.end_date)['Adj Close']

        lower_band = Algo1.bollinger_bands(self)['Lower']
        upper_band = Algo1.bollinger_bands(self)['Upper']
        rsi = Algo1.rsi(self)

        current_price = data.values

        rsi_aligned = rsi.reindex(data.index).values
        lower_band_aligned = lower_band.reindex(data.index).values
        upper_band_aligned = upper_band.reindex(data.index).values

        buy_signal = (rsi_aligned < 30) & (current_price < lower_band_aligned)
        sell_signal = (rsi_aligned > 70) & (current_price > upper_band_aligned)

        signals = pd.DataFrame(data.index, columns=['Date'])

        buy_signal_list = buy_signal.astype(int).tolist()
        signals[self.ticker + '_Buy'] = buy_signal_list
        sell_signal_list = sell_signal.astype(int).tolist()
        signals[self.ticker + '_Sell'] = sell_signal_list

        return signals

    def algo1_loop(self):
        """
        Executes the algorithm for multiple tickers. The function returns a
        list with the buying/selling signals.
        """

        signals_list = []

        for ticker1 in self.tickers_list:
            instance_1 = Algo1(ticker=ticker1, start_date=self.start_date,end_date=self.end_date)
            signals_1 = instance_1.generate_signals()
            signals_list.append(signals_1)

        return signals_list
