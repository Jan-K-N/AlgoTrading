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
import sys
from algo1 import Algo1
sys.path.insert(1,'/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
sys.path.insert(2,'/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/models')
from finance_database import Database
from random_forrest import RandomForrest
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.proportion import proportion_confint

class Algo2:
    def __init__(self,ticker=None, start_date=None,end_date=None, tickers_list=None,
                 days_back = None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
        self.days_back = days_back
        self.db_instance = Database(start=start_date, end=end_date, ticker=ticker)  # Create an instance of the Database class

    def run_algo1(self):
        instance_algo1 = Algo1(start_date=self.start_date,
                               end_date=self.end_date,
                               tickers_list=self.tickers_list)
        algo1_output = instance_algo1.algo1_loop()

        return algo1_output

    def return_data(self):
        """
        Private method for pulling return data from our finance database for multiple tickers.

        Returns:
            A list of DataFrames, where each DataFrame contains return data for a specific ticker.
        """
        return_data_list = []  # Create an empty list to store return data DataFrames for each ticker

        for ticker in self.tickers_list:
            # Calculate the start date based on self.days_back
            start_date = datetime.strptime(self.start_date, "%Y-%m-%d") - timedelta(days=self.days_back)
            start_date = start_date.strftime("%Y-%m-%d")  # Convert back to string format

            return_data = self.db_instance.compute_stock_return(start=start_date, end=self.end_date, ticker=ticker)

            return_data_list.append(return_data)  # Append return data DataFrame to the list

        return return_data_list

    def determine_position_exit(self, latest_price,
                                reference_price,
                                pct_stop_loss = 0.02,
                                returns_series=None,
                                forecast_target=None):
        """
        Method to control our position. The method is used after having taken a long position.
        The method is used to control exit
        positions. Hence, it includes a stop-loss mechanism.

        # Ideas:
            # Liquidity Considerations.
                # Factor in liquidity constraints. If the instrument becomes less liquid,
                it might be harder to exit at a desired price.


        """
        stop_loss = reference_price - reference_price * pct_stop_loss

        if returns_series is not None:
            # Monte-Carlo:

            # 1. Modelling:
            initial_price = latest_price
            mu = returns_series.mean()
            sigma = returns_series.std()
            volatility = 0.3
            drift = 0.2
            time_horizon = 252
            # threshold_distance = 5  # Distance from target to consider as a hit

            # 2. Simulating:
            num_simulations = 10000
            # Generate random daily returns for each simulation using a more sophisticated model
            returns = np.random.normal((mu - 0.5 * volatility ** 2) / time_horizon, volatility / np.sqrt(time_horizon),
                                       (time_horizon, num_simulations))

            # Initialize an array to store simulated prices
            simulated_prices = np.zeros((time_horizon + 1, num_simulations))
            simulated_prices[0] = initial_price

            # Simulate daily prices using geometric Brownian motion with drift
            simulated_returns = np.exp(np.cumsum(returns, axis=0))
            simulated_prices[1:] = initial_price * np.exp(np.cumsum(returns, axis=0))

            std_simulated_prices = np.std(simulated_prices[-1, :])
            num_std_devs = 2
            threshold_distance = num_std_devs * std_simulated_prices

            # Calculate probabilities of hitting the target price for each simulation
            target_price = forecast_target

            # Calculate distances from the target price for each simulation
            distances_from_target = np.abs(simulated_prices[-1, :] - target_price)

            # Calculate probabilities of hitting the target price for each simulation
            probability_hit_target = np.sum(distances_from_target < threshold_distance) / num_simulations

            # Calculate confidence interval
            lower_ci, upper_ci = proportion_confint(np.sum(probability_hit_target), num_simulations, method='wilson')

            if reference_price > target_price:
                return -1
            elif probability_hit_target > 0.5 and latest_price > stop_loss:
                return 1
            elif latest_price < stop_loss:
                return -1
            # We stay long in the position as long as the following is true:
            elif probability_hit_target < 0.2 and latest_price > stop_loss:
                return -1

        # If returns_series is None, you might want to handle this case differently.
        # For now, return None.
        return None


    def random_forest(self):
        """
        Function for creating a random forest for the stock return.
        Input to the rf should be the stock returns from the suggested
        stocks from algo1. If there is a buy/sell signal for a given date,
        we pull the return data for the given stock up till that day.
        Then we run a random forest model to predict the probability
        of a up/down movement.

        Returns:

        """
        algo1_signals = self.run_algo1()

        # Initialize empty lists to store DataFrames for buy and sell signals
        buy_dataframes = []
        sell_dataframes = []

        for prediction_dataframe in algo1_signals:
            # Access the "buy" and "sell" columns by name
            ticker_column = prediction_dataframe.iloc[:, 0]
            buy_column = prediction_dataframe.iloc[:, 1]
            sell_column = prediction_dataframe.iloc[:, 2]

            # Create empty DataFrames to store the filtered buy and sell data
            filtered_buy_df = pd.DataFrame(columns=['Ticker', 'Buy_Date'])
            filtered_sell_df = pd.DataFrame(columns=['Ticker', 'Sell_Date'])

            # Iterate through buy and sell signals
            for date, ticker, buy_signal, sell_signal in zip(prediction_dataframe.index, ticker_column, buy_column, sell_column):
                if buy_signal == 1:
                    buy_date = date  # Update buy_date when a "buy" signal is found
                    ticker_name = ticker
                    filtered_buy_df = pd.concat(
                        [filtered_buy_df, pd.DataFrame({'Ticker': [ticker_name], 'Buy_Date': [buy_date]})],
                        ignore_index=True)
                if sell_signal == -1:
                    sell_date = date  # Update sell_date when a "sell" signal is found
                    ticker_name = ticker
                    filtered_sell_df = pd.concat(
                        [filtered_sell_df, pd.DataFrame({'Ticker': [ticker_name], 'Sell_Date': [sell_date]})],
                        ignore_index=True)

            # Append the filtered buy and sell DataFrames to their respective lists
            buy_dataframes.append(filtered_buy_df)
            sell_dataframes.append(filtered_sell_df)

        # Now we can create some return vectors, where the end-date point is given by
        # the last date, which we get from buy_dataframes and sell_dataframes.

        # 1: Data preparation:
        returns = self.return_data()

        selected_buy_series_list = []
        selected_sell_series_list = []

        for prediction_dataframe, df1, df2 in zip(buy_dataframes, returns, sell_dataframes):
            buy_column = prediction_dataframe.iloc[:, 1]
            sell_column = df2.iloc[:, 1]

            for i in range(0, len(buy_column)):
                buy_date = buy_column[i]
                if buy_date in df1.index:
                    selected_buy_series = df1.loc[df1.index <= buy_date]
                    # Add a new column with the last index value
                    selected_buy_series['buy_signal_date'] = buy_date
                    selected_buy_series_list.append(selected_buy_series)
                else:
                    # If 'buy_date' is not in the DataFrame's index, append an empty series:
                    selected_buy_series_list.append(pd.Series())

            for j in range(0, len(sell_column)):
                sell_date = sell_column[j]
                if sell_date in df1.index:
                    selected_sell_series = df1.loc[df1.index <= sell_date]
                    # Add a new column with the last index value
                    selected_sell_series['sell_signal_date'] = sell_date
                    selected_sell_series_list.append(selected_sell_series)
                else:
                    selected_sell_series_list.append(pd.Series())

        # 2. Data exploration.
            # This should be added later, and it should include:
                # Correlations.
                # Potential outliers.

        prediction_buy_list = []
        prediction_sell_list = []
        evaluation_list = []
        one_step_ahead_forecast_list = []

        # Common hyperparameters for RandomForestRegressor
        common_regr_params = {
            'random_state': 42,
        }

        # Buy signals:
        for series in selected_buy_series_list:
            returns = series.iloc[:, 0].values
            returns = returns[:-1]

            # Reshape "returns" to have two dimensions
            returns = returns.reshape(-1, 1)

            random_forrest_instance = RandomForrest(series=returns[:-1],x_data=returns[1:])
            random_forrest_predictor = random_forrest_instance.predictor()
            one_day_ahead = series.index[-len(random_forrest_predictor[2]):] + pd.DateOffset(days=1)

            # Create a DataFrame directly
            structured_dateframe_forecasts = pd.DataFrame({
                'Prediction': random_forrest_predictor[2].item(),
                'Date': [one_day_ahead],
                'Ticker': series.columns[0]
            })

            structured_dateframe_forecasts['Date']=structured_dateframe_forecasts['Date'].item()[0]

            # Append the DataFrame to the list
            one_step_ahead_forecast_list.append(structured_dateframe_forecasts)

            signals_list_buy = []
            signals_list_buy_updated = []
            for ticker in self.tickers_list:
                for df in one_step_ahead_forecast_list:
                    new_df = pd.DataFrame()
                    new_df["Ticker"] = [ticker]
                    new_df['Position'] = None
                    new_df['Buy price'] = None
                    new_df['Position date'] = None
                    if df['Prediction'].iloc[0] > 0:
                        new_df.at[0, 'Position'] = 1
                        prices = self.db_instance.get_price_data(start=self.start_date,
                                                                          end=self.end_date,
                                                                          ticker=ticker)['Adj Close']

                        # Find the index of the closest date in the array
                        last_date2 = df['Date'].iloc[-1]
                        one_day_ahead2 = last_date2 + pd.DateOffset(days=1)


                        index_of_closest_date = np.abs(prices.index - last_date2).argmin()

                        # Check if there is a next element
                        if index_of_closest_date + 1 < len(prices):
                            # Access the next element
                            next_element = prices.index[index_of_closest_date + 1]
                            buy_price = prices.loc[next_element]
                            new_df['Buy price'] = buy_price
                            new_df['Position date'] = next_element
                            signals_list_buy.append(new_df)
                        else:
                            print("No next element. The last_date is the last element in price_at_signal.")
                    print("k")

                # Now monitor:

                # Initialize final_df for each ticker
                final_df = pd.DataFrame()
                for df2 in signals_list_buy:
                    new_df2 = pd.DataFrame()
                    new_df2["Ticker"] = [ticker]
                    new_df2['Position'] = None
                    new_df2['Latest price'] = None
                    new_df2['Position date'] = None
                    first_iteration = True  # Flag for the first iteration

                    while True:
                        prices_actual = self.db_instance.get_price_data(start=self.start_date,
                                                                        end=self.end_date,
                                                                        ticker=ticker)['Adj Close']
                        if first_iteration:
                            last_date2 = df2['Position date'].iloc[0]
                            index_of_closest_date2 = np.abs(prices_actual.index - last_date2).argmin()
                        else:
                            last_date2 = new_df2['Position date'].iloc[-1]
                            index_of_closest_date2 = np.abs(prices_actual.index - last_date2).argmin()

                        if index_of_closest_date2 + 1 < len(prices_actual):
                            next_element2 = prices_actual.index[index_of_closest_date2 + 1]

                            # Calculate the returns. Should be used for forecasting in the monitor process.
                            returns_actual = prices_actual.loc[:next_element2].pct_change().dropna()
                            order = (2,1,2) # Tune later.
                            model = ARIMA(returns_actual,order=order)
                            results = model.fit()
                            # forecasts = results.forecast(steps=5)[-1]
                            forecasts_array = results.forecasts
                            last_row = forecasts_array[-1]
                            forecasts = last_row[-1]
                            target = (df2['Buy price'].iloc[0]+df2['Buy price'].iloc[0]*forecasts).item()

                            # Calculate the latest price
                            latest_price = prices_actual.loc[next_element2]

                            # Update the Position based on your condition
                            if first_iteration:
                                # In the if-statement below, we control our position:
                                if self.determine_position_exit(latest_price,
                                                                reference_price=df2['Buy price'].iloc[0],
                                                                returns_series=returns_actual,
                                                                forecast_target=target) == 1: #latest_price > df2['Buy price'].iloc[0]: #forecasts.item() > 0:
                                    new_df2['Position'] = 1
                                else:
                                    new_df2['Position'] = -1
                                    break  # Break the loop if the condition is not fulfilled
                                # Update new_df2 with the latest price and date
                                new_df2['Latest price'] = latest_price
                                new_df2['Position date'] = next_element2
                                first_iteration = False  # Update the flag after the first iteration
                            else:
                                # In the if-statement below, we control our position:
                                if self.determine_position_exit(latest_price, reference_price=df2['Buy price'].iloc[0]) == 1:  #latest_price > new_df2['Latest price'].iloc[0]: # forecasts.item() > 0:
                                    new_df2['Position'] = 1
                                else:
                                    new_df2['Position'] = -1
                                    break  # Break the loop if the condition is not fulfilled
                                # Update new_df2 with the latest price and date
                                new_df2['Latest price'] = latest_price
                                new_df2['Position date'] = next_element2
                        else:
                            # Break the loop if there is no next element
                            break

                    # Append the final DataFrame to the updated list
                    final_df = pd.concat([df2, new_df2], axis=0, ignore_index=True)

                signals_list_buy_updated.append(final_df)


        print("k")

        # Sell signals: <----------------------------------------
        for series_sell in selected_sell_series_list:
            # 3: Data splitting:
            returns = series_sell.iloc[:, 0].values
            returns = returns[:-1]

            # Reshape "returns" to have two dimensions
            returns = returns.reshape(-1, 1)

            # 3: Splitting the data:
            X_train, X_test, y_train, y_test = train_test_split(returns[:-1], returns[1:], test_size=0.25,
                                                                random_state=42)

            # 4: Feature Engineering:
            # This should be added later, and it should include:
            # Detecting missing data or scaling features.

            # 5: Model Training:
            regr = RandomForestRegressor(n_estimators=10, random_state=42)
            regr.fit(X_train, y_train)

            y_pred = regr.predict(X_test)
            y_pred = y_pred.reshape(-1, 1)
            n = y_pred.shape[0]
            last_n_dates = series_sell.index[-n:]
            # Create a structured array with two fields: "prediction" and "date"
            structured_array = np.empty(n, dtype=[('prediction', float), ('date', 'datetime64[ns]'),
                                                  ('Ticker', 'S10')])
            structured_array['prediction'] = y_pred[:, 0]
            structured_array['date'] = last_n_dates
            structured_array['Ticker'] = series_sell.columns[0]

            # Convert the structured array to a DataFrame
            prediction_dataframe = pd.DataFrame(structured_array)

            # Rename the columns if needed
            prediction_dataframe.columns = ['Prediction', 'Date', 'Ticker']
            prediction_dataframe['Ticker'] = prediction_dataframe['Ticker'].str.decode('utf-8')

            prediction_sell_list.append(prediction_dataframe)

        # 6: Model evaluation:

        # 7: Model Interpretation:
            # Analyze feature importance to understand which features contribute most.

        # 8: Model Tuning.

        # 9: Cross-Validation.

        # 10: Repeat step 1-9, until satisfactory result.

        # 11: Model Deployment.
            # Let the model make predictions on new, unseen data.

        # 12: Monitoring and Maintenance.
            # Monitor the model's performance in a production environment.
            # Update data and model if necessary.


if __name__ == '__main__':
    instance = Algo2(start_date='2023-01-01',end_date='2023-10-04',tickers_list=['FLS.CO','TSLA','AAPL'],
                     days_back=0)
    f = instance.random_forest()
    k = instance.return_data()
    f1 = instance.determine_position_exit(return_series = k[0])
    print("k")
