"""
Module for detecting gaps in stock market data using various technical indicators.

This module defines a `GapDetector` class that provides methods to fetch stock data,
detect gaps using MACD, ATR, RSI, and Bollinger Bands, backtest the gap strategy,
and get signals for a specific date. The class integrates with a local database and
Yahoo Finance API for data retrieval.

Classes:
    GapDetector: Implements methods for gap detection and backtesting.

Imports:
    sys, pandas as pd, numpy as np, Path from pathlib,
    Database from finance_database, pandas_ta as ta
"""
# pylint: disable=wrong-import-position.
import sys
import pandas as pd
import numpy as np
from pathlib import Path
sys.path.append("..")
from data.finance_database import Database
import pandas_ta as ta

class GapDetector:
    """
    Class for detecting gaps in stock market data using various technical indicators.

    Attributes:
        ticker (str): The stock ticker symbol.
        start_date (str): The start date for data retrieval.
        end_date (str): The end date for data retrieval.
        tickers_list (list): A list of ticker symbols.
        data (pd.DataFrame): DataFrame containing stock market data.
        market (str): The market identifier.
    """

    def __init__(self, ticker: str = None, start_date: str = None, end_date: str = None,
                 tickers_list: list = None, data: pd.DataFrame = None, market: str = None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
        self.db_instance = Database()
        self.data = data
        self.market = market

    def detect_gaps_with_macd(self, atr_window: int = 14, gap_threshold: float = 1.5) -> tuple:
        """
        Detect trading signals/gaps using MACD, ATR, RSI, and Bollinger Bands.

        Args:
            atr_window (int): The window length for ATR calculation. Default is 14.
            gap_threshold (float): The threshold multiplier for detecting gaps. Default is 1.5.

        Returns:
            tuple: A tuple containing the data DataFrame, gap up signals, and gap down signals.
        """
        data = self.data
        if data is None:
            db_path = Path.home() / "Desktop" / "Database" / "SandP.db"
            data = self.db_instance.retrieve_data_from_database(start_date=self.start_date,
                                                                end_date=self.end_date,
                                                                ticker=self.ticker,
                                                                database_path=db_path)
            data.set_index('Date', inplace=True)

        # Remove duplicate dates
        data = data[~data.index.duplicated(keep='first')]

        # ATR Calculation
        data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'], length=atr_window)

        # MACD Calculation
        macd_results = ta.macd(data['Close'])
        data['MACD'] = macd_results['MACD_12_26_9']
        data['MACD_Signal'] = macd_results['MACDs_12_26_9']

        # Additional Indicator: RSI
        data['RSI'] = ta.rsi(data['Close'], length=14)

        # Additional Indicator: Bollinger Bands
        bollinger = ta.bbands(data['Close'], length=20, std=2)
        data['BB_upper'] = bollinger['BBU_20_2.0']
        data['BB_lower'] = bollinger['BBL_20_2.0']

        trend_up = (data['MACD'] > data['MACD_Signal']) & (data['RSI'] < 70)
        trend_down = (data['MACD'] < data['MACD_Signal']) & (data['RSI'] > 30)

        # Calculate expected gap size based on ATR
        expected_gap = data['ATR'] * gap_threshold

        # Identify where gaps occur
        gap_up = (data['Close'] - data['Open']) > expected_gap
        gap_down = (data['Open'] - data['Close']) > expected_gap

        # Combine gap detection with trend direction and volume filter
        gap_up &= trend_up & (data['Volume'] > data['Volume'].rolling(window=20).mean())
        gap_down &= trend_down & (data['Volume'] > data['Volume'].rolling(window=20).mean())

        return data, gap_up, gap_down

    def backtest_gap_strategy(self, gap_up: pd.Series,
                              gap_down: pd.Series,
                              specific_date: str) -> tuple:
        """
        Backtest the gap trading strategy up to a specific date.

        Args:
            gap_up (pd.Series): Series indicating gap up signals.
            gap_down (pd.Series): Series indicating gap down signals.
            specific_date (str): The specific date to filter data up to.

        Returns:
            tuple: A tuple containing cumulative returns and a DataFrame of trades.
        """
        data = self.data
        if data is None:
            db_path = Path.home() / "Desktop" / "Database" / "SandP.db"
            data = self.db_instance.retrieve_data_from_database(start_date=self.start_date,
                                                                end_date=self.end_date,
                                                                ticker=self.ticker,
                                                                database_path=db_path)
            data.set_index('Date', inplace=True)

        # Remove duplicate dates
        data = data[~data.index.duplicated(keep='first')]

        # Filter data up to the specific date
        data = data[:specific_date]
        gap_up = gap_up[:specific_date]
        gap_down = gap_down[:specific_date]

        # Initialize position
        position = 0  # 0: no position, 1: long, -1: short

        # Initialize returns and trades
        returns = []
        trades = []

        for i in range(len(data) - 1):
            if gap_up.iloc[i]:
                # Enter long position
                position = 1
                entry_price = data['Open'].iloc[i + 1]  # Open price of the day after the gap up
                entry_date = data.index[i + 1]
            elif gap_down.iloc[i]:
                # Exit long position
                if position == 1:
                    exit_price = data['Open'].iloc[
                        i + 1]  # Open price of the day after the gap down
                    exit_date = data.index[i + 1]
                    trade_return = (exit_price - entry_price) / entry_price
                    returns.append(trade_return)
                    trades.append({
                        'Entry_Date': entry_date,
                        'Entry_Price': entry_price,
                        'Exit_Date': exit_date,
                        'Exit_Price': exit_price,
                        'Return': trade_return
                    })
                    position = 0

        if position == 1:
            # If still in position at the end of the data, exit position at the last day's close
            exit_price = data['Close'].iloc[-1]
            exit_date = data.index[-1]
            trade_return = (exit_price - entry_price) / entry_price
            returns.append(trade_return)
            trades.append({
                'Entry_Date': entry_date,
                'Entry_Price': entry_price,
                'Exit_Date': exit_date,
                'Exit_Price': exit_price,
                'Return': trade_return
            })

        cumulative_returns = (1 + np.array(returns)).cumprod()

        trades_df = pd.DataFrame(trades)
        return cumulative_returns, trades_df

    def get_signals_for_date(self, date: str,
                             atr_window: int = 14,
                             gap_threshold: float = 1.5) -> tuple:
        """
        Get gap trading signals for a specific date.

        Args:
            date (str): The date to get signals for.
            atr_window (int): The window length for ATR calculation. Default is 14.
            gap_threshold (float): The threshold multiplier for detecting gaps. Default is 1.5.

        Returns:
            tuple: A tuple containing gap up signal and gap down signal for the given date.
        """
        data, gap_up, gap_down = self.detect_gaps_with_macd(atr_window, gap_threshold)

        if date not in data.index:
            raise ValueError(f"Date {date} not found in the data.")

        signal_gap_up = gap_up.loc[date]
        signal_gap_down = gap_down.loc[date]

        return signal_gap_up, signal_gap_down
