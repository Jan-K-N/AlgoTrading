"""
Main script for arima forecaster.
"""
import pandas as pd
import sys
sys.path.insert(0, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
from finance_database import Database
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
from statsmodels.tsa.statespace.sarimax import SARIMAX

class TimeSeriesForecast:
    def __init__(self, data, steps, train_size=0.75, expanding_window=True):
        self.data = data
        self.steps = steps
        self.train_size = train_size
        self.expanding_window = expanding_window

    def check_stationarity(self):
        # Perform Augmented Dickey-Fuller test for stationarity
        result = adfuller(self.data)
        p_value = result[1]

        if p_value > 0.05:
            print("The time series is not stationary.")
        else:
            print("The time series is stationary.")

    def find_optimal_order(self):
        # Find the optimal order of p, d, and q using AIC
        order_aic = []
        for p in range(3):
            for d in range(2):  # Consider differencing term from 0 to 1
                for q in range(3):
                    try:
                        model = ARIMA(self.data, order=(p, d, q))
                        model_fit = model.fit()
                        order_aic.append((p, d, q, model_fit.aic))
                    except:
                        continue

        # Sort the orders based on AIC in ascending order
        order_aic.sort(key=lambda x: x[3])

        # Get the optimal order with the lowest AIC
        optimal_order = order_aic[0][:3]
        print("Optimal Order (p, d, q):", optimal_order)

        return optimal_order

    def fit_arima(self, train_data):
        # Find the optimal order of p and q
        optimal_order = self.find_optimal_order()

        # Fit the ARIMA model with the optimal order using the training set
        model = SARIMAX(train_data, order=optimal_order)
        model_fit = model.fit()

        return model_fit

    def forecast(self, future_steps=0):
        # Check stationarity
        self.check_stationarity()

        # Determine the test set size
        test_size = len(self.data) - int(len(self.data) * self.train_size)

        # Initialize lists to store forecasts, RMSE, and MAE
        forecasts = []
        rmses = []
        maes = []

        # Perform expanding or rolling window forecast
        if self.expanding_window:
            window_range = range(test_size)
        else:
            window_range = range(test_size - self.steps + 1)

        for i in window_range:
            # Determine the training set size for each iteration
            train_size = len(self.data) - test_size + i

            # Extract the training set for each iteration
            train_data = self.data[:train_size]

            # Fit the ARIMA model for each iteration
            try:
                fitted_model = self.fit_arima(train_data)

                # Make one-step ahead forecast for each iteration
                forecast_value = fitted_model.get_forecast(steps=1).predicted_mean[0]
            except:
                # Handle the case where fitting failed
                # Compute the mean of available data up until the current data point
                mean_value = train_data.mean()

                # Set forecast value to the computed mean
                forecast_value = mean_value

            # Append the forecast to the list
            forecasts.append(forecast_value)

            # Append the actual value to the list for computing RMSE and MAE
            if self.expanding_window:
                actual_value = self.data[train_size + self.steps - 1]
            else:
                actual_value = self.data[train_size + i + self.steps]

            rmses.append(sqrt(mean_squared_error([actual_value], [forecast_value])))
            maes.append(mean_absolute_error([actual_value], [forecast_value]))

        # Compute average RMSE and MAE
        avg_rmse = sum(rmses) / len(rmses)
        avg_mae = sum(maes) / len(maes)

        # Make out-of-sample forecasts if future_steps > 0
        if future_steps > 0:
            fitted_model = self.fit_arima(self.data)

            # Make future forecasts with the optimal order
            future_forecasts = fitted_model.get_forecast(steps=future_steps).predicted_mean
            forecasts.extend(future_forecasts)

        # Handle the case where no forecasts are available
        if len(forecasts) == 0:
            return pd.Series([]), avg_rmse, avg_mae

        return pd.Series(forecasts), avg_rmse, avg_mae


if __name__ == '__main__':
    data_instance = Database(start='2022-12-01', end='2023-05-01', ticker='TSLA')
    data = data_instance.compute_stock_return(start='2022-12-01', end='2023-04-01', ticker='TSLA')
    data2 = data_instance.compute_stock_return(start='2022-12-01', end='2023-05-01', ticker='TSLA')

    # Create an instance of the TimeSeriesForecast class
    ts_forecast = TimeSeriesForecast(data, steps=1, train_size=0.75, expanding_window=True)

    # Perform forecasting
    forecasts, avg_rmse, avg_mae = ts_forecast.forecast(future_steps=1)

    # Print the forecasts, average RMSE, and average MAE
    print("Forecasts:", forecasts)
    print("Average RMSE:", avg_rmse)
    print("Average MAE:", avg_mae)
