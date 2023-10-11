"""
Main script for algo2. This algo will find signals in the same way
as algo1. However, instead of considering these signals as
signals to buy/sell, this algo will instead only use them as
a way to way stock candidates. When these candidates
are found, a Random Forrest to predict the stock return
for the next day. The direction of this predicted
stock return, serves as the actual signal for the algo.
The opposite movement for the position is then determined
by this specific algorithm.
"""
# pylint: disable=import-error
# pylint: disable=wrong-import-position
# pylint: disable=inconsistent-return-statements
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
import sys
from datetime import datetime, timedelta
from typing import Union, Optional

import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportion_confint
from statsmodels.tsa.arima.model import ARIMA

# Ensure that the paths are inserted before importing local modules
sys.path.insert(1, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
sys.path.insert(2, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/models')

from finance_database import Database
from random_forrest import RandomForrest
from algo1 import Algo1

class Algo2:
    """
    Class for implementing Algorithm 2.

    This algorithm involves running Algorithm 1 (Algo1), creating a random forest
    for stock returns based on the signals generated by Algo1, and monitoring the
    stock positions with a stop-loss mechanism and Monte Carlo simulation.

    Parameters:
        ticker (str): Ticker symbol of the stock.
        start_date (str): Start date for the analysis in "YYYY-MM-DD" format.
        end_date (str): End date for the analysis in "YYYY-MM-DD" format.
        tickers_list (List[str]): List of ticker symbols for multiple stocks.
        days_back (int): Number of days for calculating the start date based on historical data.

    Attributes:
        ticker (str): Ticker symbol of the stock.
        start_date (str): Start date for the analysis in "YYYY-MM-DD" format.
        end_date (str): End date for the analysis in "YYYY-MM-DD" format.
        tickers_list (List[str]): List of ticker symbols for multiple stocks.
        days_back (int): Number of days for calculating the start date based on historical data.
        db_instance (Database): An instance of the Database class for fetching financial data.

    Methods:
        run_algo1(): Run Algorithm 1 and return its output.
        return_data(): Fetch return data for multiple tickers from the finance database.
        monte_carlo_monitor(): Monitor a long position with a
        stop-loss mechanism and Monte Carlo simulation.
        random_forest(): Create a random forest for stock returns based on Algo1 signals.

    """

    # pylint: disable=too-many-arguments
    def __init__(self, ticker=None, start_date=None,
                 end_date=None, tickers_list=None, days_back=None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
        self.days_back = days_back
        self.db_instance = Database(start=start_date, end=end_date, ticker=ticker)

    def run_algo1(self):
        """
        Run Algorithm 1 and return its output.

        Returns:
            Output of Algorithm 1.
        """
        instance_algo1 = Algo1(start_date=self.start_date,
                               end_date=self.end_date,
                               tickers_list=self.tickers_list)
        algo1_output = instance_algo1.algo1_loop()
        return algo1_output

    def return_data(self):
        """
        Private method for pulling return data from the finance database for multiple tickers.

        Returns:
            List of DataFrames, where each DataFrame contains return data for a specific ticker.
        """
        return_data_list = []

        for ticker in self.tickers_list:
            start_date = datetime.strptime(self.start_date,
                                           "%Y-%m-%d") - timedelta(
                days=self.days_back)
            start_date = start_date.strftime("%Y-%m-%d")
            return_data = self.db_instance.compute_stock_return(start=start_date,
                                                                end=self.end_date,
                                                                ticker=ticker)
            return_data_list.append(return_data)

        return return_data_list

    # pylint: disable=too-many-locals
    @staticmethod
    def monte_carlo_monitor(
        latest_price: float,
        reference_price: float,
        pct_stop_loss: float = 0.02,
        returns_series: Optional[np.ndarray] = None,
        forecast_target: Optional[float] = None
    ) -> Union[int, None]:
        """
        Method to control a long position, including a stop-loss mechanism
        and Monte Carlo simulation.

        Parameters:
            latest_price (float): The latest price of the asset.
            reference_price (float): The reference price for calculations.
            pct_stop_loss (float, optional): The percentage for the stop-loss mechanism.
            Defaults to 0.02.
            returns_series (np.ndarray, optional): Array of historical returns for
            Monte Carlo simulation.
            forecast_target (float, optional): The target price made by forecasting.

        Returns:
            Union[int, None]: Action signal based on the conditions.
                - 1: Buy/hold signal
                - -1: Sell signal
                - None: No action

        Notes:
            Liquidity considerations may impact the effectiveness of the exit strategy.
        """
        stop_loss = reference_price - reference_price * pct_stop_loss

        if returns_series is not None:
            # Monte-Carlo:

            # 1. Modelling:
            initial_price = latest_price
            mean_return = returns_series.mean()
            volatility = 0.3
            time_horizon = 252

            # 2. Simulating:
            num_simulations = 10000
            returns = np.random.normal(
                (mean_return - 0.5 * volatility ** 2) / time_horizon,
                volatility / np.sqrt(time_horizon),
                (time_horizon, num_simulations)
            )

            simulated_prices = np.zeros((time_horizon + 1, num_simulations))
            simulated_prices[0] = initial_price

            simulated_prices[1:] = initial_price * np.exp(np.cumsum(returns, axis=0))

            std_simulated_prices = np.std(simulated_prices[-1, :])
            num_std_devs = 2
            threshold_distance = num_std_devs * std_simulated_prices

            target_price = forecast_target

            distances_from_target = np.abs(simulated_prices[-1, :] - target_price)

            probability_hit_target = np.sum(distances_from_target
                                            < threshold_distance) / num_simulations

            lower_ci, upper_ci = proportion_confint(np.sum(probability_hit_target),
                                                    num_simulations,
                                                    method='wilson')

            if reference_price > target_price:
                return -1
            if probability_hit_target > 0.5 \
                    and latest_price > stop_loss \
                    and 0 < lower_ci or 0 > upper_ci:
                return 1
            if latest_price < stop_loss:
                return -1
            if probability_hit_target < 0.2 and latest_price > stop_loss:
                return -1

    # pylint: disable=too-many-locals
    def random_forest(self):
        """
        Function for creating a random forest for stock returns.

        Returns:
            List of DataFrames: Buy/sell signals and related information.
        """
        algo1_signals = self.run_algo1()
        buy_dataframes = []
        sell_dataframes = []

        for prediction_dataframe in algo1_signals:
            ticker_column = prediction_dataframe.iloc[:, 0]
            buy_column = prediction_dataframe.iloc[:, 1]
            sell_column = prediction_dataframe.iloc[:, 2]

            filtered_buy_df = pd.DataFrame(columns=['Ticker', 'Buy_Date'])
            filtered_sell_df = pd.DataFrame(columns=['Ticker', 'Sell_Date'])

            for date, ticker, buy_signal, sell_signal in zip(prediction_dataframe.index,
                                                             ticker_column,
                                                             buy_column,
                                                             sell_column):
                if buy_signal == 1:
                    buy_date = date
                    ticker_name = ticker
                    filtered_buy_df = pd.concat(
                        [filtered_buy_df, pd.DataFrame({'Ticker': [ticker_name],
                                                        'Buy_Date': [buy_date]})],
                        ignore_index=True)
                if sell_signal == -1:
                    sell_date = date
                    ticker_name = ticker
                    filtered_sell_df = pd.concat(
                        [filtered_sell_df, pd.DataFrame({'Ticker': [ticker_name],
                                                         'Sell_Date': [sell_date]})],
                        ignore_index=True)

            buy_dataframes.append(filtered_buy_df)
            sell_dataframes.append(filtered_sell_df)

        returns = self.return_data()
        selected_buy_series_list = []
        selected_sell_series_list = []

        for prediction_dataframe, df1, df2 in zip(buy_dataframes, returns, sell_dataframes):
            buy_column = prediction_dataframe.iloc[:, 1]
            sell_column = df2.iloc[:, 1]

            for _, buy_date in enumerate(buy_column):
                if buy_date in df1.index:
                    selected_buy_series = df1.loc[df1.index <= buy_date]
                    selected_buy_series['buy_signal_date'] = buy_date
                    selected_buy_series_list.append(selected_buy_series)
                else:
                    selected_buy_series_list.append(pd.Series())

            for _, sell_date in enumerate(sell_column):
                if sell_date in df1.index:
                    selected_sell_series = df1.loc[df1.index <= sell_date]
                    selected_sell_series['sell_signal_date'] = sell_date
                    selected_sell_series_list.append(selected_sell_series)
                else:
                    selected_sell_series_list.append(pd.Series())

        one_step_ahead_forecast_list = []
        # pylint: disable=too-many-nested-blocks
        for series in selected_buy_series_list:
            returns = series.iloc[:, 0].values
            returns = returns[:-1]
            returns = returns.reshape(-1, 1)

            random_forest_instance = RandomForrest(series=returns[:-1], x_data=returns[1:])
            random_forest_predictor = random_forest_instance.predictor()
            one_day_ahead = series.index[-len(random_forest_predictor[2]):] + pd.DateOffset(days=1)

            structured_dataframe_forecasts = pd.DataFrame({
                'Prediction': random_forest_predictor[2].item(),
                'Date': [one_day_ahead],
                'Ticker': series.columns[0]
            })

            structured_dataframe_forecasts['Date'] =\
                structured_dataframe_forecasts['Date'].item()[0]

            one_step_ahead_forecast_list.append(structured_dataframe_forecasts)

            signals_list_buy = []
            signals_list_buy_updated = []

            for ticker in self.tickers_list:
                for forecast_dataframe in one_step_ahead_forecast_list:
                    new_df = pd.DataFrame()
                    new_df["Ticker"] = [ticker]
                    new_df['Position'] = None
                    new_df['Buy price'] = None
                    new_df['Position date'] = None

                    if forecast_dataframe['Prediction'].iloc[0] <= 0:
                        continue

                    prices = self.db_instance.get_price_data(
                        start=self.start_date,
                        end=self.end_date,
                        ticker=ticker
                    )['Adj Close']

                    last_date2 = forecast_dataframe['Date'].iloc[-1]
                    index_of_closest_date = np.abs(prices.index - last_date2).argmin()

                    if index_of_closest_date + 1 >= len(prices):
                        continue

                    next_element = prices.index[index_of_closest_date + 1]
                    buy_price = prices.loc[next_element]

                    new_df['Buy price'] = buy_price
                    new_df['Position date'] = next_element

                    signals_list_buy_updated.append(new_df)

                final_df = pd.DataFrame()
                for df2 in signals_list_buy:
                    new_df2 = pd.DataFrame()
                    new_df2["Ticker"] = [ticker]
                    new_df2['Position'] = None
                    new_df2['Latest price'] = None
                    new_df2['Position date'] = None
                    first_iteration = True

                    while True:
                        prices_actual = self.db_instance.get_price_data(start=self.start_date,
                                                                        end=self.end_date,
                                                                        ticker=ticker)['Adj Close']

                        if first_iteration:
                            last_date2 = df2['Position date'].iloc[0]
                            index_of_closest_date2 = np.abs(prices_actual.index
                                                            - last_date2).argmin()
                        else:
                            last_date2 = new_df2['Position date'].iloc[-1]
                            index_of_closest_date2 = np.abs(
                                prices_actual.index - last_date2).argmin()

                        if index_of_closest_date2 + 1 < len(prices_actual):
                            next_element2 = prices_actual.index[index_of_closest_date2 + 1]
                            returns_actual = prices_actual.loc[:next_element2].pct_change().dropna()
                            order = (2, 1, 2)
                            model = ARIMA(returns_actual, order=order)
                            results = model.fit()
                            forecasts_array = results.forecasts
                            last_row = forecasts_array[-1]
                            forecasts = last_row[-1]
                            target = (df2['Buy price'].iloc[0]
                                      + df2['Buy price'].iloc[0] * forecasts).item()

                            latest_price = prices_actual.loc[next_element2]

                            if first_iteration:
                                if self.monte_carlo_monitor(
                                        latest_price,
                                        reference_price=df2['Buy price'].iloc[0],
                                        returns_series=returns_actual,
                                        forecast_target=target) == 1:
                                    new_df2['Position'] = 1
                                else:
                                    new_df2['Position'] = -1
                                    break
                                new_df2['Latest price'] = latest_price
                                new_df2['Position date'] = next_element2
                                first_iteration = False
                            else:
                                if self.monte_carlo_monitor(
                                        latest_price,
                                        reference_price=df2['Buy price'].iloc[0]) == 1:
                                    new_df2['Position'] = 1
                                else:
                                    new_df2['Position'] = -1
                                    break
                                new_df2['Latest price'] = latest_price
                                new_df2['Position date'] = next_element2
                        else:
                            break

                    final_df = pd.concat([df2, new_df2], axis=0, ignore_index=True)

                signals_list_buy_updated.append(final_df)

        return signals_list_buy_updated


if __name__ == '__main__':
    instance = Algo2(start_date='2022-06-01',end_date='2023-10-04',tickers_list=['AAPL'],
                     days_back=0)
    f = instance.random_forest()
    k = instance.return_data()
    # f1 = instance.monte_carlo_monitor(return_series = k[0])
    print("k")
