import sys
sys.path.insert(0,'..')
from algo_scrapers.danish_ticker_scraper import OMXC25scraper
from algo_scrapers.omxs30_scraper import OMXS30scraper
from algo_scrapers.s_and_p_scraper import SAndPScraper
from algo_scrapers.obx_scraper import OBXscraper
import yfinance as yf
import pandas as pd
import ta  # Technical analysis library
import numpy as np
import schedule
import time
import pytz
import streamlit as st
from datetime import datetime


def get_stock_data(ticker: str, interval: str = '15m', period: str = '1d') -> pd.DataFrame:
    """
    Fetches stock data for a given ticker using yfinance.
    """
    data = yf.download(ticker, interval=interval, period=period)

    # Ensure data is not empty
    if data.empty:
        return None

    return data


def calculate_rsi(data: pd.DataFrame, window: int = 14) -> pd.Series:
    """
    Calculates the Relative Strength Index (RSI) for the given data.
    """
    if 'Close' not in data.columns or data['Close'].empty:
        return pd.Series([np.nan] * len(data))  # Return NaNs if data is missing

    return ta.momentum.RSIIndicator(data['Close'], window=window).rsi()


def calculate_bollinger_bands(data: pd.DataFrame, window: int = 20, std_dev: float = 2) -> pd.DataFrame:
    """
    Calculates the Bollinger Bands for the given data.
    """
    if 'Close' not in data.columns or data['Close'].empty:
        return pd.DataFrame(index=data.index, columns=['BB_Middle', 'BB_Upper', 'BB_Lower'])

    bb_indicator = ta.volatility.BollingerBands(close=data['Close'], window=window, window_dev=std_dev)
    data['BB_Middle'] = bb_indicator.bollinger_mavg()
    data['BB_Upper'] = bb_indicator.bollinger_hband()
    data['BB_Lower'] = bb_indicator.bollinger_lband()
    return data[['BB_Middle', 'BB_Upper', 'BB_Lower']]


def generate_buy_signals(data: pd.DataFrame) -> pd.DataFrame:
    """
    Generates buy signals based on RSI < 20 and the close price being below the lower Bollinger Band.
    """
    data['Buy_Signal'] = np.where((data['RSI'] < 20) & (data['Close'] < data['BB_Lower']), 1, 0)
    return data


def main(ticker: str):
    """
    Main function to calculate RSI, Bollinger Bands, and Buy signals for a given ticker.
    """
    try:
        stock_data = get_stock_data(ticker)

        if stock_data is None:
            return None  # Skip if no data is retrieved

        stock_data['RSI'] = calculate_rsi(stock_data)
        bollinger_bands = calculate_bollinger_bands(stock_data)
        stock_data = stock_data.join(bollinger_bands, rsuffix='_BB')
        stock_data = generate_buy_signals(stock_data)

        # Filter Buy Signals
        buy_signals = stock_data[stock_data['Buy_Signal'] == 1]

        if not buy_signals.empty:
            buy_signals['Ticker'] = ticker  # Add ticker symbol to buy signals DataFrame

        return buy_signals  # Return the DataFrame with buy signals

    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        return None

def run_strategy():
    """
    Runs the strategy for a list of tickers and collects the buy signals.
    """
    tickers_list0 = SAndPScraper()  # Example of using a scraper
    tickers = tickers_list0.run_scraper()

    all_signals = pd.DataFrame()

    for ticker in tickers:
        signals = main(ticker)
        if signals is not None and not signals.empty:
            all_signals = pd.concat([all_signals, signals])

    return all_signals


# Streamlit app setup
st.title("Real-Time Buy Signal Dashboard")

# Initialize session state if not done already
if 'run_strategy' not in st.session_state:
    st.session_state.run_strategy = True

