"""The main script for algo3/arbitrage trading"""
# pylint: disable=wrong-import-position
import pandas as pd
import numpy as np
import statsmodels.api as sm
from algo_scrapers.s_and_p_scraper import SAndPScraper
from algo_scrapers.dax_scraper import DAXScraper
from data.finance_database import Database

class ArbitrageTrading:
    """
    Class for performing arbitrage trading strategy.

    Attributes:
        start_date (str): Start date of the data to be used for analysis in 'YYYY-MM-DD' format.
            Default is None.
        end_date (str): End date of the data to be used for analysis in 'YYYY-MM-DD' format.
        Default is None.
        market (str): Market name for which the data is to be scraped
            ('DAX' for DAX index, '^GSPC' for S&P 500). Default is None
        data (pd.DataFrame): DataFrame containing historical price data of selected assets.

    Methods:
        __init__(self, start_date=None, end_date=None, market=None):
            Initializes the ArbitrageTrading object with the specified parameters.

        get_data(self):
            Retrieves historical price data for selected assets based on the specified market.

        find_cointegrated_pairs(self):
            Finds cointegrated pairs among the selected assets using cointegration test.

        arbitrage_strategy(self):
            Implements the arbitrage trading strategy based on cointegrated pairs.

    """
    def __init__(self, start_date=None, end_date=None, market=None):
        """
        Initialize the ArbitrageTrading object.

        Parameters:
            start_date (str): Start date of the data to be used for analysis in 'YYYY-MM-DD' format.
                Default is None.
            end_date (str): End date of the data to be used for analysis in 'YYYY-MM-DD' format.
                Default is None.
            market (str): Market name for which the data is to be scraped
                ('DAX' for DAX index, '^GSPC' for S&P 500). Default is None.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.market = market
        self.data = self.get_data()

    def get_data(self):
        """
        Retrieve historical price data for selected assets based on the specified market.

        Returns:
            pd.DataFrame: DataFrame containing historical price data of selected assets.
        """
        if self.market == 'DAX':
            instance_dax = DAXScraper()
            tickers_list = instance_dax.run_scraper()
        elif self.market == '^GSPC':
            instance_sp500 = SAndPScraper()
            tickers_list = instance_sp500.run_scraper()

        returns_dataframe = pd.DataFrame()  # Initialize an empty dataframe

        for ticker in tickers_list:
            data_instance = Database()
            returns = data_instance.compute_stock_return(start=self.start_date,
                                                         end=self.end_date,
                                                         ticker=ticker)
            returns_dataframe = pd.concat([returns_dataframe, returns], axis=1)

        return returns_dataframe

    def find_cointegrated_pairs(self):
        """
        Find cointegrated pairs among the selected assets using cointegration test.

        Returns:
            tuple: A tuple containing:
                - list: List of tuples representing cointegrated pairs (asset1_idx, asset2_idx).
                - np.ndarray: Matrix containing cointegration test scores.
                - np.ndarray: Matrix containing p-values from cointegration test.
        """
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

    # pylint: disable=too-many-locals
    def arbitrage_strategy(self):
        """
        Implement the arbitrage trading strategy based on cointegrated pairs.

        Returns:
            list: List of dictionaries, each representing an arbitrage opportunity, containing:
                - tuple: Pair of asset names (asset1, asset2).
                - pd.DataFrame: DataFrame containing trading signals for the pair of assets.
        """
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
            data_frame = pd.DataFrame(index=self.data.index)
            asset1_name = asset1.name
            asset2_name = asset2.name
            data_frame[asset1_name] = np.where(spread > spread_mean + 1.5 * spread_std,
                                               1,
                                               np.where(spread < spread_mean -
                                                        1.5 * spread_std, -1, 0))
            data_frame[asset2_name] = np.where(spread > spread_mean + 1.5 * spread_std,
                                               -1,
                                               np.where(spread < spread_mean -
                                                        1.5 * spread_std, 1, 0))

            arbitrage_opportunities.append({
                'Pair': (asset1_name, asset2_name),
                'DataFrame': data_frame
            })

        arbitrage_opportunities = [opportunity for opportunity
                                   in arbitrage_opportunities if
                                   opportunity['DataFrame'][
                                       [opportunity['Pair'][0],
                                        opportunity['Pair'][1]]].nunique().sum() > 2]

        return arbitrage_opportunities
