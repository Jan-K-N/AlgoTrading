"""
Main Finance Database script.
"""
from datetime import date, timedelta
import yfinance as yf
import pandas as pd
import sqlite3
import sys
sys.path.insert(0,'..')
from algo_scrapers.s_and_p_scraper import SAndPScraper
from datetime import datetime
class Database():
    """
    This is the main class for the AlgoTrading database. The database consists of various
    functions, which download different types of data.
    """
    def __init__(self, start=None, end=None, ticker=None,scraper=None):
        if end is None:
            end = date.today().strftime("%Y-%m-%d")
        if start is None:
            start = (date.today() - timedelta(days=3*365)).strftime("%Y-%m-%d")
        self.start = start
        self.end = end
        self.ticker = ticker
        self.conn = None
        self.cursor = None
        self.scraper = scraper

    def connect_to_database(self,db_path):
        """
        Establishes connection to the SQLite database.

        Args:
            db_path (str): The path to the SQLite database file.

        Returns:
            None
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        """
        Closes the connection to the SQLite database.

        Returns:
            None
        """
        if self.conn:
            self.conn.close()

    def insert_price_data_to_sqlite(self, db_path):
        """
        Fetches price data for all tickers for a given date and inserts it into a SQLite database table.

        Args:
            db_path (str): The path to the SQLite database file.
            table_name (str): The name of the table in the database.
            date (str): The date for which data needs to be inserted in the format 'YYYY-MM-DD'.

        Returns:
            None
        """

        # Get list of tickers
        instance  = self.scraper
        tickers_list = instance.run_scraper()

        # Establish connection to the SQLite database
        self.connect_to_database(db_path)

        # Iterate over each ticker and fetch data for the given date
        for ticker in tickers_list:
            price_data = self.get_price_data(start=self.start, end=self.end, ticker=ticker)

            # Insert data into the SQLite database table
            if not price_data.empty:
                price_data.to_sql(ticker, self.conn, if_exists='append', index_label='Date')

        # Commit changes and close connection
        self.conn.commit()
        self.close_connection()

    def get_price_data(self, start=None, end=None, ticker=None):
        """Fetches the historical price data of a stock.

        Args:
            start (str): A string representing the start date in the format 'YYYY-MM-DD'.
            end (str): A string representing the end date in the format 'YYYY-MM-DD'.
            ticker (str): A string representing the stock ticker symbol.

        Returns:
            pandas.DataFrame: A DataFrame containing the historical price data of the
            specified stock.

        Note:
            If `ticker`, `start`, and `end` are not specified, the function will use the
            previously set values.

        Raises:
            ValueError: If `ticker` is not specified.
        """
        if ticker is not None:
            self.ticker = ticker
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        try:
            ticker_data = yf.download(tickers=self.ticker,
                                      start=self.start,
                                      end=self.end, threads=True)
        except KeyError:
            print(f"KeyError: Ticker {self.ticker} not found or data not available. Skipping...")
            return None

        return ticker_data

    def get_dividend_data(self, start:str=None, end:str=None, ticker:str=None):
        """Fetches dividend data for a given stock ticker between specified start and end dates.

            Args:
                start (str): Optional. Start date in 'YYYY-MM-DD' format. Defaults to None.
                end (str): Optional. End date in 'YYYY-MM-DD' format. Defaults to None.
                ticker (str): Optional. Stock ticker symbol. Defaults to None.

            Returns:
                pandas.core.series.Series: Dividend data for the specified ticker and date range.

            Raises:
                ValueError: If the ticker symbol is not provided.

            Example:
                To fetch dividend data for AAPL between 2020-01-01 and 2021-12-31:

                >>> db = Database()
                >>> dividends = db.get_dividend_data(start='2020-01-01',
                >>> end='2021-12-31', ticker='AAPL')
            """
        if ticker is not None:
            self.ticker = ticker
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        ticker_info = yf.Ticker(self.ticker)
        ticker_div = ticker_info.dividends
        return ticker_div

    def compute_stock_return(self, start=None, end=None, ticker=None):
        """
        Computes the daily return of a stock based on its price data.

        Args:
            start (str): A string representing the start date in the format 'YYYY-MM-DD'.
            end (str): A string representing the end date in the format 'YYYY-MM-DD'.
            ticker (str): A string representing the stock ticker symbol.

        Returns:
            pandas.Series: The computed daily return of the stock.

        Note:
            If `ticker`, `start`, and `end` are not specified, the function will use the
            previously set values.

        Raises:
            ValueError: If `ticker` is not specified.
        """
        price_data = self.get_price_data(start=start, end=end, ticker=ticker)
        if price_data.empty:
            raise ValueError("Price data is empty.")

        # Compute the daily returns
        daily_returns = pd.DataFrame()
        daily_returns[ticker] = price_data['Close'].pct_change()

        # Drop 'NaN' values
        daily_returns = daily_returns.dropna()
        return daily_returns

    def retrieve_data_from_database(self, start_date, end_date, ticker_symbol, db_path):
        """
        Retrieves data from the database for a given time period and ticker symbol.

        Args:
            start_date (str): The start date in the format 'YYYY-MM-DD'.
            end_date (str): The end date in the format 'YYYY-MM-DD'.
            ticker_symbol (str): The ticker symbol indicating the table name in the database.
            db_path (str): The path to the SQLite database file.

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved data.
        """
        # Establish connection to the SQLite database
        self.connect_to_database(db_path)

        # Construct query to retrieve data from the specified table for the given time period
        query = f"SELECT * FROM {ticker_symbol} WHERE Date BETWEEN '{start_date}' AND '{end_date}'"

        # Execute query and fetch data
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        # Convert fetched data into DataFrame
        columns = [description[0] for description in self.cursor.description]
        df = pd.DataFrame(data, columns=columns)

        # Close connection to the database
        self.close_connection()

        return df

if __name__ == "__main__":
    tickers_list = ['TSLA','AAPL']

    data_frames = []
    for ticker in tickers_list:
        instance_database = Database()
        data = instance_database.retrieve_data_from_database(start_date="2020-04-01", end_date="2021-10-01",
                                                             ticker_symbol=ticker,
                                                             db_path="/Users/jankindtnielsen/Documents/SandP.db")
        data_frames.append(data)

print("k")