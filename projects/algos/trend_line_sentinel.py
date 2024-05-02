"""
The term "Sentinel" generally refers to a guard or watchman,
someone or something that stands watch or keeps vigil.
In the context of the algorithm name "TrendLine Sentinel,"
it implies that the algorithm acts as a vigilant observer or guardian of trends,
making decisions based on the information derived from linear regression lines
to protect or optimize the trading strategy.
"""
# pylint: disable=wrong-import-position.
# pylint: disable=wrong-import-order.
# pylint: disable=broad-exception-caught.
# pylint: disable=too-many-locals.
from pathlib import Path
import sys
sys.path.append("..")

from data.finance_database import Database
from algo_scrapers.s_and_p_scraper import SAndPScraper

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

class Sentinel:
    """
    Main class for the sentinel trading algorithm.
    """
    def __init__(self,start_date=None,
                 end_date=None,ticker=None,
                 tickers_list=None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.tickers_list = tickers_list

    def sentinel_data(self):
        """
        Method for pulling data from the finance database.

        Returns:
        pandas.DataFrame: A DataFrame containing
            the historical stock price data.
            The DataFrame has the date as the index and
            'Adj Close' prices for the
            specified ticker as the only column.
        """
        # Construct path to database:
        desktop_path = Path.home() / "Desktop"
        database_folder_path = desktop_path / "Database"
        db_path = database_folder_path / "SandP.db"

        data_instance = Database(ticker=self.ticker,start=self.start_date,end=self.end_date)

        data = data_instance.retrieve_data_from_database(
            start_date=self.start_date,
            end_date=self.end_date,
            ticker=self.ticker,
            database_path=db_path)[['Date','Adj Close']]
        data.set_index('Date',inplace=True)
        data.columns = [self.ticker]

        return data

    def sentinel_features_data(self):
        """
        This method constructs the features data for the trading model/algorithm.

        Returns:
        pandas.DataFrame: A DataFrame containing the feature
            data for the trading model.
            Each column represents a different stock,
            and rows correspond to dates.
            The DataFrame contains historical 'Adj Close'
            prices for the stocks in the
            feature set obtained from the tickers_list.
        """

        scraper = SAndPScraper()
        feature_set = scraper.run_scraper()

        # Construct path to database:
        desktop_path = Path.home() / "Desktop"
        database_folder_path = desktop_path / "Database"
        db_path = database_folder_path / "SandP.db"

        data_final = pd.DataFrame()
        for ticker in feature_set:
            try:
                data_instance = Database(ticker=ticker, start=self.start_date, end=self.end_date)
                data = data_instance.retrieve_data_from_database(start_date=self.start_date,
                                                                 end_date=self.end_date,
                                                                 ticker = ticker,
                                                                 database_path=db_path)
                data = data[['Date', 'Adj Close']]
                data.set_index('Date', inplace=True)
                data = data.rename(columns={'Adj Close':ticker})
                data = data[~data.index.duplicated()]  # Remove duplicate indices
                data_final = pd.concat([data_final, data], axis=1)
            except Exception as error:
                print(f"Error occurred for ticker {ticker}: {error}")
                continue

        # Drop the column corresponding to self.ticker if it exists
        if self.ticker in data_final.columns:
            data_final.drop(columns=self.ticker, inplace=True)

        return data_final
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
        - Buy Order: Generated when transitioning from a sell signal
            to a buy signal, indicating a long position.
        - Sell Order: Generated when transitioning from a
            buy signal to a sell signal, indicating a short position.

        Returns:
        DataFrame: A DataFrame containing the trading signals and corresponding positions.
        The 'signal' column indicates the trading signal
            (+1 for buy, -1 for sell), and the 'positions' column
        specifies the position to take (1 for long, -1 for short).
        """

        data = self.sentinel_data()
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        y_input = data.values.reshape(-1, 1)

        data2 = self.sentinel_features_data()

        # Calculate correlation matrix:
        x_df = pd.DataFrame(data2)
        y_df = pd.DataFrame(y_input)

        # Convert DataFrames to NumPy arrays
        y_array = y_df.to_numpy().flatten()

        # Create a MinMaxScaler object
        scaler = MinMaxScaler()

        # Normalize the variables in x_df
        x_normalized = scaler.fit_transform(x_df)

        # Convert the normalized array back to a DataFrame
        x_normalized_df = pd.DataFrame(x_normalized, columns=x_df.columns)

        # Compute the correlation between the normalized variables and y_df
        correlation_matrix_normalized = np.corrcoef(x_normalized_df.T, y_array)
        correlation_series_normalized = pd.Series(
            correlation_matrix_normalized[:-1, -1],
            index=x_normalized_df.columns
        )

        # Sort the correlation series
        sorted_correlation_series_normalized =\
            correlation_series_normalized.sort_values(
                ascending=False
            )
        sorted_correlation_series_normalized = (
            sorted_correlation_series_normalized.dropna()
        )

        # Extract the 20 most relevant variables:
        combined_df = pd.concat([
            x_df.loc[:, sorted_correlation_series_normalized.tail(10).index],
            x_df.loc[:, sorted_correlation_series_normalized.head(10).index]
        ], axis=1)

        x_input = combined_df

        # Split the data into training and test sets
        (x_train,
         x_test,
         y_train,
         y_test) = train_test_split(x_input,
                                            y_input,
                                            test_size=0.2,
                                            random_state=42)

        # Create a pipeline for neural network regression
        nn_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values by mean.
            ('scaler', StandardScaler()),
            ('mlp', MLPRegressor())
        ])

        # Define hyperparameters grid for GridSearchCV
        param_grid = {
            'mlp__hidden_layer_sizes': [(500,),
                                        (50,50,50,50,50),
                                        (1000,),
                                        (300, 300),
                                        (500, 500),
                                        (200, 200,200)],  # Adjust number of hidden layers and units
            'mlp__activation': ['relu', 'tanh'],  # Activation function options
            'mlp__alpha': [0.0001, 0.01, 0.1],  # Regularization parameter
        }

        # Perform grid search with cross-validation
        grid_search = GridSearchCV(nn_pipeline, param_grid, cv=5, scoring='neg_mean_squared_error')
        grid_search.fit(x_train, y_train)

        # Get the best model from grid search
        best_model = grid_search.best_estimator_

        # Make predictions on the test set
        y_pred = best_model.predict(x_test)

        # Compute RMSE
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Set threshold
        threshold = 30  # Define threshold value

        # Use the forecast if RMSE is below the threshold
        if rmse <= threshold:
            print("Forecast RMSE is below the threshold. Using the forecast.")

            # Iterate over the data and generate signals
            for index_label, row in data.iterrows():
                # Use the best model for 1-step ahead prediction
                forecast = best_model.predict(x_input.loc[index_label].values.reshape(1, -1))

                # Determine the direction of the forecasted market movement
                if forecast > row[self.ticker]:  # If forecast is greater than the observed value
                    signals.loc[index_label, 'signal'] = 1.0  # Go long
                else:
                    signals.loc[index_label, 'signal'] = -1.0  # Go short

            # Generate trading orders
            signals['positions'] = signals['signal'].diff().fillna(0)

        else:
            print("Forecast RMSE is above the threshold. Discarding the forecast.")

        return signals

if __name__ == "__main__":
    instance = Sentinel(start_date="2022-01-01",
                        end_date="2023-01-01",
                        ticker='TSLA')
    k1 = instance.sentinel_data()
    k = instance.generate_signals()
    print("k")