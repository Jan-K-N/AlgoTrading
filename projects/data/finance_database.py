"""
Main Finance Database script. The script will create a
database folder on the users desktop in which the data
files are stored.
"""
# pylint: disable=wrong-import-position.
# pylint: disable=wrong-import-order.
# pylint: disable=ungrouped-imports.
from datetime import date, timedelta, datetime
import sqlite3
import sys
from pathlib import Path

import pandas.errors

sys.path.insert(0,'..')
from algo_scrapers.s_and_p_scraper import SAndPScraper
import os
import schedule
import time
from typing import Optional, Union
import yfinance as yf
import pandas as pd

class Database():
    """
    This is the main class for the AlgoTrading database. The database consists of various
    functions, which download different types of data.
    """

    def __init__(self, start: Optional[str] = None, end: Optional[str] = None,
                 ticker: Optional[str] = None,
                 scraper: Optional[SAndPScraper] = None):
        """
        Initialize the Database object.

        Args:
            start (str, optional): The start date in the format 'YYYY-MM-DD'. Defaults to None.
            end (str, optional): The end date in the format 'YYYY-MM-DD'. Defaults to None.
            ticker (str, optional): The stock ticker symbol. Defaults to None.
            scraper (SAndPScraper, optional): Instance of the SAndPScraper class. Defaults to None.
        """
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

    def connect_to_database(self, database_path: str):
        """
        Establish connection to the SQLite database.

        Args:
            database_path (str): The path to the SQLite database file.
        """
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        """
        Closes the connection to the SQLite database.

        Returns:
            None
        """
        if self.conn:
            self.conn.close()

    def insert_price_data_to_sqlite(self, database_path: str):
        """
        Fetches price data for all tickers for a given date and
            inserts it into a SQLite database table.

        Args:
            database_path (str): The path to the SQLite database file.
        """

        # Get list of tickers
        instance  = self.scraper
        tickers_list = instance.run_scraper()

        # Establish connection to the SQLite database
        self.connect_to_database(database_path)

        # Iterate over each ticker and fetch data for the given date
        for ticker in tickers_list:
            price_data = self.get_price_data(start=self.start, end=self.end, ticker=ticker)

            # Insert data into the SQLite database table
            if not price_data.empty:
                price_data.to_sql(ticker, self.conn, if_exists='append', index_label='Date')

        # Commit changes and close connection
        self.conn.commit()
        self.close_connection()

    def get_price_data(self, start: Optional[str] = None, end: Optional[str] = None,
                       ticker: Optional[str] = None) -> Union[pd.DataFrame, None]:
        """
        Fetches the historical price data of a stock.

        Args:
            start (str, optional): A string representing the start date in the format
                'YYYY-MM-DD'. Defaults to None.
            end (str, optional): A string representing the end date in
                the format 'YYYY-MM-DD'. Defaults to None.
            ticker (str, optional): A string representing the
                stock ticker symbol. Defaults to None.

        Returns:
            pandas.DataFrame: A DataFrame containing the
                historical price data of the specified stock.

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

    def get_dividend_data(self, start: Optional[str] = None, end: Optional[str] = None,
                          ticker: Optional[str] = None) -> pd.Series:
        """
        Fetches dividend data for a given stock ticker between specified start and end dates.

        Args:
            start (str, optional): Start date in 'YYYY-MM-DD' format. Defaults to None.
            end (str, optional): End date in 'YYYY-MM-DD' format. Defaults to None.
            ticker (str, optional): Stock ticker symbol. Defaults to None.

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

    def compute_stock_return(self, start: Optional[str] = None, end: Optional[str] = None,
                             ticker: Optional[str] = None) -> pd.Series:
        """
        Computes the daily return of a stock based on its price data.

        Args:
            start (str, optional): A string representing the
                start date in the format 'YYYY-MM-DD'. Defaults to None.
            end (str, optional): A string representing the
                end date in the format 'YYYY-MM-DD'. Defaults to None.
            ticker (str, optional): A string representing the
                stock ticker symbol. Defaults to None.

        Returns:
            pandas.Series: The computed daily return of the stock.

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

    def retrieve_data_from_database(self, start_date: str,
                                    end_date: str,
                                    ticker: str,
                                    database_path: str) -> pd.DataFrame:
        """
        Retrieves data from the database for a given time period and ticker symbol.

        Args:
            start_date (str): The start date in the format 'YYYY-MM-DD'.
            end_date (str): The end date in the format 'YYYY-MM-DD'.
            ticker (str): The ticker symbol indicating the table name in the database.
            database_path (str): The path to the SQLite database file.

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved data.
        """
        # Establish connection to the SQLite database
        try:
            self.connect_to_database(database_path)

            # Construct query to retrieve data from the specified table for the given time period
            query = (f"SELECT * FROM {ticker}"
                     f" WHERE Date BETWEEN '{start_date}' AND '{end_date}'")

            # Execute query and fetch data
            self.cursor.execute(query)
            data = self.cursor.fetchall()

            # Convert fetched data into DataFrame
            columns = [description[0] for description in self.cursor.description]
            retrived_dataframe = pd.DataFrame(data, columns=columns)
            retrived_dataframe = retrived_dataframe.drop_duplicates()

            # Close connection to the database
            self.close_connection()

            return retrived_dataframe
        except sqlite3.Error as error:
            print(f"SQLite error : {error}")
            return pd.DataFrame()
        except pandas.errors.EmptyDataError:
            print(f"No data available for ticker symbol {ticker}")
            return pd.DataFrame()

class DatabaseScheduler:
    """
    This is the class to run the Database on a schedule.
    """
    def __init__(self, instance_database: Database, database_path: str):
        """
        Initialize the DatabaseScheduler object.

        Args:
            instance_database (Database): An instance of the Database class.
            database_path (str): The path to the SQLite database file.
        """
        self.instance_database = instance_database
        self.database_path = database_path

    def run_insert_price_data(self):
        """Method to run and insert the data to the database."""
        print("Inserting price data to database...")
        self.instance_database.insert_price_data_to_sqlite(database_path=self.database_path)
        print("Price data insertion complete.")

    def schedule_insert_price_data(self, interval_hours: float):
        """
        Method to do the actual scheduling.

        Args:
            interval_hours (float): The number of hours between each run.
        """
        schedule.every(interval_hours).hours.do(self.run_insert_price_data)

        while True:
            schedule.run_pending()
            time.sleep(60)  # Sleep for 1 second to avoid high CPU usage

        while True:
            schedule.run_pending()
            time.sleep(60)  # Sleep for 60 seconds to avoid high CPU usage

if __name__ == "__main__":
    tickers_list0 = SAndPScraper()

    instance_database0 = Database(start="2019-01-01",
                                 end=datetime.today().strftime("%Y-%m-%d"),
                                 scraper=tickers_list0)



    # Create the 'Database' folder on the user's desktop if it doesn't exist
    desktop_path = Path.home() / "Desktop"
    database_folder_path = desktop_path / "Database"
    if not database_folder_path.exists():
        os.makedirs(database_folder_path)

    db_path = database_folder_path / "SandP.db"
    #
    # k = instance_database0.retrieve_data_from_database(start_date="2019-01-01",
    #                                                    end_date="2021-01-01",
    #                                                    ticker="TSLA",
    #                                                    database_path=db_path)

    db_scheduler = DatabaseScheduler(instance_database0, database_path=db_path)

    # Schedule the insertion of price data every minute
    db_scheduler.schedule_insert_price_data(interval_hours=0.01)
