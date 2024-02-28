"""
Main script for algo1 backtest.
"""
# pylint: disable=wrong-import-position.
# pylint: disable=too-many-locals.
# pylint: disable=too-many-branches.
# pylint: disable=too-many-statements.
# pylint: disable=too-many-nested-blocks.
# pylint: disable=duplicate-code.
import sys
import pandas as pd
import numpy as np
sys.path.append('..')
from algos.algo1 import Algo1
from data.finance_database import Database

class Algo1Backtest:
    """
    A class to backtest Algo1. The class uses the output from Algo1.
    The class contains various backtesting measures to backtest
    the algo.
    """
    # pylint: disable=too-many-arguments.
    def __init__(self,start_date=None,end_date=None,
                 tickers_list=None,consecutive_days=None,
                 consecutive_days_sell=None):
        """
        Initialize the Algo1Backtest object.

        Args:
            start_date (str):
                The start date of the backtest period. Defaults to None.
            end_date (str):
                The end date of the backtest period. Defaults to None.
            tickers_list (List[str]):
                A list of ticker symbols to be used for backtesting.
            Defaults to None.
            consecutive_days (int or None):
                The number of consecutive days the conditions should be met to
                generate signals. If None, the default is None.
            consecutive_days_sell (int or None):
                The number of consecutive days the sell conditions should be met
                to generate signals. If None, the default is None.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
        self.consecutive_days = consecutive_days
        self.consecutive_days_sell = consecutive_days_sell

    def run_algo1(self):
        """
        Executes Algo1 algorithm and returns the output.

        This method initializes an instance of the Algo1 class with the provided
        start and end dates, and a list of tickers.
        It then runs the algo1_loop method to perform the
         algorithm logic and obtain the output.

        Returns:
            algo1_output (Any): The output of the Algo1 algorithm.

        """
        output_list = []
        for ticker1 in self.tickers_list:
            try:
                instance_1 = Algo1(ticker=ticker1,
                                   start_date=self.start_date,
                                   end_date=self.end_date,
                                   consecutive_days=self.consecutive_days,
                                   consecutive_days_sell=self.consecutive_days_sell)
                signals_1 = instance_1.generate_signals()
            except KeyError as error:
                print(f"KeyError for {ticker1}: {str(error)}")
                continue
            except ValueError as error:
                print(f"ValueError for {ticker1}: {str(error)}")
                continue

            condition1 = signals_1[ticker1 + '_Buy'] == 1
            condition2 = signals_1[ticker1 + '_Sell'] == -1

            combined_condition = condition1 | condition2

            extracted_rows = signals_1[combined_condition]

            new_df = pd.DataFrame()
            new_df["Ticker"] = [ticker1] * len(extracted_rows)
            new_df["Buy"] = [1 if b else "" for b in extracted_rows[ticker1 + '_Buy']]
            new_df["Sell"] = [-1 if s else "" for s in extracted_rows[ticker1 + '_Sell']]
            new_df.index = extracted_rows['Date']

            if not new_df.empty:
                output_list.append(new_df)

        algo1_output = output_list

        return algo1_output

    def backtest_prices(self):
        """
        This method computes and retrieves the prices
        given the buy/sell signals from Algo1.

        Returns:
            List[List[pd.DataFrame]]: A list containing two sub-lists:
                - buy_prices_list:
                 List of pandas DataFrames containing buy prices for each ticker.
                - sell_prices_list:
                 List of pandas DataFrames containing sell prices for each ticker.
        """

        price_data = {}

        for ticker in self.tickers_list:
            data = Database.get_price_data(self, start=self.start_date,
                                           end=self.end_date,
                                           ticker=ticker)
            if data is None:
                return pd.DataFrame()
            price_data[ticker] = data["Open"]

        algo1_data = Algo1Backtest.run_algo1(self)

        df_buy_signals = pd.DataFrame(columns=['Ticker', 'Buy Signal'])
        df_sell_signals = pd.DataFrame(columns=['Ticker', 'Sell Signal'])

        df_buy_signals_list = []
        df_sell_signals_list = []

        for df_algo1 in algo1_data:
            ticker = df_algo1.at[df_algo1.index[0], 'Ticker']
            df_buy = df_algo1.loc[df_algo1['Buy'] == 1]
            df_sell = df_algo1.loc[df_algo1['Sell'] == -1]

            buy_df_to_concat = pd.DataFrame({'Ticker': [ticker] * len(df_buy),
                                             'Buy Signal': df_buy.index})

            if not df_buy.empty:

                df_buy_signals_list.append(buy_df_to_concat)

            sell_df_to_concat = pd.DataFrame({'Ticker': [ticker] * len(df_sell),
                                              'Sell Signal': df_sell.index})
            if not sell_df_to_concat.empty:
                df_sell_signals_list.append(sell_df_to_concat)

        if df_buy_signals_list:
            df_buy_signals = pd.concat(df_buy_signals_list, ignore_index=True, sort=False)
        else:
            df_buy_signals = pd.DataFrame(columns=['Ticker', 'Buy Signal'])
        if df_sell_signals_list:
            df_sell_signals = pd.concat(df_sell_signals_list, ignore_index=True, sort=False)
        else:
            df_sell_signals = pd.DataFrame(columns=['Ticker', 'Sell Signal'])
        # We will now make the buy/sell prices:
        buy_prices_list = []
        sell_prices_list = []

        filtered_df_sell = pd.DataFrame(columns=['Ticker',
                                                 'Sell Signal',
                                                 'Sell date',
                                                 'Sell price'])

        for ticker1 in self.tickers_list:
            filtered_df = df_buy_signals[df_buy_signals['Ticker'] == ticker1].copy()
            filtered_df['Buy date'] = pd.to_datetime(
                filtered_df['Buy Signal']).dt.date + pd.DateOffset(days=1)

            for j in range(len(filtered_df)):
                mask = filtered_df['Buy date'].iloc[j]
                value = None
                while value is None:
                    if mask.weekday() < 5:
                        if mask in price_data[ticker1]:
                            value = price_data[ticker1][mask]
                            break
                    mask += pd.DateOffset(days=1)
                filtered_df.loc[filtered_df.index[j], 'Buy date'] = mask
                filtered_df.loc[filtered_df['Buy date'] == mask, 'Buy price'] = value
                filtered_df_sell = filtered_df_sell.reset_index(
                    drop=True) if not filtered_df_sell.empty else pd.DataFrame(
                    columns=['Ticker', 'Sell Signal',
                             'Sell date', 'Sell price'])

                if not filtered_df_sell.empty:
                    filtered_df_sell.loc[filtered_df_sell['Sell date'] == mask,
                    'Sell price'] = value

            # Append to the list:
            if not filtered_df.empty:
                buy_prices_list.append(filtered_df)

            filtered_df_sell = df_sell_signals[
                df_sell_signals['Ticker'] == ticker1].copy()
            filtered_df_sell['Sell date'] = pd.to_datetime(
                filtered_df_sell['Sell Signal']).dt.date + pd.DateOffset(
                days=1)

            for j in range(len(filtered_df_sell)):
                mask = filtered_df_sell['Sell date'].iloc[j]
                value = None
                while value is None:
                    if mask.weekday() < 5:
                        if mask in price_data[ticker1]:
                            value = price_data[ticker1][mask]
                            break
                    mask += pd.DateOffset(days=1)
                filtered_df_sell.loc[filtered_df_sell.index[j], 'Sell date'] = mask
                filtered_df_sell.loc[filtered_df_sell['Sell date'] == mask, 'Sell price'] = value

            # Append to list:
            if not filtered_df_sell.empty:
                sell_prices_list.append(filtered_df_sell)

        return [buy_prices_list, sell_prices_list]

    def backtest_returns(self):
        """
        Backtests the returns for each ticker based on the provided price data.

        Returns a dictionary containing DataFrames with backtested returns for each ticker.

        Returns:
            dict: A dictionary where keys are tickers and values are DataFrames
            containing backtested returns.
                Each DataFrame has the following columns:
                    - 'Ticker': The ticker symbol.
                    - 'Buy Date': The date of the buy transaction.
                    - 'Sell Date': The date of the sell transaction.
                    - 'Returns': The calculated returns.
                    - 'Log returns': The logarithm of the returns.
                Empty DataFrames are filtered out before returning the final dictionary.
        """
        prices = self.backtest_prices()

        returns_dict = {}

        for ticker1 in self.tickers_list:
            returns_df = pd.DataFrame(columns=['Ticker', 'Buy Date',
                                               'Sell Date', 'Returns',
                                               'Log returns'])
            position = 0  # Initialize position as 0 (no position)
            latest_sell_date = None  # Initialize latest sell date as None

            for df_buy in prices[0]:
                for df_sell in prices[1]:
                    if not df_buy.empty and not df_sell.empty \
                            and df_buy['Ticker'].iloc[0] == ticker1 \
                            and df_sell['Ticker'].iloc[0] == ticker1:
                        df_buy = pd.DataFrame(df_buy)
                        df_sell = pd.DataFrame(df_sell)

                        # Initialize variables here
                        timestamp1 = None
                        sell_date = None
                        returns = None
                        log_returns = None

                        new_data = {'Ticker': [ticker1],
                                    'Buy Date': [timestamp1],
                                    'Sell Date': [sell_date],
                                    'Returns': [returns],
                                    'Log returns': [log_returns]}

                        if returns_df.empty:
                            returns_df = pd.DataFrame(new_data)
                        else:
                            returns_df = returns_df.append(new_data, ignore_index=True)

                        for _, row in df_buy.iterrows():
                            if pd.notnull(row['Buy price']):
                                timestamp1 = row['Buy date']
                                buy_price = row['Buy price']

                                # Filter out sell dates before the latest sell date with position=1
                                if latest_sell_date is not None and timestamp1 < latest_sell_date:
                                    continue  # Skip the iteration if there are no valid sell dates

                                # Filter sell dataframe based on the buy date
                                df_sell_filtered = df_sell[df_sell['Sell date'] > timestamp1]

                                # Check if there is a sell_price available
                                if not df_sell_filtered.empty:
                                    sell_price = df_sell_filtered.iloc[0]['Sell price']
                                    sell_date = df_sell_filtered.iloc[0]['Sell date']
                                    latest_sell_date = sell_date  # Update the latest sell date

                                    # Update position based on Buy date and Sell date
                                    if position == 0:  # No position is active
                                        if timestamp1 < sell_date:
                                            position = 1
                                    elif position == 1:  # Position is active
                                        if timestamp1 < sell_date:
                                            position = 0
                                else:
                                    sell_price = None
                                    sell_date = None

                                # Check if there is a remaining sell_price
                                if sell_price is not None:
                                    returns = (sell_price - buy_price) / sell_price
                                    log_returns = np.log1p(returns)
                                    returns_df = pd.concat([returns_df, pd.DataFrame(
                                        {'Ticker': [ticker1],
                                         'Buy Date': [timestamp1],
                                         'Sell Date': [sell_date],
                                         'Returns': [returns],
                                         'Log returns': [log_returns]
                                         })])

            if not returns_df.empty:
                returns_dict[ticker1] = returns_df.dropna()

        # Filter out empty dataframes before returning the final dictionary
        returns_dict = {k: v for k, v in returns_dict.items() if not v.empty}

        return returns_dict

    def backtest_cumulative_returns(self):
        """
        Computes and retrieves the cumulative returns for each ticker based on
        the buy/sell signals obtained from Algo1.

        Returns:
            List[pd.DataFrame]: A list of pandas DataFrames containing
                the cumulative returns data for each ticker. Each DataFrame
                contains the following columns:
                    - Ticker: Ticker symbol
                    - Cumulative Returns: Cumulative returns based on the previous trades
        """
        returns_list = self.backtest_returns()
        cumulative_returns_list = []

        for returns_df in returns_list:
            cumulative_returns = (1 + returns_df['Returns']).cumprod() - 1
            cumulative_returns_df = pd.DataFrame({
                'Ticker': returns_df['Ticker'],
                'Cumulative Returns': cumulative_returns
            })
            cumulative_returns_list.append(cumulative_returns_df)

        return cumulative_returns_list

    def compute_volatility(self):
        """
        Computes and retrieves the volatility of returns for each ticker
        based on the buy/sell signals obtained from Algo1.

        Returns:
            pandas.DataFrame: A DataFrame containing the volatility data for each ticker.
                The DataFrame has the following columns:
                    - Ticker: Ticker symbol
                    - Volatility: Volatility of returns
        """

        volatility_data = []  # Initialize a list to store DataFrames

        database_instance = Database()

        for ticker in self.tickers_list:
            try:
                data_returns = database_instance.compute_stock_return(start=self.start_date,
                                                                      end=self.end_date,
                                                                      ticker=ticker)

                # Check if price data is not empty
                if not data_returns.empty:
                    trading_days = data_returns.shape[0]
                    # Calculate realized volatility as the standard deviation of daily returns
                    realized_volatility = np.sqrt(trading_days) * data_returns.std()

                    # Append DataFrame to the list
                    volatility_data.append(pd.DataFrame({'Ticker': [ticker],
                                                         'Volatility': [realized_volatility]}))
            except ValueError as error:
                # Handle the ValueError here (print a message, log, etc.)
                print(f"Error for {ticker}: {str(error)}")
                continue  # Continue to the next iteration

        if not volatility_data:
            print("No valid tickers with non-empty price data.")
            return pd.DataFrame(columns=['Ticker', 'Volatility'])  # Return an empty DataFrame

        # Concatenate DataFrames in the list
        volatility_df = pd.concat(volatility_data, ignore_index=True)

        return volatility_df
