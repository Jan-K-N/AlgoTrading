"""
Main script for algo1 backtest.
"""
# pylint: disable=wrong-import-position.
import sys
import pandas as pd
sys.path.insert(0,'/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos')
sys.path.insert(1,'/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
# pylint: disable=import-error.
from algo1 import Algo1
# pylint: disable=import-error.
from finance_database import Database

class Algo1Backtest:
    """
    A class to backtest Algo1. The class uses the output from Algo1.
    """
    def __init__(self,start_date=None,end_date=None,tickers_list=None):
        """
        Initialize the Algo1Backtest object.

        Args:
            start_date (str): The start date of the backtest period. Defaults to None.
            end_date (str): The end date of the backtest period. Defaults to None.
            tickers_list (List[str]): A list of ticker symbols to be used for backtesting.
            Defaults to None.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list

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
        instance_algo1 = Algo1(start_date=self.start_date,
                               end_date=self.end_date,
                               tickers_list=self.tickers_list)
        algo1_output = instance_algo1.algo1_loop()

        return algo1_output

    def backtest_prices(self):
        # pylint: disable=too-many-locals.
        """
        Computes and retrieves the prices from the buy/sell signals obtained from Algo1.

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
            price_data[ticker] = data["Open"]

        algo1_data = Algo1Backtest.run_algo1(self)

        df_buy_signals = pd.DataFrame(columns=['Ticker', 'Buy Signal'])
        df_sell_signals = pd.DataFrame(columns=['Ticker', 'Sell Signal'])

        for df_algo1 in algo1_data:
            ticker = df_algo1['Ticker'][0]
            df_buy = df_algo1.loc[df_algo1['Buy'] == 1]
            df_sell = df_algo1.loc[df_algo1['Sell'] == -1]

            df_buy_signals = pd.concat(
                [df_buy_signals, pd.DataFrame({'Ticker': [ticker] * len(df_buy),
                                               'Buy Signal': df_buy.index})])
            df_sell_signals = pd.concat(
                [df_sell_signals, pd.DataFrame({'Ticker': [ticker] * len(df_sell),
                                                'Sell Signal': df_sell.index})])

        # We will now make the buy/sell prices:
        buy_prices_list = []
        sell_prices_list = []

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
                filtered_df['Buy date'].iloc[j] = mask
                filtered_df.loc[filtered_df['Buy date'] == mask, 'Buy price'] = value

            # Append to the list:
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
                filtered_df_sell['Sell date'].iloc[j] = mask
                filtered_df_sell.loc[filtered_df_sell['Sell date'] == mask, 'Sell price'] = value

            # Append to list:
            sell_prices_list.append(filtered_df_sell)

        return [buy_prices_list, sell_prices_list]

    # pylint: disable=too-many-locals.
    def backtest_returns(self):
        # pylint: disable=too-many-branches.
        """
        Computes and retrieves the returns for each ticker based
        on the buy/sell signals obtained from Algo1.

        Returns:
            List[pd.DataFrame]: A list of pandas DataFrames containing
                the returns data for each ticker. Each DataFrame
                contains the following columns:
                                    - Ticker: Ticker symbol
                                    - Buy Date: Date of buy signal, i.e. one day after the signal.
                                    - Sell Date: Date of sell signal
                                    - Returns: Computed returns for the trade
        """

        prices = Algo1Backtest.backtest_prices(self)

        returns_list = []  # List to store the returns dataframes for each ticker

        # pylint: disable=too-many-nested-blocks
        for ticker1 in self.tickers_list:
            returns_df = pd.DataFrame(columns=['Ticker',
                                               'Buy Date',
                                               'Sell Date',
                                               'Returns',
                                               'Position'])
            position = 0  # Initialize position as 0 (no position)
            latest_sell_date = None  # Initialize latest sell date as None

            for df_buy in prices[0]:
                for df_sell in prices[1]:
                    if not df_buy.empty\
                            and not df_sell.empty\
                            and df_buy['Ticker'].iloc[0] == ticker1 and \
                            df_sell['Ticker'].iloc[0] == ticker1:
                        df_buy = pd.DataFrame(df_buy)
                        df_sell = pd.DataFrame(df_sell)

                        # pylint: disable=unused-variable.
                        for j, row in df_buy.iterrows():
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
                                    returns_df = pd.concat([returns_df, pd.DataFrame(
                                        {'Ticker': [ticker1], 'Buy Date': [timestamp1],
                                         'Sell Date': [sell_date],
                                         'Returns': [returns], 'Position': [position]})])

            returns_df = returns_df.drop(columns=['Position'])
            returns_list.append(returns_df)

        return returns_list
