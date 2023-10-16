"""
Main script for random forrest. The model can be used to predict,
stock returns.
"""
# pylint: disable=import-error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import numpy as np
# pylint: disable=too-many-locals
# pylint: disable=too-few-public-methods
class RandomForrest:
    """
    A class for training a RandomForestRegressor model and making predictions.

    Parameters:
        series (numpy.ndarray): The target series we want to predict.
        x_data (numpy.ndarray): Predictors.

    Attributes:
        series (numpy.ndarray): The target series.
        x_data (numpy.ndarray): Predictors.

    Methods:
        predictor(out_of_sample=True):
            Trains a RandomForestRegressor model, evaluates its performance, and makes predictions.

            Parameters:
                out_of_sample (bool): If True, makes out-of-sample predictions. Default is True.

            Returns:
                tuple: A tuple containing:
                    - evaluation_list (list): A list of dictionaries containing evaluation metrics.
                    - best_model: The trained model with the best hyperparameters.
                    - y_out_of_sample_pred: Predictions for out-of-sample data.
    """
    def __init__(self,series=None,x_data=None):
        """
        Initializes a RandomForrest instance.

        Parameters:
            series (numpy.ndarray): The target series we want to predict.
            x_data (numpy.ndarray): Predictors.
        """
        self.series = series
        self.x_data=x_data
    def predictor(self, out_of_sample=True):
        """
        Trains a RandomForestRegressor model, evaluates its performance, and makes predictions.

        Parameters:
            out_of_sample (bool): If True, makes out-of-sample predictions. Default is True.

        Returns:
            tuple: A tuple containing:
                - evaluation_list (list): A list of dictionaries containing evaluation metrics.
                - best_model: The trained RandomForestRegressor model with the best hyperparameters.
                - y_out_of_sample_pred: Predictions for out-of-sample data.
        """
        evaluation_list = []

        common_regr_params = {
            'random_state': 42,
        }

        series_final = self.series.reshape(-1, 1)
        x_train, x_test, y_train, y_test = train_test_split(series_final,
                                                            self.x_data,
                                                            test_size=0.25,
                                                            random_state=42)

        # Model training:
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [None, 10],
        }
        grid_search = GridSearchCV(estimator=RandomForestRegressor(**common_regr_params),
                                   param_grid=param_grid, cv=5)
        # Fit the model:
        grid_search.fit(x_train, y_train)

        # Access the best hyperparameters
        best_params = grid_search.best_params_

        # Create a new model with the best hyperparameters
        best_regr = RandomForestRegressor(
            n_estimators=best_params['n_estimators'],
            max_depth=best_params['max_depth'],
            **common_regr_params  # Include any other relevant hyperparameters
        )

        # Retrain the model with the best hyperparameters
        best_regr.fit(x_train, y_train)

        # Evaluate the best model on the test set
        y_test_pred = best_regr.predict(x_test)

        # Calculate evaluation metrics:
        mae = mean_absolute_error(y_test, y_test_pred)
        mse = mean_squared_error(y_test, y_test_pred)
        rmse = np.sqrt(mse)

        # Append the evaluation metrics to the list
        evaluation_list.append({'MAE': mae, 'MSE': mse, 'RMSE': rmse})

        # Choose the best model based on the lowest RMSE
        best_model_index = np.argmin([result['RMSE'] for result in evaluation_list])
        best_model = best_regr if best_model_index == 0 else None

        # Use the best model for out-of-sample forecasting
        if out_of_sample:
            y_out_of_sample_pred = best_model.predict(series_final[-1].reshape(1, -1))
        return evaluation_list, best_model, y_out_of_sample_pred
