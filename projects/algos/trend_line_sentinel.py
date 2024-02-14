"""
The term "Sentinel" generally refers to a guard or watchman,
someone or something that stands watch or keeps vigil.
In the context of the algorithm name "TrendLine Sentinel,"
it implies that the algorithm acts as a vigilant observer or guardian of trends,
making decisions based on the information derived from linear regression lines
to protect or optimize the trading strategy.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("..")
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from data.finance_database import Database
from sklearn.model_selection import GridSearchCV
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from algo_scrapers.s_and_p_scraper import SAndPScraper

class sentinel:

    def __init__(self,start_date=None,
                 end_date=None,ticker=None,
                 tickers_list=None,window=50):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list
        self.window = window
        self.signals = None

    def sentinel_data(self):
        """
        Method for pulling data from the finance database.
        Returns:

        """
        data = Database.get_price_data(self,ticker=self.ticker,start=self.start_date,
                                       end=self.end_date)['Adj Close']
        data = pd.DataFrame(data.values, index=data.index, columns=[self.ticker])

        return data

    def sentinel_features_data(self, y_ticker="TSLA"):
        """
        This method should be used to create a dataframe containing the
        variables which are most correlated with a given ticker/stock
        Returns:
        """

        scraper = SAndPScraper()
        feature_set = scraper.run_scraper()

        sentinel_features = pd.DataFrame()
        for ticker in feature_set:
            sentinel_features[ticker] = Database.get_price_data(self, ticker=ticker, start=self.start_date,
                                                                end=self.end_date)['Adj Close']

        # Drop the column corresponding to self.ticker if it exists
        if y_ticker in sentinel_features.columns:
            sentinel_features.drop(columns=y_ticker, inplace=True)

        return sentinel_features
    def generate_signals(self):
        """
        Method for generating signals based on a linear regression method.
        Signals are made in the following way:

            - Buy:
                When the current/latest price of the stock is above the regression line,
                we generate a buy signal, indicating that the stock is
                potentially undervalued or trending upwards.
            - Sell:
                When the current price is below the regression line,
                we generate a sell signal, suggesting that the stock may
                be overvalued or trending downwards.

        Trading Orders: Using these buy and sell signals, we generate trading orders:
        When transitioning from a sell signal to a buy signal, we place a buy order, indicating a long position.
        When transitioning from a buy signal to a sell signal, we place a sell order, indicating a short position.

        Returns:

        """
        data = self.sentinel_data()
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        x = np.arange(len(data)).reshape(-1, 1)
        y = data.values.reshape(-1, 1)

        # Incorporate seasonal component into the feature matrix
        decomposition = seasonal_decompose(data[self.ticker], model='additive', period=7)
        seasonal = decomposition.seasonal

        # Scale the seasonal component to increase its weight
        seasonal_scaled = seasonal  # Adjust the scaling factor as needed

        # Use sine and cosine functions to represent seasonal patterns
        seasonal_sin = np.sin(2 * np.pi * np.arange(len(data)) / 7)
        seasonal_cos = np.cos(2 * np.pi * np.arange(len(data)) / 7)

        data2 = self.sentinel_features_data()


        X = np.column_stack((x, seasonal_sin, seasonal_cos, seasonal_scaled, data2))

        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a pipeline for Lasso regression
        lasso_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')), # Impute missing values by mean.
            ('scaler', StandardScaler()),
            ('lasso', Lasso(alpha=0.1))
        ])

        # Fit Lasso regression
        lasso_pipeline.fit(X_train, y_train)

        # Transform the features using Lasso
        X_test_lasso = lasso_pipeline['imputer'].transform(X_test)
        X_test_lasso = lasso_pipeline['scaler'].transform(X_test)
        X_train_lasso = lasso_pipeline.fit_transform(X_train, y_train)

        # Create a pipeline for Gradient Boosting Regressor
        gbr_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('gbr', GradientBoostingRegressor())
        ])

        # Define hyperparameters grid for GridSearchCV
        param_grid = {
            'gbr__n_estimators': [50, 100, 300],  # Adjust number of boosting stages
            'gbr__max_depth': [3, 4, 5],  # Adjust maximum depth of individual trees
            'gbr__learning_rate': [0.01, 0.1, 0.2]  # Adjust learning rate
        }

        # Perform grid search with cross-validation
        grid_search = GridSearchCV(gbr_pipeline, param_grid, cv=10, scoring='neg_mean_squared_error')
        grid_search.fit(X_train_lasso, y_train)

        # Transform the test data using the same scaler
        X_test_lasso_scaled = lasso_pipeline['scaler'].transform(X_test_lasso)

        # Get the best model from grid search
        best_model = grid_search.best_estimator_

        # Make predictions on the test set
        y_pred = best_model.predict(X_test_lasso_scaled)

        # Compute RMSE
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Set threshold
        threshold = 5  # Define your threshold value

        # Use the forecast if RMSE is below the threshold
        if rmse <= threshold:
            print("Forecast RMSE is below the threshold. Using the forecast.")

            # Iterate over the data and generate signals
            for i in range(len(data)):
                # Use the best model for 1-step ahead prediction
                forecast = best_model.predict(X[i].reshape(1, -1))

                # Determine the direction of the forecasted market movement
                if forecast > data.iloc[i].values:  # If forecast is greater than the observed value
                    signals.loc[data.index[i], 'signal'] = 1.0  # Go long
                else:
                    signals.loc[data.index[i], 'signal'] = -1.0  # Go short

            # Generate trading orders
            signals['positions'] = signals['signal'].diff().fillna(0)

        else:
            print("Forecast RMSE is above the threshold. Discarding the forecast.")
            # Handle the case where the forecast does not meet the threshold

        return signals

    def plot_signals(self):
        fig, ax = plt.subplots(figsize=(12, 8))

        data = self.sentinel_data()

        # Plotting historical price data, dropping the first observation
        ax.plot(data.index[1:], data[self.ticker].iloc[1:], label='Price', linewidth=2)

        signals = self.generate_signals()

        # # Plotting fitted values, dropping the first observation
        # ax.plot(data.index[1:], signals['regression_line'].iloc[1:], label='Fitted Values', linestyle='--',
        #         color='orange')

        # Plotting buy signals
        buy_indices = signals[signals['signal'] == 1.0].index
        buy_values = data[self.ticker][signals['signal'] == 1.0]
        ax.plot(buy_indices, buy_values, '^', markersize=10, color='g', label='Buy Signal')

        # Plotting sell signals
        sell_indices = signals[signals['signal'] == -1.0].index
        sell_values = data[self.ticker][signals['signal'] == -1.0]
        ax.plot(sell_indices, sell_values, 'v', markersize=10, color='r', label='Sell Signal')

        # ax.set_title('Linear Regression Trading Strategy')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()

        plt.show()

    def backtest(self):
        """
        Method for backtesting the trading strategy.
        Returns:
            dict: A dictionary containing backtest results.
        """
        # Generate signals
        signals = self.generate_signals()

        # Initialize variables
        initial_cash = 10000  # Initial cash amount
        cash = initial_cash
        position = 0  # Initial position (no position)
        last_signal = 0  # Initial signal (no signal)
        positions = []  # Store positions for analysis

        # Iterate over signals and calculate returns
        for index, signal in signals.iterrows():
            if signal['positions'] == 1 and last_signal != 1:  # Buy signal
                shares_bought = cash / signals.loc[index, self.ticker]
                position = shares_bought
                cash = 0
                last_signal = 1
                positions.append((index, 'Buy', signals.loc[index, self.ticker], position, cash))
            elif signal['positions'] == -1 and last_signal != -1:  # Sell signal
                cash = position * signals.loc[index, self.ticker]
                position = 0
                last_signal = -1
                positions.append((index, 'Sell', signals.loc[index, self.ticker], position, cash))

        # Calculate final value
        final_value = cash + position * signals.iloc[-1][self.ticker]

        # Calculate return
        returns = (final_value - initial_cash) / initial_cash * 100

        # Create a dictionary to store backtest results
        backtest_results = {
            'Initial Cash': initial_cash,
            'Final Value': final_value,
            'Returns (%)': returns,
            'Positions': positions
        }

        return backtest_results




if __name__ == "__main__":
    instance = sentinel(start_date="2023-06-01",end_date="2024-01-01",
                        ticker="TSLA")
    f4 = instance.sentinel_features_data()
    k = instance.sentinel_data()
    f = instance.generate_signals()

    # 3. Plot signals on the price chart
    instance.plot_signals()
    f1=instance.backtest()



