"""
Main class for downloading data from the FRED-MD database
"""
import pandas as pd
import pandas_datareader as pdr

class FredMdDataDownloader:
    """
    A class for downloading FRED-MD data and returning it as a DataFrame.
    """

    def __init__(self):
        """
        Initialize the FredMdDataDownloader class.
        """
        # FRED-MD series IDs for the data you want to download
        self.series_ids = [
            "UNRATE",  # Civilian Unemployment Rate
            "GDPC1",   # Real Gross Domestic Product
            "CPIAUCSL",  # Consumer Price Index for All Urban Consumers
            # Add more series IDs as needed
        ]

    def download_data(self, start_date, end_date):
        """
        Download FRED-MD data and return it as a DataFrame.

        Args:
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.

        Returns:
            pd.DataFrame: A DataFrame containing the downloaded data.
        """
        # Download FRED-MD data using pandas_datareader
        data = pdr.get_data_fred(self.series_ids, start=start_date, end=end_date)

        return data

if __name__ == "__main__":
    # Example usage:
    downloader = FredMdDataDownloader()
    start_date = "2000-01-01"
    end_date = "2023-12-31"
    fred_md_data = downloader.download_data(start_date, end_date)
    print(fred_md_data.head())
