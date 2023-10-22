"""
Main script for the Algo1.
"""
# pylint: disable=import-error
# pylint: disable=wrong-import-position
import sys
sys.path.insert(1, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/strategies')
from bb import BollingerBandsStrategy
from rsi import RSIStrategy
sys.path.insert(2, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/strategies')
from finance_database import Database
import pandas as pd

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

    bollinger_bands() -> pd.DataFrame:
        Retrieves Bollinger Bands data for the specified ticker and date range.

    generate_signals() -> pd.DataFrame:
        Generates buy and sell signals based on RSI and Bollinger Bands strategies.

    algo1_loop() -> list:
        Executes the algorithm for multiple tickers. The function returns a
        single DataFrame with the buying/selling signals.
    """
    def __init__(self,ticker=None, start_date=None,end_date=None, tickers_list=None, consecutive_days=2):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
        self.consecutive_days = consecutive_days
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
        signals : pd.DataFrame
            DataFrame containing the buy and sell signals.
        """
        data = Database.get_price_data(self, ticker=self.ticker,
                                       start=self.start_date,
                                       end=self.end_date)['Adj Close']

        lower_band = Algo1.bollinger_bands(self)['Lower']
        upper_band = Algo1.bollinger_bands(self)['Upper']
        rsi = Algo1.rsi(self)

        current_price = data.values

        rsi_aligned = rsi.reindex(data.index).values
        lower_band_aligned = lower_band.reindex(data.index).values
        upper_band_aligned = upper_band.reindex(data.index).values

        consecutive_buy = 0
        consecutive_sell = 0
        buy_signal = []
        sell_signal = []

        for i in range(len(data)):
            if (rsi_aligned[i] < 30) and (current_price[i] < lower_band_aligned[i]):
                consecutive_buy += 1
                consecutive_sell = 0
            elif (rsi_aligned[i] > 70) and (current_price[i] > upper_band_aligned[i]):
                consecutive_sell += 1
                consecutive_buy = 0
            else:
                consecutive_buy = 0
                consecutive_sell = 0

            buy_signal.append(1 if consecutive_buy >= self.consecutive_days else 0)  # Use self.consecutive_days
            sell_signal.append(-1 if consecutive_sell >= self.consecutive_days else 0)  # Use self.consecutive_days

        signals = pd.DataFrame(data.index, columns=['Date'])
        signals[self.ticker + '_Buy'] = buy_signal
        signals[self.ticker + '_Sell'] = sell_signal

        return signals

    def algo1_loop(self)->list:
        """
        Executes the algorithm for multiple tickers and generates
        buying/selling signals for each ticker.

        Returns:
        -------
        list of pandas.DataFrame:
        A list of pandas DataFrames, each containing the buying/selling signals for a ticker.
        Each DataFrame has 3 columns: 'Date', 'Buy', and 'Sell', where 'Buy' and 'Sell'
        are binary indicators of whether a buy or a sell signal was generated on that
        date for the corresponding ticker.
        """

        signals_list = []

        for ticker1 in self.tickers_list:
            try:
                instance_1 = Algo1(ticker=ticker1,
                                   start_date=self.start_date,
                                   end_date=self.end_date)
                signals_1 = instance_1.generate_signals()
            except KeyError as error:
                print(f"KeyError for {ticker1}: {str(error)}")
                continue
            except ValueError as error:
                print(f"ValueError for {ticker1}: {str(error)}")
                continue

            condition1 = signals_1[ticker1 + '_Buy'] == 1
            condition2 = signals_1[ticker1 + '_Sell'] == 1

            combined_condition = condition1 | condition2

            extracted_rows = signals_1[combined_condition]

            new_df = pd.DataFrame()
            new_df["Ticker"] = [ticker1] * len(extracted_rows)
            new_df["Buy"] = [1 if b else "" for b in extracted_rows[ticker1 + '_Buy']]
            new_df["Sell"] = [-1 if s else "" for s in extracted_rows[ticker1 + '_Sell']]
            new_df.index = extracted_rows['Date']

            if not new_df.empty:
                signals_list.append(new_df)
        return signals_list
