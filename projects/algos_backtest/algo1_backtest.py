"""
Main script for algo1 backtest.
"""
# pylint: disable=wrong-import-position.
# import sys
# import pandas as pd
# import numpy as np
# sys.path.append('..')
# from algos.algo1 import Algo1
# # pylint: disable=duplicate-code.
# from data.finance_database import Database
# from data.danish_tickers import TickerCodeProvider
#
# class Algo1Backtest:
#     """
#     A class to backtest Algo1. The class uses the output from Algo1.
#     The class contains various backtesting measures to backtest
#     the algo.
#     """
#     # pylint: disable=too-many-arguments.
#     def __init__(self,start_date=None,end_date=None,
#                  tickers_list=None,consecutive_days=None,
#                  consecutive_days_sell=None):
#         """
#         Initialize the Algo1Backtest object.
#
#         Args:
#             start_date (str):
#                 The start date of the backtest period. Defaults to None.
#             end_date (str):
#                 The end date of the backtest period. Defaults to None.
#             tickers_list (List[str]):
#                 A list of ticker symbols to be used for backtesting.
#             Defaults to None.
#             consecutive_days (int or None):
#                 The number of consecutive days the conditions should be met to
#                 generate signals. If None, the default is None.
#             consecutive_days_sell (int or None):
#                 The number of consecutive days the sell conditions should be met
#                 to generate signals. If None, the default is None.
#         """
#         self.start_date = start_date
#         self.end_date = end_date
#         self.tickers_list = tickers_list
#         self.consecutive_days = consecutive_days
#         self.consecutive_days_sell = consecutive_days_sell
#
#     def run_algo1(self):
#         """
#         Executes Algo1 algorithm and returns the output.
#
#         This method initializes an instance of the Algo1 class with the provided
#         start and end dates, and a list of tickers.
#         It then runs the algo1_loop method to perform the
#          algorithm logic and obtain the output.
#
#         Returns:
#             algo1_output (Any): The output of the Algo1 algorithm.
#
#         """
#         output_list = []
#         for ticker1 in self.tickers_list:
#             try:
#                 instance_1 = Algo1(ticker=ticker1,
#                                    start_date=self.start_date,
#                                    end_date=self.end_date,
#                                    consecutive_days=self.consecutive_days,
#                                    consecutive_days_sell=self.consecutive_days_sell)
#                 signals_1 = instance_1.generate_signals()
#             except KeyError as error:
#                 print(f"KeyError for {ticker1}: {str(error)}")
#                 continue
#             except ValueError as error:
#                 print(f"ValueError for {ticker1}: {str(error)}")
#                 continue
#
#             condition1 = signals_1[ticker1 + '_Buy'] == 1
#             condition2 = signals_1[ticker1 + '_Sell'] == -1
#
#             combined_condition = condition1 | condition2
#
#             extracted_rows = signals_1[combined_condition]
#
#             new_df = pd.DataFrame()
#             new_df["Ticker"] = [ticker1] * len(extracted_rows)
#             new_df["Buy"] = [1 if b else "" for b in extracted_rows[ticker1 + '_Buy']]
#             new_df["Sell"] = [-1 if s else "" for s in extracted_rows[ticker1 + '_Sell']]
#             new_df.index = extracted_rows['Date']
#
#             if not new_df.empty:
#                 output_list.append(new_df)
#
#         algo1_output = output_list
#
#         return algo1_output
#
#     def backtest_prices(self):
#         # pylint: disable=too-many-locals.
#         """
#         This method computes and retrieves the prices
#         given the buy/sell signals from Algo1.
#
#         Returns:
#             List[List[pd.DataFrame]]: A list containing two sub-lists:
#                 - buy_prices_list:
#                  List of pandas DataFrames containing buy prices for each ticker.
#                 - sell_prices_list:
#                  List of pandas DataFrames containing sell prices for each ticker.
#         """
#
#         price_data = {}
#
#         for ticker in self.tickers_list:
#             data = Database.get_price_data(self, start=self.start_date,
#                                            end=self.end_date,
#                                            ticker=ticker)
#             price_data[ticker] = data["Open"]
#
#         algo1_data = Algo1Backtest.run_algo1(self)
#
#         df_buy_signals = pd.DataFrame(columns=['Ticker', 'Buy Signal'])
#         df_sell_signals = pd.DataFrame(columns=['Ticker', 'Sell Signal'])
#
#         for df_algo1 in algo1_data:
#             ticker = df_algo1.at[df_algo1.index[0], 'Ticker']
#             df_buy = df_algo1.loc[df_algo1['Buy'] == 1]
#             df_sell = df_algo1.loc[df_algo1['Sell'] == -1]
#
#             buy_df_to_concat = pd.DataFrame({'Ticker': [ticker] * len(df_buy),
#                                              'Buy Signal': df_buy.index})
#
#             if not df_buy.empty:
#
#                 df_buy_signals = pd.concat([df_buy_signals, buy_df_to_concat],
#                                            ignore_index=True, sort=False)
#
#             sell_df_to_concat = pd.DataFrame({'Ticker': [ticker] * len(df_sell),
#                                               'Sell Signal': df_sell.index})
#             if not sell_df_to_concat.empty:
#                 df_sell_signals = pd.concat([df_sell_signals, sell_df_to_concat],
#                                             ignore_index=True, sort=False)
#
#         # We will now make the buy/sell prices:
#         buy_prices_list = []
#         sell_prices_list = []
#
#         filtered_df_sell = pd.DataFrame(columns=['Ticker', 'Sell Signal', 'Sell date', 'Sell price'])
#
#         for ticker1 in self.tickers_list:
#             filtered_df = df_buy_signals[df_buy_signals['Ticker'] == ticker1].copy()
#             filtered_df['Buy date'] = pd.to_datetime(
#                 filtered_df['Buy Signal']).dt.date + pd.DateOffset(days=1)
#
#             for j in range(len(filtered_df)):
#                 mask = filtered_df['Buy date'].iloc[j]
#                 value = None
#                 while value is None:
#                     if mask.weekday() < 5:
#                         if mask in price_data[ticker1]:
#                             value = price_data[ticker1][mask]
#                             break
#                     mask += pd.DateOffset(days=1)
#                 # filtered_df['Buy date'].iloc[j] = mask
#                 filtered_df.loc[filtered_df.index[j], 'Buy date'] = mask
#                 filtered_df.loc[filtered_df['Buy date'] == mask, 'Buy price'] = value
#                 filtered_df_sell.loc[filtered_df_sell['Sell date'] == mask, 'Sell price'] = value
#
#             # Append to the list:
#             buy_prices_list.append(filtered_df)
#
#             filtered_df_sell = df_sell_signals[
#                 df_sell_signals['Ticker'] == ticker1].copy()
#             filtered_df_sell['Sell date'] = pd.to_datetime(
#                 filtered_df_sell['Sell Signal']).dt.date + pd.DateOffset(
#                 days=1)
#
#             for j in range(len(filtered_df_sell)):
#                 mask = filtered_df_sell['Sell date'].iloc[j]
#                 value = None
#                 while value is None:
#                     if mask.weekday() < 5:
#                         if mask in price_data[ticker1]:
#                             value = price_data[ticker1][mask]
#                             break
#                     mask += pd.DateOffset(days=1)
#                 # filtered_df_sell['Sell date'].iloc[j] = mask
#                 filtered_df_sell.loc[filtered_df_sell.index[j], 'Sell date'] = mask
#                 filtered_df_sell.loc[filtered_df_sell['Sell date'] == mask, 'Sell price'] = value
#
#             # Append to list:
#             sell_prices_list.append(filtered_df_sell)
#
#         return [buy_prices_list, sell_prices_list]
#
#     # pylint: disable=too-many-locals.
#     def backtest_returns(self):
#         # pylint: disable=too-many-branches.
#         """
#         Computes and retrieves the returns for each ticker based
#         on the buy/sell signals obtained from Algo1.
#
#         Returns:
#             List[pd.DataFrame]: A list of pandas DataFrames containing
#                 the returns data for each ticker. Each DataFrame
#                 contains the following columns:
#                                     - Ticker: Ticker symbol
#                                     - Buy Date: Date of buy signal, i.e. one day after the signal.
#                                     - Sell Date: Date of sell signal
#                                     - Returns: Computed returns for the trade
#                                     - Log returns: Log returns. The formula log(1 + x) is used
#                                       to deal with negative return values.
#         """
#
#         prices = Algo1Backtest.backtest_prices(self)
#
#         # returns_list = []  # List to store the returns dataframes for each ticker
#         returns_dict = {}
#
#         # pylint: disable=too-many-nested-blocks
#         for ticker1 in self.tickers_list:
#             returns_df = pd.DataFrame(columns=['Ticker',
#                                                'Buy Date',
#                                                'Sell Date',
#                                                'Returns',
#                                                'Position',
#                                                'Log returns'])
#             position = 0  # Initialize position as 0 (no position)
#             latest_sell_date = None  # Initialize latest sell date as None
#
#             for df_buy in prices[0]:
#                 for df_sell in prices[1]:
#                     if not df_buy.empty\
#                             and not df_sell.empty\
#                             and df_buy['Ticker'].iloc[0] == ticker1 and \
#                             df_sell['Ticker'].iloc[0] == ticker1:
#                         df_buy = pd.DataFrame(df_buy)
#                         df_sell = pd.DataFrame(df_sell)
#
#                         new_data = {'Ticker': [ticker1],
#                                     'Buy_Date': [timestamp1],
#                                     'Sell_Date': [sell_date],
#                                     'Returns': [returns],
#                                     'Position': [position],
#                                     'Log_returns': [log_returns]}
#
#                         if returns_df.empty:
#                             returns_df = pd.DataFrame(new_data)
#                         else:
#                             returns_df = returns_df.append(new_data, ignore_index=True)
#
#                         # pylint: disable=unused-variable.
#                         for j, row in df_buy.iterrows():
#                             if pd.notnull(row['Buy price']):
#                                 timestamp1 = row['Buy date']
#                                 buy_price = row['Buy price']
#
#                                 # Filter out sell dates before the latest sell date with position=1
#                                 if latest_sell_date is not None and timestamp1 < latest_sell_date:
#                                     continue  # Skip the iteration if there are no valid sell dates
#
#                                 # Filter sell dataframe based on the buy date
#                                 df_sell_filtered = df_sell[df_sell['Sell date'] > timestamp1]
#
#                                 # Check if there is a sell_price available
#                                 if not df_sell_filtered.empty:
#                                     sell_price = df_sell_filtered.iloc[0]['Sell price']
#                                     sell_date = df_sell_filtered.iloc[0]['Sell date']
#                                     latest_sell_date = sell_date  # Update the latest sell date
#
#                                     # Update position based on Buy date and Sell date
#                                     if position == 0:  # No position is active
#                                         if timestamp1 < sell_date:
#                                             position = 1
#                                     elif position == 1:  # Position is active
#                                         if timestamp1 < sell_date:
#                                             position = 0
#                                 else:
#                                     sell_price = None
#                                     sell_date = None
#
#                                 # Check if there is a remaining sell_price
#                                 if sell_price is not None:
#                                     returns = (sell_price - buy_price) / sell_price
#                                     log_returns = np.log1p(returns)
#                                     returns_df = pd.concat([returns_df, pd.DataFrame(
#                                         {'Ticker': [ticker1],
#                                          'Buy_Date': [timestamp1],
#                                          'Sell_Date': [sell_date],
#                                          'Returns': [returns],
#                                          'Position': [position],
#                                          'Log_returns': [log_returns]
#                                          })])
#             returns_df = returns_df.drop(columns=['Position'])
#             # returns_list.append(returns_df)
#             returns_dict[ticker1] = returns_df
#
#         return returns_dict
#
#     def backtest_cumulative_returns(self):
#         """
#         Computes and retrieves the cumulative returns for each ticker based on
#         the buy/sell signals obtained from Algo1.
#
#         Returns:
#             List[pd.DataFrame]: A list of pandas DataFrames containing
#                 the cumulative returns data for each ticker. Each DataFrame
#                 contains the following columns:
#                     - Ticker: Ticker symbol
#                     - Cumulative Returns: Cumulative returns based on the previous trades
#         """
#         returns_list = self.backtest_returns()
#         cumulative_returns_list = []
#
#         for returns_df in returns_list:
#             cumulative_returns = (1 + returns_df['Returns']).cumprod() - 1
#             cumulative_returns_df = pd.DataFrame({
#                 'Ticker': returns_df['Ticker'],
#                 'Cumulative Returns': cumulative_returns
#             })
#             cumulative_returns_list.append(cumulative_returns_df)
#
#         return cumulative_returns_list
#
#     def compute_volatility(self):
#         """
#         Computes and retrieves the volatility of returns for each ticker
#         based on the buy/sell signals obtained from Algo1.
#
#         Returns:
#             pandas.DataFrame: A DataFrame containing the volatility data for each ticker.
#                 The DataFrame has the following columns:
#                     - Ticker: Ticker symbol
#                     - Volatility: Volatility of returns
#         """
#
#         volatility_data = []  # Initialize a list to store DataFrames
#
#         database_instance = Database()
#
#         for ticker in self.tickers_list:
#             try:
#                 data_returns = database_instance.compute_stock_return(start=self.start_date,
#                                                                       end=self.end_date,
#                                                                       ticker=ticker)
#
#                 # Check if price data is not empty
#                 if not data_returns.empty:
#                     trading_days = data_returns.shape[0]
#                     # Calculate realized volatility as the standard deviation of daily returns
#                     realized_volatility = np.sqrt(trading_days) * data_returns.std()
#
#                     # Append DataFrame to the list
#                     volatility_data.append(pd.DataFrame({'Ticker': [ticker],
#                                                          'Volatility': [realized_volatility]}))
#             except ValueError as error:
#                 # Handle the ValueError here (print a message, log, etc.)
#                 print(f"Error for {ticker}: {str(error)}")
#                 continue  # Continue to the next iteration
#
#         if not volatility_data:
#             print("No valid tickers with non-empty price data.")
#             return pd.DataFrame(columns=['Ticker', 'Volatility'])  # Return an empty DataFrame
#
#         # Concatenate DataFrames in the list
#         volatility_df = pd.concat(volatility_data, ignore_index=True)
#
#         return volatility_df
#
#     def variable_importance(self):
#         """
#         Assess the historical importance of different variables on the return series of the algo.
#
#         Returns:
#             List[pd.DataFrame]: A list of DataFrames containing variable importance scores.
#                                 Each DataFrame includes the following columns:
#                                     - 'Signal ticker': Ticker symbol of the signal series.
#                                     - 'Correlation': Correlation coefficient with the target series.
#                                     - 'Ticker': Ticker symbol of the target series.
#         """
#         data_downloader = Database()
#
#         danish_tickers = TickerCodeProvider.get_ticker_codes()
#         danish_returns = []
#
#         for ticker in danish_tickers:
#             try:
#                 danish_return = data_downloader.compute_stock_return(start=self.start_date,
#                                                                      end=self.end_date,
#                                                                      ticker=ticker)
#                 danish_returns.append(danish_return)
#             except ValueError as error:
#                 # Handle the ValueError here (We print a message. Could also be logged.)
#                 print(f"Error for {ticker}: {str(error)}")
#                 continue  # Continue to the next iteration
#
#         correlation_list = []
#
#         for ticker in self.tickers_list:
#             target_series = data_downloader.compute_stock_return(start=self.start_date,
#                                                      end=self.end_date,
#                                                      ticker=ticker)
#
#             ticker_correlations = []  # Initialize a list to store correlations for this ticker
#
#             for df_return in danish_returns:
#                 # Find the common start date/index
#                 common_start_date = max(target_series.index.min(), df_return.index.min())
#                 common_end_date = min(target_series.index.max(), df_return.index.max())
#
#                 # Adjust y to start from the common start date and end at the common end date
#                 target_series = target_series[(target_series.index >= common_start_date)
#                                               & (target_series.index <= common_end_date)]
#
#                 # If the dataframe in Danish_tickers is shorter, drop extra rows in y
#                 if len(df_return) < len(target_series):
#                     target_series = target_series.iloc[:len(df_return)]
#                 elif len(target_series) < len(df_return):
#                     df_return = df_return.iloc[:len(target_series)]
#
#                 # Extract Series from DataFrames
#                 target_series_squeezed = target_series.squeeze()
#                 df_series = df_return.squeeze()
#
#                 # Calculate the correlation between the two Series
#                 correlation = np.corrcoef(target_series_squeezed, df_series)[0, 1]
#
#                 # Append correlation information to the list
#                 ticker_correlations.append(
#                     {'Signal ticker': ticker, 'Correlation': correlation, 'Ticker': df_series.name})
#
#             # Create a DataFrame for this ticker's correlations
#             correlation_dataframe = pd.DataFrame(ticker_correlations)
#
#             # Sort the DataFrame by correlation in descending order
#             correlation_dataframe = correlation_dataframe.sort_values(by='Correlation',
#                                                                       ascending=False)
#             correlation_list.append(correlation_dataframe)
#
#         return correlation_list
#
# if __name__ == "__main__":
#     k = Algo1Backtest(tickers_list=['TSLA','FLS.CO'],start_date="2021-01-01",
#                       end_date="2024-01-01",consecutive_days=2,consecutive_days_sell=2)
#     k0 = k.backtest_prices()
#     k1 = k.backtest_returns()
#     print("k")




