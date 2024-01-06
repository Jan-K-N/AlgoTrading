"""
The main script for the Algo1.

This script defines the Algo1 class for generating trading signals based
on Relative Strength Index (RSI) and Bollinger Bands strategies.
It provides methods for calculating RSI, Bollinger Bands, generating
buy and sell signals, and executing the algorithm for multiple tickers.
"""
# pylint: disable=import-error.
# pylint: disable=wrong-import-position.
import sys
import pandas as pd
import numpy as np
#sys.path.insert(0,'/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/strategies')
sys.path.insert(0,'/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
from bb import BollingerBandsStrategy
from rsi import RSIStrategy
from finance_database import Database

# pylint: disable=too-many-arguments.
class Algo1:
    """
    Algo1 - Algorithm for Trading Signal Generation.

    The Algo1 class is designed to generate trading signals based on
    the Relative Strength Index (RSI) and Bollinger Bands strategies.
    It provides methods for calculating RSI, Bollinger Bands,
    generating buy and sell signals, and executing the algorithm
    for multiple tickers.

    Attributes:
    -----------
        ticker (str):
            The ticker symbol of the financial instrument.
        start_date (str or None):
            The start date for retrieving price data. If None, the default is None.
        end_date (str or None):
            The end date for retrieving price data. If None, the default is None.
        tickers_list (list or None):
            A list of ticker symbols for multiple financial instruments.
            If None, the default is None.
        consecutive_days (int or None):
            The number of consecutive days the conditions should be met
            to generate signals. If None, the default is None.
        consecutive_days_sell (int or None):
            The number of consecutive days the sell conditions should be met
            to generate signals. If None, the default is None.

    Methods:
    --------
    rsi() -> pd.Series:
        Calculates the Relative Strength Index (RSI) for the specified ticker and date range.

    bollinger_bands() -> pd.DataFrame:
        Retrieves Bollinger Bands data for the specified ticker and date range.

    generate_signals() -> pd.DataFrame:
        Generates buy and sell signals based on RSI and Bollinger Bands strategies.
        The signals are based on the specified consecutive days.

    algo1_loop() -> list:
        Executes the algorithm for multiple tickers and generates
        buying/selling signals for each ticker.
    """

    def __init__(self, ticker=None, start_date=None,
                 end_date=None, tickers_list=None, consecutive_days=None,
                 consecutive_days_sell=None):
        """
        Initialize the Algo1 instance.

        Parameters:
        -----------
            ticker (str):
                The ticker symbol of the financial instrument.
            start_date (str or None):
                The start date for retrieving price data. If None, the default is None.
            end_date (str or None):
                The end date for retrieving price data. If None, the default is None.
            tickers_list (list or None):
                A list of ticker symbols for multiple financial instruments. If None,
                the default is None.
            consecutive_days (int or None):
                The number of consecutive days the conditions should be met to
                generate signals. If None, the default is None.
            consecutive_days_sell (int or None):
                The number of consecutive days the sell conditions should be met
                to generate signals. If None, the default is None.
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
        self.consecutive_days = consecutive_days
        self.consecutive_days_sell = consecutive_days_sell

    def rsi(self) -> pd.Series:
        """
        Calculates the Relative Strength Index (RSI) for the specified ticker and date range.

        Returns:
        -------
            rsi_data (pd.Series):
                Series containing the RSI values.
        """
        rsi_instance = RSIStrategy(ticker=self.ticker,
                                   start_date=self.start_date,
                                   end_date=self.end_date)
        rsi_data = rsi_instance.get_data()['RSI']
        return rsi_data

    def bollinger_bands(self):
        """
        Retrieves Bollinger Bands data for the specified ticker and date range.

        Returns:
        -------
            bollingerbands_data (pd.DataFrame):
                DataFrame containing the Bollinger Bands data.
        """
        bollingerbands_instance = BollingerBandsStrategy(ticker=self.ticker,
                                                         start_date=self.start_date,
                                                         end_date=self.end_date)
        bollingerbands_data = bollingerbands_instance.get_data()
        return bollingerbands_data

    def generate_signals(self):
        """
        Generates buy and sell signals based on RSI and Bollinger Bands strategies.

        Returns:
        -------
            signals (pd.DataFrame):
                DataFrame containing the buy and sell signals.
        """
        data = Database.get_price_data(self, ticker=self.ticker,
                                       start=self.start_date,
                                       end=self.end_date)['Adj Close']

        lower_band = self.bollinger_bands()['Lower']
        upper_band = self.bollinger_bands()['Upper']
        rsi = self.rsi()

        current_price = data.values

        rsi_aligned = rsi.reindex(data.index).values
        lower_band_aligned = lower_band.reindex(data.index).values
        upper_band_aligned = upper_band.reindex(data.index).values

        consecutive_buy = 0
        consecutive_sell = 0
        buy_signal = [0] * len(data)
        sell_signal = [0] * len(data)

        for i in range(len(data)):
            if not np.isnan(rsi_aligned[i]) and not np.isnan(
                    current_price[i]) and not np.isnan(lower_band_aligned[i]):
                if (rsi_aligned[i] < 30) and (current_price[i] < lower_band_aligned[i]):
                    consecutive_buy += 1
                    consecutive_sell = 0
                elif (rsi_aligned[i] > 70) and (current_price[i] > upper_band_aligned[i]):
                    consecutive_sell += 1
                    consecutive_buy = 0
                else:
                    consecutive_buy = 0
                    consecutive_sell = 0

                buy_signal[i] = 1 if (
                            self.consecutive_days is not None
                            and consecutive_buy >= self.consecutive_days) else 0
                sell_signal[i] = -1 if (
                            self.consecutive_days_sell is not None and
                            consecutive_sell >= self.consecutive_days_sell) else 0
            else:
                consecutive_buy = 0
                consecutive_sell = 0

        signals = pd.DataFrame(data.index, columns=['Date'])
        signals[self.ticker + '_Buy'] = buy_signal
        signals[self.ticker + '_Sell'] = sell_signal

        return signals

    def algo1_loop(self) -> list:
        """
        Executes the algorithm for multiple tickers and generates
        buying/selling signals for each ticker.

        Returns:
        -------
            signals_list (list of pd.DataFrame):
                A list of pandas DataFrames, each containing the
                buying/selling signals for a ticker. Each DataFrame has 3 columns:
                'Date', 'Buy', and 'Sell', where 'Buy' and 'Sell' are
                binary indicators of whether a buy or a sell signal was
                generated on that date for the corresponding ticker.
        """
        signals_list = []

        for ticker1 in self.tickers_list:
            try:
                instance_1 = Algo1(ticker=ticker1,
                                   start_date=self.start_date,
                                   end_date=self.end_date)
                signals_1 = instance_1.generate_signals()
            except KeyError as error:
                print(f"KeyError for the {ticker1}: {str(error)}")
                continue
            except ValueError as error:
                print(f"ValueError for the {ticker1}: {str(error)}")
                continue

            condition1_buy = signals_1[ticker1 + '_Buy'] == 1
            condition2_sell = signals_1[ticker1 + '_Sell'] == 1

            combined_condition = condition1_buy | condition2_sell

            extracted_rows = signals_1[combined_condition]

            df_signals = pd.DataFrame()
            df_signals["Ticker"] = [ticker1] * len(extracted_rows)
            df_signals["Buy"] = [1 if b else "" for b in extracted_rows[ticker1 + '_Buy']]
            df_signals["Sell"] = [-1 if s else "" for s in extracted_rows[ticker1 + '_Sell']]
            df_signals.index = extracted_rows['Date']

            if not df_signals.empty:
                signals_list.append(df_signals)
        return signals_list

if __name__ == "__main__":
    instance = Algo1(tickers_list=['TSLA','FLS.CO'],start_date="2022-01-01",end_date="2023-01-01")
    k = instance.algo1_loop()
    print("k")