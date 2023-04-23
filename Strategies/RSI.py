"""
Main script for RSI-based trading strategy. The script will be class based
so that it can contain backtest and other features.
"""
from Data.FinanceDatabase import Database
import pandas as pd
import yfinance as yf

class RSIStrategy():
    
    def __init__(self,ticker: str,start_date,end_date):
        
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        
    def get_data(self) -> pd.DataFrame:
        """
        Downloads price data for a specified ticker and date range from a database and calculates the 14-day
        Relative Strength Index (RSI) for each day.

        Returns:
        -------
        data: pd.DataFrame
            A DataFrame containing the RSI values for each day.
        """
        
        data = Database.get_price_data(self,start = self.start_date,
                                 end = self.end_date,
                                 ticker = self.ticker)
        delta = data['Adj Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        data['RSI'] = 100 - (100 / (1 + rs))
        return data.dropna()
        
    def backtest(self):
        data = self.get_data()
        buy_signals = []
        sell_signals = []
        position = 0
        for i in range(1, len(data)):
            # Buy signal: RSI crosses below 30
            if data['RSI'][i-1] < 30 and data['RSI'][i] >= 30 and position == 0:
                buy_signals.append(data.index[i])
                position = 1
            # Sell signal: RSI crosses above 70
            elif data['RSI'][i-1] > 70 and data['RSI'][i] <= 70 and position == 1:
                sell_signals.append(data.index[i])
                position = 0
        # Calculate returns
        returns = None
        for i in range(len(buy_signals)):
            buy_price = data['Adj Close'][buy_signals[i]]
            sell_price = data['Adj Close'][sell_signals[i]]
            if buy_price > 0:
                if returns is None:
                    returns = (sell_price - buy_price) / buy_price
                else:
                    returns += (sell_price - buy_price) / buy_price
        if returns is None:
            returns = 0
        return returns

if __name__ == "__main__":

    # Example usage
    strategy = RSIStrategy('TSLA', '2010-01-01', '2022-04-21')
    data1 = strategy.get_data()
    returns = strategy.backtest()
    print(f'Returns: {returns:.2%}')

            
            

