"""
Main script for arima forecaster.
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

class TimeSeriesForecast:
    def __init__(self, data, steps):
        self.data = data
        self.steps = steps

    def check_stationarity(self):
        # Perform Augmented Dickey-Fuller test for stationarity
        result = adfuller(self.data)
        p_value = result[1]

        if p_value > 0.05:
            print("The time series is not stationary.")
        else:
            print("The time series is stationary.")

    def find_optimal_order(self):
        # Find the optimal order of p and q using AIC
        order_aic = []
        for p in range(3):
            for q in range(3):
                try:
                    model = ARIMA(self.data, order=(p, 0, q))
                    model_fit = model.fit()
                    order_aic.append((p, q, model_fit.aic))
                except:
                    continue

        # Sort the orders based on AIC in ascending order
        order_aic.sort(key=lambda x: x[2])

        # Get the optimal order with the lowest AIC
        optimal_order = order_aic[0][:2]
        print("Optimal Order (p, q):", optimal_order)

        return optimal_order

    def fit_arima(self):
        # Find the optimal order of p and q
        optimal_order = self.find_optimal_order()

        # Fit the ARIMA model with the optimal order
        model = ARIMA(self.data, order=optimal_order)
        model_fit = model.fit()

        return model_fit

    def forecast(self):
        # Check stationarity
        self.check_stationarity()

        # Fit the ARIMA model
        model_fit = self.fit_arima()

        # Make forecasts
        forecast_values = model_fit.forecast(steps=self.steps)[0]

        return forecast_values

# Example usage
# Assuming 'returns' is a pandas Series containing the time series data
ts_forecast = TimeSeriesForecast(returns, steps=5)

# Perform forecasting
forecast_values = ts_forecast.forecast()

print("Forecasted values:", forecast_values)
