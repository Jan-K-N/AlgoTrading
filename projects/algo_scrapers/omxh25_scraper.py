"""
Main script for ticker scraper in the main index in Finland (OMXH25).
The class in the script outputs the ticker symbols in the index.
The ticker codes steem from wikipedia.
"""
# pylint: disable=duplicate-code
# pylint: disable=wrong-import-position
import logging
import sys
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

sys.path.insert(0, '..')
from data.finish_tickers import TickerCodeProvider

class OMXH25scraper:
    """
    A class for scraping ticker codes from the OMXH25 Wikipedia page.

    Attributes:
        base_url (str): The base URL of the Wikipedia page.
        ticker_url (str): The URL of the OMXH25 Wikipedia page.

    Methods:
        __init__(): Initialize the OMXH25scraper class.
        scrape_ticker_codes(): Scrape ticker codes from the OMXH25 Wikipedia page.
        run_scraper(): Run the ticker code scraping process.
    """
    def __init__(self):
        """
        Initialize the scraper class.

        The base URL is set to 'https://en.wikipedia.org',
        and the ticker URL is set to the OMXH25 Wikipedia page URL.
        """
        self.base_url = 'https://en.wikipedia.org'
        self.ticker_url = self.base_url + '/wiki/OMX_Helsinki_25'

    def scrape_ticker_codes(self)->list:
        """
        Scrape ticker codes from the base_url Wikipedia page.

        Returns:
            list: A list of ticker codes.

        Raises:
            requests.exceptions.RequestException: If an error occurs while accessing the website.
        """
        try:
            response = requests.get(self.ticker_url,timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')

            scraped_table_omxh25 = soup.find('table', {'class': 'wikitable sortable'})
            scraped_rows_omxh25 = scraped_table_omxh25.find_all('tr')

            # Container to store the ticker codes in:
            ticker_codes_omxh25 = []
            # Open a loop to insert the ticker codes:
            for ticker_row_obx in scraped_rows_omxh25[1:]:
                columns = ticker_row_obx.find_all('td')
                # Replace all whitespaces with "-" and add a ".HE", so that
                # we can download the tickers on yahoo finance.
                obx_tickername = columns[2].text.strip().replace(" ", "-") + ".HE"
                ticker_codes_omxh25.append(obx_tickername)

            return ticker_codes_omxh25

        except requests.exceptions.RequestException as exc:
            logging.error("An error occurred in the process of accessing the website in the "
                          "scraping process: %s", str(exc))
            return None

    def run_scraper(self)->list:
        """
        Method to run the scraper. The method returns a list.

        Returns:
            list: A list of ticker codes obtained from the scraping process.
        """
        print("Retrieving ticker codes from...:",self.ticker_url)
        ticker_codes_omxh25=self.scrape_ticker_codes()

        ticker_codes_additional = TickerCodeProvider.get_ticker_codes()
        ticker_codes_omxh25.extend(ticker_codes_additional)

        return ticker_codes_omxh25
