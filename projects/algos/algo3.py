"""Main script for algo3"""

import pandas as pd
import numpy as np
import sys
import statsmodels.api as sm

sys.path.insert(0, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algo_scrapers')
sys.path.insert(1, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
from s_and_p_scraper import SAndPScraper
from dax_scraper import DAXScraper
from finance_database import Database

class ArbitrageTrading:
    def __init__(self, start_date = None, end_date = None, market = None):
        self.start_date = start_date
        self.end_date = end_date
        self.market = market

    def get_data(self):
        if self.market == 'DAX':
            instance_dax = DAXScraper()
            tickers_list = instance_dax.run_scraper()
        elif market == '^GSPC':
            instance_sp500 = SAndPScraper()
            tickers_list = instance_sp500.run_scraper()

        returns_dataframe = pd.DataFrame()  # Initialize an empty dataframe

        for ticker in tickers_list:
            data_instance = Database()
            returns = data_instance.compute_stock_return(start=self.start_date, end=self.end_date,ticker=ticker)
            returns_dataframe = pd.concat([returns_dataframe, returns])

        return returns_dataframe

    def find_cointegrated_pairs(self):
        num_assets = len(self.data.columns)
        score_matrix = np.zeros((num_assets, num_assets))
        pvalue_matrix = np.ones((num_assets, num_assets))
        pairs = []

        for i in range(num_assets):
            for j in range(i+1, num_assets):
                asset1 = self.data.iloc[:, i]
                asset2 = self.data.iloc[:, j]

                # Perform cointegration test
                result = sm.tsa.stattools.coint(asset1, asset2)
                score = result[0]
                pvalue = result[1]

                score_matrix[i, j] = score
                pvalue_matrix[i, j] = pvalue

                if pvalue < 0.05:
                    pairs.append((i, j))

        return pairs, score_matrix, pvalue_matrix

    def arbitrage_strategy(self):
        pairs, _, _ = self.find_cointegrated_pairs()

        for pair in pairs:
            asset1_idx = pair[0]
            asset2_idx = pair[1]
            asset1 = self.data.iloc[:, asset1_idx]
            asset2 = self.data.iloc[:, asset2_idx]

            # Perform linear regression to find hedge ratio
            model = sm.OLS(asset1, asset2)
            model_fit = model.fit()
            hedge_ratio = model_fit.params[0]

            # Compute spread between asset1 and asset2
            spread = asset1 - hedge_ratio * asset2

            # Compute mean and standard deviation of spread
            spread_mean = np.mean(spread)
            spread_std = np.std(spread)

            # Define trading thresholds
            upper_threshold = spread_mean + 1.5 * spread_std
            lower_threshold = spread_mean - 1.5 * spread_std

            # Implement arbitrage trading strategy
            if spread[-1] > upper_threshold:
                # Sell asset1 and buy asset2
                print(f"Sell asset1 and buy asset2 (Pair: {asset1.name}, {asset2.name})")
            elif spread[-1] < lower_threshold:
                # Buy asset1 and sell asset2
                print(f"Buy asset1 and sell asset2 (Pair: {asset1.name}, {asset2.name})")
            else:
                # No arbitrage opportunity
                print("No arbitrage opportunity")

# # Example usage:
# # Assuming 'data' is a pandas DataFrame containing the return data of multiple assets
# # Each column represents the return time series of an asset
# arbitrage_trading = ArbitrageTrading(data)
#
# # Perform cointegration analysis and identify arbitrage opportunities
# arbitrage_trading.arbitrage_strategy()

if __name__ == '__main__':
    instance = ArbitrageTrading(start_date='2021-01-01', end_date = '2021-04-01',market = 'DAX')
    k = instance.get_data()

