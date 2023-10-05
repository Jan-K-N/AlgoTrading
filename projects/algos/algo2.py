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
from finance_database import Database
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

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
        # Buy signals:
        for series in selected_buy_series_list:

            # 3: Data splitting:
            returns = series.iloc[:, 0].values
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
            # regr = RandomForestRegressor(n_estimators=1500,random_state=42)
            # regr.fit(X_train,y_train)

            # Define a grid of hyperparameters to search
            param_grid = {
                'n_estimators': [100, 500, 1000],
                'max_depth': [None, 10, 15],
            }

            # Create the GridSearchCV object
            grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42),
                                       param_grid=param_grid, cv=5)

            # Fit the model to the data and find the best hyperparameters
            grid_search.fit(X_train, y_train)

            # Access the best hyperparameters
            best_params = grid_search.best_params_

            # Create a new model with the best hyperparameters
            best_regr = RandomForestRegressor(
                n_estimators=best_params['n_estimators'],
                max_depth=best_params['max_depth'],
                random_state=42  # Include any other relevant hyperparameters
            )

            # Retrain the model with the best hyperparameters
            best_regr.fit(X_train, y_train)

            y_pred = best_regr.predict(X_test)
            y_pred = y_pred.reshape(-1,1)
            n = y_pred.shape[0]
            last_n_dates = series.index[-n:]
            # Create a structured array with two fields: "prediction" and "date"
            structured_array = np.empty(n, dtype=[('prediction', float), ('date', 'datetime64[ns]'),('Ticker', 'S10')])
            structured_array['prediction'] = y_pred[:, 0]
            structured_array['date'] = last_n_dates
            structured_array['Ticker'] = series.columns[0]

            # Convert the structured array to a DataFrame
            prediction_dataframe = pd.DataFrame(structured_array)

            # Rename the columns if needed
            prediction_dataframe.columns = ['Prediction','Date','Ticker']
            prediction_dataframe['Ticker'] = prediction_dataframe['Ticker'].str.decode('utf-8')

            # 6: Model evaluation:
            predicted_values = prediction_dataframe.iloc[:,[0,2]]

            # Calculate evaluation metrics:
            mae = mean_absolute_error(y_test,predicted_values.iloc[:,0])
            mse = mean_squared_error(y_test, predicted_values.iloc[:,0])
            rmse = np.sqrt(mse)

            # Create a summary dataframe for this pair of dataframes
            evaluation_summary = pd.DataFrame({
                'MAE': [mae],
                'MSE': [mse],
                'RMSE': [rmse],
            })
            evaluation_list.append(evaluation_summary)
            prediction_buy_list.append(prediction_dataframe)

            # Make actual out-of-sample one-step ahead forecast.
            # To do this, we should use the best model from above:
            best_regr = RandomForestRegressor(
                n_estimators=best_params['n_estimators'],
                max_depth=best_params['max_depth'],
                random_state=42  # Include any other relevant hyperparameters
            )

            # Retrain the model with the best hyperparameters on the entire dataset
            best_regr.fit(returns[:-1], returns[1:])



            forecast1 = best_regr.predict(returns[-1].reshape(1, -1))
            last_date = last_n_dates[-1]
            one_day_ahead = last_date + pd.DateOffset(days=1)

            # Create a DataFrame directly
            structured_dateframe_forecasts = pd.DataFrame({
                'Prediction': forecast1,
                'Date': [one_day_ahead],
                'Ticker': series.columns[0]
            })

            # Convert 'Date' column to datetime64[ns]
            structured_dateframe_forecasts['Date'] = pd.to_datetime(structured_dateframe_forecasts['Date'])

            # Append the DataFrame to the list
            one_step_ahead_forecast_list.append(structured_dateframe_forecasts)

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
            regr = RandomForestRegressor(n_estimators=1000, random_state=42)
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
    instance = Algo2(start_date='2023-01-01',end_date='2023-10-04',tickers_list=['TSLA','AAPL','FLS.CO'],
                     days_back=0)
    f = instance.random_forest()
    k = instance.return_data()
