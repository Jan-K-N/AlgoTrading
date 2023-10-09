"""
Main script for random forrest. The model can be used to predict,
stock returns.
"""
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import numpy as np
import pandas as pd

class RandomForrest:
    def __init__(self,series=None,x_data=None):
        """
        series: The target series we want to predict.
        x_data: predictors.
        """
        self.series = series
        self.x_data=x_data

    def predictor(self, out_of_sample=True):
        evaluation_list = []

        common_regr_params = {
            'random_state': 42,
        }

        series_final = self.series.reshape(-1, 1)
        X_train, X_test, y_train, y_test = train_test_split(series_final, self.x_data, test_size=0.25, random_state=42)

        # Model training:
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [None, 10],
        }
        grid_search = GridSearchCV(estimator=RandomForestRegressor(**common_regr_params),
                                   param_grid=param_grid, cv=5)
        # Fit the model:
        grid_search.fit(X_train, y_train)

        # Access the best hyperparameters
        best_params = grid_search.best_params_

        # Create a new model with the best hyperparameters
        best_regr = RandomForestRegressor(
            n_estimators=best_params['n_estimators'],
            max_depth=best_params['max_depth'],
            **common_regr_params  # Include any other relevant hyperparameters
        )

        # Retrain the model with the best hyperparameters
        best_regr.fit(X_train, y_train)

        # Evaluate the best model on the test set
        y_test_pred = best_regr.predict(X_test)

        # Calculate evaluation metrics:
        mae = mean_absolute_error(y_test, y_test_pred)
        mse = mean_squared_error(y_test, y_test_pred)
        rmse = np.sqrt(mse)

        # Append the evaluation metrics to the list
        evaluation_list.append({'MAE': mae, 'MSE': mse, 'RMSE': rmse})

        # Choose the best model based on the lowest RMSE
        best_model_index = np.argmin([result['RMSE'] for result in evaluation_list])
        best_model = best_regr if best_model_index == 0 else None  # In this case, we have only one model

        # Use the best model for out-of-sample forecasting
        if out_of_sample:
            # Ensure that the format of series_final[-1] matches the input features used during training
            y_out_of_sample_pred = best_model.predict(series_final[-1].reshape(1, -1))
        return evaluation_list, best_model, y_out_of_sample_pred

if __name__ == "__main__":
    # Set a random seed for reproducibility
    np.random.seed(42)

    # Generate a random returns series
    num_days = 100
    returns = np.random.normal(loc=0.0005, scale=0.01, size=num_days)
    instance = RandomForrest(series=returns[:-1],x_data=returns[1:])
    k = instance.predictor()
    print("k")