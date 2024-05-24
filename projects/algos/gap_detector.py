import sys
import pandas as pd
import numpy as np
import pandas_ta as ta
from pathlib import Path
sys.path.append("..")
from data.finance_database import Database
from algo_scrapers.s_and_p_scraper import SAndPScraper
import pandas_ta as ta
from algo_scrapers.danish_ticker_scraper import OMXC25scraper
from algo_scrapers.omxs30_scraper import OMXS30scraper

class GapDetector:
    """
    Algo for gap detector
    """

    def __init__(self, ticker=None, start_date=None, end_date=None, tickers_list=None, data=None,
                 market = None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
        self.db_instance = Database()
        self.data = data
        self.market = market

    def fetch_data_from_yahoo(self):
        """
        Method to fetch data from the yahoo finance website.
        This website is currently used for other markets than the American, where
        we don't have a database.

        Returns:
        Data from the yahoo finance api.

        """
        if self.ticker:
            data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
            data.index.name = 'Date'
            return data

    def detect_gaps_with_macd(self, atr_window=14, gap_threshold=1.5):
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

    def backtest_gap_strategy(self, gap_up, gap_down, specific_date):
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
                    exit_price = data['Open'].iloc[i + 1]  # Open price of the day after the gap down
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

    def get_signals_for_date(self, date, atr_window=14, gap_threshold=1.5):
        data, gap_up, gap_down = self.detect_gaps_with_macd(atr_window, gap_threshold)

        if date not in data.index:
            raise ValueError(f"Date {date} not found in the data.")

        signal_gap_up = gap_up.loc[date]
        signal_gap_down = gap_down.loc[date]

        return signal_gap_up, signal_gap_down


# Example usage
if __name__ == "__main__":
    tickers_list0 = SAndPScraper()
    tickers_list = tickers_list0.run_scraper()
    start_date = "2024-01-01"
    end_date = "2024-05-21"
    specific_date = "2024-05-17 00:00:00"

    signals_list = []
    specific_date_signals_list = []
    backtested_list = []
    trade_returns_list = []
    all_data = {}

    db_instance = Database()
    db_path = Path.home() / "Desktop" / "Database" / "SandP.db"

    # Fetch data for all tickers once
    for ticker in tickers_list:
        try:
            data = db_instance.retrieve_data_from_database(start_date=start_date,
                                                           end_date=end_date,
                                                           ticker=ticker,
                                                           database_path=db_path)
            data.set_index('Date', inplace=True)
            all_data[ticker] = data
        except Exception as e:
            print(f"Error fetching data for ticker {ticker}: {e}")
            continue

    for ticker in tickers_list:
        if ticker not in all_data:
            continue

        instance = GapDetector(start_date=start_date, end_date=end_date, ticker=ticker, data=all_data[ticker])

        try:
            # Apply the combined strategy
            data, gap_up, gap_down = instance.detect_gaps_with_macd(gap_threshold=1.5)

            # Check if there are any signals before appending
            if gap_up.any() or gap_down.any():
                # Create a DataFrame for signals
                signals_df = pd.DataFrame({
                    'Date': data.index,
                    'Gap_Up': gap_up,
                    'Gap_Down': gap_down
                })
                signals_df['Ticker'] = ticker

                # Append the DataFrame to the list
                signals_list.append(signals_df)

            # Get signals for a specific date
            try:
                signal_gap_up, signal_gap_down = instance.get_signals_for_date(specific_date)
                if signal_gap_up or signal_gap_down:  # Check if either Gap_Up or Gap_Down is True
                    specific_date_df = pd.DataFrame({
                        'Date': [specific_date],
                        'Gap_Up': [signal_gap_up],
                        'Gap_Down': [signal_gap_down],
                        'Ticker': [ticker]
                    })
                    specific_date_signals_list.append(specific_date_df)

                    # Backtest the strategy for this ticker up to the specific date
                    backtested_returns, trades_df = instance.backtest_gap_strategy(gap_up, gap_down, specific_date)
                    backtested_df = pd.DataFrame({
                        'Date': data.index[:len(backtested_returns)],
                        'Cumulative_Returns': backtested_returns
                    })
                    backtested_df['Ticker'] = ticker
                    backtested_list.append(backtested_df)
                    trade_returns_list.append(trades_df)

            except ValueError as e:
                print(e)
                continue

        except Exception as e:
            print(f"Error processing ticker {ticker}: {e}")
            continue

    # # Print signals list
    # for signals_df in signals_list:
    #     print(signals_df)
    #
    # # Print specific date signals list
    # for specific_signals_df in specific_date_signals_list:
    #     print(specific_signals_df)
    #
    # # Print backtested results list
    # for backtested_df in backtested_list:
    #     print(backtested_df)
    #
    # # Print trade returns list
    # for trades_df in trade_returns_list:
    #     print(trades_df)

    print("k")




