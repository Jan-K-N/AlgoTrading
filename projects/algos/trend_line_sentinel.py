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
from sklearn.linear_model import LinearRegression
from data.finance_database import Database

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

        x = np.arange(len(data)).reshape(-1,1)
        y = data.values.reshape(-1,1)
        model = LinearRegression()
        model.fit(x,y)
        signals['regression_line'] = model.predict(x)

        data, signals['regression_line'] = data.align(signals['regression_line'], join='inner', axis=0)

        # Create signals
        signals['signal'] = np.where(data.values.flatten() > signals['regression_line'].values.flatten(), 1.0, -1.0)

        # Generate trading orders
        signals['positions'] = signals['signal'].diff()



        return signals

    def plot_signals(self, data):
        fig, ax = plt.subplots(figsize=(12, 8))

        # Plotting historical price data
        ax.plot(data.index, data[self.ticker], label='Price', linewidth=2)

        signals = self.generate_signals()

        # Plotting linear regression line
        ax.plot(data.index, signals['regression_line'], label='Linear Regression Line', linestyle='--', color='orange')

        # Plotting buy signals
        ax.plot(signals[signals['positions'] == 1.0].index,
                signals['regression_line'][signals['positions'] == 1.0],
                '^', markersize=10, color='g', label='Buy Signal')

        # Plotting sell signals
        ax.plot(signals[signals['positions'] == -1.0].index,
                signals['regression_line'][signals['positions'] == -1.0],
                'v', markersize=10, color='r', label='Sell Signal')

        ax.set_title('Linear Regression Trading Strategy')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()

        plt.show()




if __name__ == "__main__":
    instance = sentinel(start_date="2022-01-01",end_date="2023-01-01",
                        ticker="TSLA")
    k = instance.sentinel_data()
    f = instance.generate_signals()

    # 3. Plot signals on the price chart
    instance.plot_signals(k)