import pandas as pd
from zipline import run_algorithm
from zipline.api import order_target_percent, symbol
from zipline.finance import commission, slippage
from zipline.utils.events import date_rules, time_rules

class Algo1Backtest:

    def __init__(self, start_date=None, end_date=None, tickers_list=None,
                 consecutive_days=None, consecutive_days_sell=None):
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
        self.consecutive_days = consecutive_days
        self.consecutive_days_sell = consecutive_days_sell

    def initialize(context):
        context.tickers_list = [symbol(ticker) for ticker in self.tickers_list]
        context.algos = {}

    def handle_data(context, data):
        algo1_data = {}
        for ticker in context.tickers_list:
            signals = self.run_algo1(ticker.symbol)
            algo1_data[ticker.symbol] = {'signals': signals}

        for ticker, data in algo1_data.items():
            algo_signals = data['signals']
            # Implement your trading logic based on algo_signals
            # Example: Buy if signal is 1, Sell if signal is -1
            if 1 in algo_signals:
                order_target_percent(ticker, 1.0)
            elif -1 in algo_signals:
                order_target_percent(ticker, 0.0)

    def run_algo1(self, ticker):
        instance = Algo1(ticker=ticker, start_date=self.start_date,
                         end_date=self.end_date,
                         consecutive_days=self.consecutive_days,
                         consecutive_days_sell=self.consecutive_days_sell)
        signals = instance.generate_signals()
        return signals

    def backtest(self):
        start_date = pd.to_datetime(self.start_date)
        end_date = pd.to_datetime(self.end_date)

        run_algorithm(
            start=start_date,
            end=end_date,
            initialize=self.initialize,
            handle_data=self.handle_data,
            capital_base=100000,
            data_frequency='daily',
            bundle='yahoo_equities',  # Specify the data bundle you want to use
            benchmark_symbol='AAPL',  # Choose a benchmark symbol
            slippage=slippage.FixedSlippage(spread=0.0),
            commission=commission.PerShare(cost=0.001, min_trade_cost=1.0)
        )

if __name__ == "__main__":
    backtester = Algo1Backtest(start_date='2022-01-01', end_date='2022-12-31',
                               tickers_list=['AAPL', 'GOOGL'],
                               consecutive_days=3, consecutive_days_sell=2)
    backtester.backtest()