# Continuously run the strategy every minute
while st.session_state.run_strategy:
    buy_signals = run_strategy()

    if not buy_signals.empty:
        # Show buy signals as a table in Streamlit
        st.write(f"Buy Signals Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.dataframe(buy_signals)
    else:
        st.write("No Buy Signals generated.")

    time.sleep(60)  # Wait for 60 seconds before refreshing

#
# def get_stock_data(ticker: str, interval: str = '5m', period: str = '1d') -> pd.DataFrame:
#     """
#     Fetches stock data for a given ticker using yfinance.
#
#     Parameters:
#     -----------
#     ticker : str
#         Stock ticker symbol.
#     interval : str
#         Interval between data points (e.g., '15m', '1d', etc.)
#     period : str
#         Data period (e.g., '1d', '5d').
#
#     Returns:
#     --------
#     pd.DataFrame
#         DataFrame containing the stock data.
#     """
#     data = yf.download(ticker, interval=interval, period=period)
#
#     # Ensure data is not empty
#     if data.empty:
#         print(f"No data retrieved for ticker {ticker}")
#         return None
#
#     return data
#
#
# def calculate_rsi(data: pd.DataFrame, window: int = 14) -> pd.Series:
#     """
#     Calculates the Relative Strength Index (RSI) for the given data.
#
#     Parameters:
#     -----------
#     data : pd.DataFrame
#         DataFrame containing stock data with a 'Close' column.
#     window : int
#         Lookback period for calculating RSI.
#
#     Returns:
#     --------
#     pd.Series
#         Series containing the RSI values.
#     """
#     if 'Close' not in data.columns or data['Close'].empty:
#         print("No 'Close' column or data is empty for RSI calculation.")
#         return pd.Series([np.nan] * len(data))  # Return NaNs if data is missing
#
#     return ta.momentum.RSIIndicator(data['Close'], window=window).rsi()
#
#
# def calculate_bollinger_bands(data: pd.DataFrame, window: int = 20, std_dev: float = 2) -> pd.DataFrame:
#     """
#     Calculates the Bollinger Bands for the given data.
#
#     Parameters:
#     -----------
#     data : pd.DataFrame
#         DataFrame containing stock data with a 'Close' column.
#     window : int
#         Lookback period for calculating Bollinger Bands.
#     std_dev : float
#         Number of standard deviations for the upper and lower bands.
#
#     Returns:
#     --------
#     pd.DataFrame
#         DataFrame containing the 'Middle', 'Upper', and 'Lower' Bollinger Bands.
#     """
#     if 'Close' not in data.columns or data['Close'].empty:
#         print("No 'Close' column or data is empty for Bollinger Bands calculation.")
#         return pd.DataFrame(index=data.index, columns=['BB_Middle', 'BB_Upper', 'BB_Lower'])
#
#     bb_indicator = ta.volatility.BollingerBands(close=data['Close'], window=window, window_dev=std_dev)
#     data['BB_Middle'] = bb_indicator.bollinger_mavg()
#     data['BB_Upper'] = bb_indicator.bollinger_hband()
#     data['BB_Lower'] = bb_indicator.bollinger_lband()
#     return data[['BB_Middle', 'BB_Upper', 'BB_Lower']]
#
#
# def generate_buy_signals(data: pd.DataFrame) -> pd.DataFrame:
#     """
#     Generates buy signals based on RSI < 20 and the close price being below the lower Bollinger Band.
#
#     Parameters:
#     -----------
#     data : pd.DataFrame
#         DataFrame containing stock data with RSI and Bollinger Bands.
#
#     Returns:
#     --------
#     pd.DataFrame
#         DataFrame containing buy signals (1 for buy, 0 otherwise).
#     """
#     data['Buy_Signal'] = np.where((data['RSI'] < 20) & (data['Close'] < data['BB_Lower']), 1, 0)
#     return data
#
#
# def main(ticker: str):
#     try:
#         # Fetch stock data (15-minute intervals, 1 day of data)
#         stock_data = get_stock_data(ticker)
#
#         if stock_data is None:
#             return  # Skip if no data is retrieved
#
#         # Calculate RSI (14-period window)
#         stock_data['RSI'] = calculate_rsi(stock_data)
#
#         # Calculate Bollinger Bands (20-period window, 2 standard deviations)
#         bollinger_bands = calculate_bollinger_bands(stock_data)
#
#         # Join Bollinger Bands data, specifying suffix to avoid column overlap
#         stock_data = stock_data.join(bollinger_bands, rsuffix='_BB')
#
#         # Generate Buy Signals
#         stock_data = generate_buy_signals(stock_data)
#
#         # Filter Buy Signals
#         buy_signals = stock_data[stock_data['Buy_Signal'] == 1]
#
#         if not buy_signals.empty:
#             # Print the ticker name and the price at which the signal occurred
#             for index, row in buy_signals.iterrows():
#                 print(f"Buy Signal for {ticker} at {index}: Price = {row['Close']:.2f}, RSI = {row['RSI']:.2f}")
#
#     except Exception as e:
#         print(f"Error processing {ticker}: {e}")
#
#
# def run_strategy():
#     # Define the tickers to track
#     tickers_list0 = OMXS30scraper()
#     tickers = tickers_list0.run_scraper()
#
#     for ticker in tickers:
#         main(ticker)
#
#
# # Schedule the strategy to run every 15 minutes
# schedule.every(1).minutes.do(run_strategy)
#
# # Keep the script running
# if __name__ == "__main__":
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


