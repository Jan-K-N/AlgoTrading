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

# class ArbitrageTrading:
#     def __init__(self, start_date = None, end_date = None, market = None):
#         self.start_date = start_date
#         self.end_date = end_date
#         self.market = market
#         self.data = self.get_data()
#
#     def get_data(self):
#         if self.market == 'DAX':
#             instance_dax = DAXScraper()
#             tickers_list = instance_dax.run_scraper()
#         elif self.market == '^GSPC':
#             instance_sp500 = SAndPScraper()
#             tickers_list = instance_sp500.run_scraper()
#
#         returns_dataframe = pd.DataFrame()  # Initialize an empty dataframe
#
#         for ticker in tickers_list:
#             data_instance = Database()
#             returns = data_instance.compute_stock_return(start=self.start_date, end=self.end_date,ticker=ticker)
#             returns_dataframe = pd.concat([returns_dataframe, returns], axis=1)
#
#         return returns_dataframe
#
#     def find_cointegrated_pairs(self):
#         num_assets = len(self.data.columns)
#         score_matrix = np.zeros((num_assets, num_assets))
#         pvalue_matrix = np.ones((num_assets, num_assets))
#         pairs = []
#
#         for i in range(num_assets):
#             for j in range(i + 1, num_assets):
#                 asset1 = self.data.iloc[:, i]
#                 asset2 = self.data.iloc[:, j]
#
#                 # Handle missing or invalid values
#                 if asset1.isnull().any() or asset2.isnull().any():
#                     print("Missing or invalid values in the data. Skipping pair...")
#                     continue
#
#                 if not np.isfinite(asset1).all() or not np.isfinite(asset2).all():
#                     print("Invalid values (e.g., NaN or infinity) in the data. Skipping pair...")
#                     continue
#
#                 # Perform cointegration test
#                 result = sm.tsa.stattools.coint(asset1, asset2)
#                 score = result[0]
#                 pvalue = result[1]
#
#                 score_matrix[i, j] = score
#                 pvalue_matrix[i, j] = pvalue
#
#                 if pvalue < 0.05:
#                     pairs.append((i, j))
#
#         return pairs, score_matrix, pvalue_matrix
#
#     def arbitrage_strategy(self):
#         pairs, _, _ = self.find_cointegrated_pairs()
#
#         arbitrage_opportunities = []
#
#         for pair in pairs:
#             asset1_idx = pair[0]
#             asset2_idx = pair[1]
#             asset1 = self.data.iloc[:, asset1_idx]
#             asset2 = self.data.iloc[:, asset2_idx]
#
#             # Perform linear regression to find hedge ratio
#             model = sm.OLS(asset1, asset2)
#             model_fit = model.fit()
#             hedge_ratio = model_fit.params[0]
#
#             # Compute spread between asset1 and asset2
#             spread = asset1 - hedge_ratio * asset2
#
#             # Compute mean and standard deviation of spread
#             spread_mean = np.mean(spread)
#             spread_std = np.std(spread)
#
#             # Create dataframe for the arbitrage opportunity
#             df = pd.DataFrame(index=self.data.index)
#             df[asset1.name] = [
#                 1 if x > spread_mean + 1.5 * spread_std else -1 if x < spread_mean - 1.5 * spread_std else 0 for x in
#                 spread]
#             df[asset2.name] = [
#                 1 if x > spread_mean + 1.5 * spread_std else -1 if x < spread_mean - 1.5 * spread_std else 0
#                 for x in spread]
#
#             arbitrage_opportunities.append({
#                 'Pair': (asset1.name, asset2.name),
#                 'DataFrame': df
#             })
#
#         return arbitrage_opportunities
class ArbitrageTrading:
    def __init__(self, start_date=None, end_date=None, market=None):
        self.start_date = start_date
        self.end_date = end_date
        self.market = market
        self.data = self.get_data()

    def get_data(self):
        if self.market == 'DAX':
            instance_dax = DAXScraper()
            tickers_list = instance_dax.run_scraper()
        elif self.market == '^GSPC':
            instance_sp500 = SAndPScraper()
            tickers_list = instance_sp500.run_scraper()

        returns_dataframe = pd.DataFrame()  # Initialize an empty dataframe

        for ticker in tickers_list:
            data_instance = Database()
            returns = data_instance.compute_stock_return(start=self.start_date, end=self.end_date, ticker=ticker)
            returns_dataframe = pd.concat([returns_dataframe, returns], axis=1)

        return returns_dataframe

    def find_cointegrated_pairs(self):
        num_assets = len(self.data.columns)
        score_matrix = np.zeros((num_assets, num_assets))
        pvalue_matrix = np.ones((num_assets, num_assets))
        pairs = []

        for i in range(num_assets):
            for j in range(i + 1, num_assets):
                asset1 = self.data.iloc[:, i]
                asset2 = self.data.iloc[:, j]

                # Handle missing or invalid values
                if asset1.isnull().any() or asset2.isnull().any():
                    print("Missing or invalid values in the data. Skipping pair...")
                    continue

                if not np.isfinite(asset1).all() or not np.isfinite(asset2).all():
                    print("Invalid values (e.g., NaN or infinity) in the data. Skipping pair...")
                    continue

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

        arbitrage_opportunities = []

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

            # Create DataFrame for the arbitrage opportunity
            df = pd.DataFrame(index=self.data.index)
            asset1_name = asset1.name
            asset2_name = asset2.name
            df[asset1_name] = np.where(spread > spread_mean + 1.5 * spread_std, 1,
                                       np.where(spread < spread_mean - 1.5 * spread_std, -1, 0))
            df[asset2_name] = np.where(spread > spread_mean + 1.5 * spread_std, -1,
                                       np.where(spread < spread_mean - 1.5 * spread_std, 1, 0))

            arbitrage_opportunities.append({
                'Pair': (asset1_name, asset2_name),
                'DataFrame': df
            })

        arbitrage_opportunities = [opportunity for opportunity in arbitrage_opportunities if
                                   opportunity['DataFrame'][
                                       [opportunity['Pair'][0], opportunity['Pair'][1]]].nunique().sum() > 2]

        return arbitrage_opportunities


if __name__ == '__main__':
    instance = ArbitrageTrading(start_date='2022-05-01', end_date = '2023-04-01',market = 'DAX')
    k = instance.get_data()
    f=instance.arbitrage_strategy()
    print("k")

