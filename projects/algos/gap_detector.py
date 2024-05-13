"""
Main script for the gap detector algo.
"""
import sys
import pandas as pd
import numpy as np
import pandas_ta as ta
from pathlib import Path
sys.path.append("..")
from data.finance_database import Database

class GapDetector:
    """
    Algo for gap dectector
    """
    def __init__(self,ticker=None,start_date=None,
                 end_date=None,tickers_list=None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
        self.db_instance = Database()

    def detect_gaps_with_macd(self,atr_window=14, gap_threshold=1):

        db_path = Path.home() / "Desktop" / "Database" / "SandP.db"

        data = self.db_instance.retrieve_data_from_database(start_date=self.start_date,
                                                    end_date=self.end_date,
                                                    ticker=self.ticker,
                                                    database_path=db_path)
        data.set_index('Date', inplace=True)

        data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'], length=atr_window)

        # Calculate MACD
        macd_results = ta.macd(data['Close'])
        data['MACD'] = macd_results['MACD_12_26_9']
        data['MACD_Signal'] = macd_results['MACDh_12_26_9']
        trend_up = data['MACD'] > data['MACD_Signal']
        trend_down = data['MACD'] < data['MACD_Signal']

        # Calculate expected gap size based on ATR
        expected_gap = data['ATR'] * gap_threshold

        # Identify where gaps occur
        gap_up = (data['Close'] - data['Open']) > expected_gap
        gap_down = (data['Open'] - data['Close']) > expected_gap

        # Combine gap detection with trend direction
        gap_up &= trend_up
        gap_down &= trend_down

        return gap_up, gap_down

    def backtest_gap_strategy(self,gap_up, gap_down):

        db_path = Path.home() / "Desktop" / "Database" / "SandP.db"

        data = self.db_instance.retrieve_data_from_database(start_date=self.start_date,
                                                    end_date=self.end_date,
                                                    ticker=self.ticker,
                                                    database_path=db_path)
        data.set_index('Date', inplace=True)

        # Initialize position
        position = 0  # 0: no position, 1: long, -1: short

        # Initialize returns
        returns = []

        for i in range(len(data)):
            if gap_up[i]:
                # Enter long position
                position = 1
                entry_price = data['Open'].iloc[i + 1]  # Open price of the day after the gap up
            elif gap_down[i]:
                # Exit long position
                if position == 1:
                    exit_price = data['Open'].iloc[i + 1]  # Open price of the day after the gap down
                    returns.append((exit_price - entry_price) / entry_price)
                    position = 0

        if position == 1:
            # If still in position at the end of the data, exit position at the last day's close
            exit_price = data['Close'].iloc[-1]
            returns.append((exit_price - entry_price) / entry_price)

        cumulative_returns = (1 + np.array(returns)).cumprod()

        return cumulative_returns

    # Example usage
if __name__ == "__main__":
    # Load sample data (replace this with your own data)
    # Assuming a DataFrame with 'Date', 'Open', 'High', 'Low', 'Close' columns
    # Here's some example data:
    data = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=100),
        'Open': np.random.randn(100),
        'High': np.random.randn(100),
        'Low': np.random.randn(100),
        'Close': np.random.randn(100)
    })


    instance = GapDetector(start_date="2022-01-01",
                           end_date="2024-01-01",
                           ticker='TWI')

    # Apply the combined strategy
    gap_up, gap_down = instance.detect_gaps_with_macd()

    cumulative_returns = instance.backtest_gap_strategy(gap_up, gap_down)

    # Print cumulative returns
    print("Cumulative Returns:", cumulative_returns)

    # Print detected gaps
    print("Gap Up:", gap_up)
    print("Gap Down:", gap_down)

