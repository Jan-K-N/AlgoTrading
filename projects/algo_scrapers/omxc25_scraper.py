"""
Main script for ticker scraper in the Danish index (C25). The class in the script
outputs the ticker codes in C25 index.
"""
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class OMXC25scraper:
    """
    A class for scraping ticker codes from the C25 Wikipedia page.

    Attributes:
        base_url (str): The base URL of the Wikipedia page.
        ticker_url (str): The URL of the C25 Wikipedia page.

    Methods:
        __init__(): Initialize the OMXC25Scraper class.
        scrape_ticker_codes(): Scrape ticker codes from the C25 Wikipedia page.
        run_scraper(): Run the ticker code scraping process.
    """
    def __init__(self):
        """
        Initialize the scraper class.

        The base URL is set to 'https://en.wikipedia.org',
        and the ticker URL is set to the OMXC25 Wikipedia page URL.
        """
        self.base_url = 'https://en.wikipedia.org'
        self.ticker_url = self.base_url + '/wiki/OMX_Copenhagen_25'

    def scrape_ticker_codes(self)->list:
        """
        Scrape ticker codes from the OMXC25 Wikipedia page.

        Returns:
            list: A list of ticker codes.

        Raises:
            requests.exceptions.RequestException: If an error occurs while accessing the website.
        """
        try:
            response = requests.get(self.ticker_url,timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table', {'class': 'wikitable sortable'})
            rows = table.find_all('tr')

            ticker_codes = []

            for row in rows[1:]:
                columns = row.find_all('td')
                ticker_name = columns[2].text.strip().replace(" ", "-") + ".CO"
                ticker_codes.append(ticker_name)

            return ticker_codes

        except requests.exceptions.RequestException as exc:
            logging.error("Error occurred while accessing the website: %s", str(exc))
            return None

    def run_scraper(self)->list:
        """
        Run the ticker code scraping process.

        Returns:
            list: A list of ticker codes obtained from the scraping process.
        """
        print("Retrieving ticker codes from...:",self.ticker_url)
        ticker_codes=self.scrape_ticker_codes()
        return ticker_codes
