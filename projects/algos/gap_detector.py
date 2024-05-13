"""
Main script for the gap detector algo.
"""
import sys
import pandas as pd
import numpy as np
import talib
sys.path.append("..")
from data.finanec_database import Database

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

    def detect_gaps_with_macd(data, atr_window=14, gap_threshold=1.5):
        # Calculate ATR
        data['ATR'] = talib.ATR(data['High'].values, data['Low'].values, data['Close'].values, timeperiod=atr_window)

        # Calculate MACD
        macd, signal, _ = talib.MACD(data['Close'].values)

        # Determine the trend based on MACD
        trend_up = macd > signal
        trend_down = macd < signal

        # Calculate expected gap size based on ATR
        expected_gap = data['ATR'] * gap_threshold

        # Identify where gaps occur
        gap_up = (data['Close'] - data['Open']) > expected_gap
        gap_down = (data['Open'] - data['Close']) > expected_gap

        # Combine gap detection with trend direction
        gap_up &= trend_up
        gap_down &= trend_down

        return gap_up, gap_down

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

    # Apply the combined strategy
    gap_up, gap_down = detect_gaps_with_macd(data)

    # Print detected gaps
    print("Gap Up:", gap_up)
    print("Gap Down:", gap_down)

