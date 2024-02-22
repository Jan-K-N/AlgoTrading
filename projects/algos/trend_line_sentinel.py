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
from pathlib import Path
import matplotlib.pyplot as plt
import sys
sys.path.append("..")

from data.finance_database import Database

from algo_scrapers.s_and_p_scraper import SAndPScraper


from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from statsmodels.tsa.seasonal import seasonal_decompose


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
        # Construct path to database:
        desktop_path = Path.home() / "Desktop"
        database_folder_path = desktop_path / "Database"
        db_path = database_folder_path / "SandP.db"

        data_instance = Database(ticker=self.ticker,start=self.start_date,end=self.end_date)

        data = data_instance.retrieve_data_from_database(start_date=self.start_date,
                                                          end_date=self.end_date,
                                                          ticker=self.ticker,
                                                          database_path=db_path)[['Date','Adj Close']]
        data.set_index('Date',inplace=True)
        data.columns = [self.ticker]

        return data

    def sentinel_features_data(self, y_ticker="TSLA"):
        """

        """

        scraper = SAndPScraper()
        feature_set = scraper.run_scraper()

        sentinel_features = pd.DataFrame()
        for ticker in feature_set:
            sentinel_features[ticker] = self.sentinel_data()

        # Drop the column corresponding to self.ticker if it exists
        if y_ticker in sentinel_features.columns:
            sentinel_features.drop(columns=y_ticker, inplace=True)

        return sentinel_features
    def generate_signals(self):
        """
        Method for generating trading signals using a neural network model.

        Signals are generated based on the forecasted stock prices
        obtained from the neural network model.

        Buy Signal:
        When the forecasted price is above the current/latest price
        of the stock, a buy signal is generated.
        This indicates that the stock may be undervalued or trending upwards.

        Sell Signal:
        When the forecasted price is below the current/latest price of the stock,
        a sell signal is generated.
        This suggests that the stock may be overvalued or trending downwards.

        Trading Orders:
        - Buy Order: Generated when transitioning from a sell signal to a buy signal, indicating a long position.
        - Sell Order: Generated when transitioning from a buy signal to a sell signal, indicating a short position.

        Returns:
        DataFrame: A DataFrame containing the trading signals and corresponding positions.
        The 'signal' column indicates the trading signal (+1 for buy, -1 for sell), and the 'positions' column
        specifies the position to take (1 for long, -1 for short).
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

        # Create a pipeline for neural network regression
        nn_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values by mean.
            ('scaler', StandardScaler()),
            ('mlp', MLPRegressor())
        ])

        # Define hyperparameters grid for GridSearchCV
        param_grid = {
            'mlp__hidden_layer_sizes': [(50,), (100,), (50, 50)],  # Adjust number of hidden layers and units
            'mlp__activation': ['relu', 'tanh'],  # Activation function options
            'mlp__alpha': [0.0001, 0.001, 0.01],  # Regularization parameter
        }

        # Perform grid search with cross-validation
        grid_search = GridSearchCV(nn_pipeline, param_grid, cv=10, scoring='neg_mean_squared_error')
        grid_search.fit(X_train, y_train)

        # Get the best model from grid search
        best_model = grid_search.best_estimator_

        # Make predictions on the test set
        y_pred = best_model.predict(X_test)

        # Compute RMSE
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Set threshold
        threshold = 10  # Define your threshold value

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

        return signals

    def plot_signals(self):
        fig, ax = plt.subplots(figsize=(12, 8))

        data = self.sentinel_data()

        # Plotting historical price data, dropping the first observation
        ax.plot(data.index[1:], data[self.ticker].iloc[1:], label='Price', linewidth=2)

        signals = self.generate_signals()

        # Plotting buy signals
        buy_indices = signals[signals['signal'] == 1.0].index
        buy_values = data[self.ticker][signals['signal'] == 1.0]
        ax.plot(buy_indices, buy_values, '^', markersize=10, color='g', label='Buy Signal')

        # Plotting sell signals
        sell_indices = signals[signals['signal'] == -1.0].index
        sell_values = data[self.ticker][signals['signal'] == -1.0]
        ax.plot(sell_indices, sell_values, 'v', markersize=10, color='r', label='Sell Signal')

        ax.set_title('NN Trading Strategy')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()

        plot = plt.show()

        return plot

if __name__ == "__main__":
    instance = sentinel(start_date="2023-06-01",end_date="2024-01-01",
                        ticker="TSLA")
    f4 = instance.sentinel_features_data()
    k = instance.sentinel_data()
    f = instance.generate_signals()

    # # 3. Plot signals on the price chart
    instance.plot_signals()
    # f1=instance.backtest()
    print("k")



