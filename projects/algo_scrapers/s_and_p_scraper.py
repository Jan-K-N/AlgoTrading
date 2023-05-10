"""
Main script for scraping S&P500 ticker codes from Wikipedia.
"""
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class SAndPScraper:
    """
    A class for scraping ticker codes from the S&P500.

    Attributes:
        base_url (str): The base URL of the S&P500.
        ticker_url (str): The URL of the S&P500 page.

    Methods:
        __init__(): Initialize the SAndPScraper class.
        scrape_ticker_codes(): Scrape ticker codes from the S&P500.
        run_scraper(): Run the ticker code scraping process.
    """
    def __init__(self):
        """
        Initialize the SAndPScraper class.

        The base URL is set to 'https://en.wikipedia.org',
        and the ticker URL is set to the S&P500 page URL.
        """
        self.base_url = 'https://en.wikipedia.org'
        self.ticker_url = self.base_url + '/wiki/List_of_S%26P_500_companies'

    def scrape_ticker_codes(self) -> list:
        """
        Scrape ticker codes from the S&P500 page.

        Returns:
            list: A list of ticker codes.

        Raises:
            requests.exceptions.RequestException: If an error occurs while accessing the website.
        """
        try:
            response = requests.get(self.ticker_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table', {'class': 'wikitable sortable'})
            rows = table.find_all('tr')[1:]

            ticker_codes = list(map(lambda row: row.find_all('td')[0].text.strip(), rows))

            return ticker_codes
        except requests.exceptions.RequestException as exc:
            raise exc

    def run_scraper(self) -> list:
        """
        Run the ticker code scraping process.

        Returns:
            list: A list of ticker codes obtained from the scraping process.
        """
        print("Retrieving ticker codes from...:", self.ticker_url)
        ticker_codes = self.scrape_ticker_codes()
        return ticker_codes
