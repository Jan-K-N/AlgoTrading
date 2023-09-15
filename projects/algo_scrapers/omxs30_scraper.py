"""
Main script for ticker scraper in the Swedish index (OMXS30). The class in the script
outputs the ticker symbols in the index.
"""
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class OMXS30scraper:
    """
    A class for scraping ticker codes from the OMXS30 Wikipedia page.

    Attributes:
        base_url (str): The base URL of the Wikipedia page.
        ticker_url (str): The URL of the OMXS30 Wikipedia page.

    Methods:
        __init__(): Initialize the OMXS30scraper class.
        scrape_ticker_codes(): Scrape ticker codes from the OMXS30 Wikipedia page.
        run_scraper(): Run the ticker code scraping process.
    """
    def __init__(self):
        """
        Initialize the scraper class.

        The base URL is set to 'https://en.wikipedia.org',
        and the ticker URL is set to the OMXC25 Wikipedia page URL.
        """
        self.base_url = 'https://en.wikipedia.org'
        self.ticker_url = self.base_url + '/wiki/OMX_Stockholm_30'

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

            table = soup.find('table', {'class': 'wikitable sortable'})
            rows = table.find_all('tr')

            # Container to store the ticker codes in:
            ticker_codes_omxs30 = []
            # Open a loop to insert the ticker codes:
            for row in rows[1:]:
                columns = row.find_all('td')
                # Replace all whitespaces with "-" and add a ".ST", so that
                # we can download the tickers on yahoo finance.
                omxs30_tickername = columns[1].text.strip().replace(" ", "-") + ".ST"
                ticker_codes_omxs30.append(omxs30_tickername)

            return ticker_codes_omxs30

        except requests.exceptions.RequestException as exc:
            logging.error("An error occurred while accessing the website in the "
                          "scraping process: %s", str(exc))
            return None

    def run_scraper(self)->list:
        """
        Method to run the scraper. The method returns a list.

        Returns:
            list: A list of ticker codes obtained from the scraping process.
        """
        print("Retrieving ticker codes from...:",self.ticker_url)
        ticker_codes_omxs30=self.scrape_ticker_codes()
        return ticker_codes_omxs30
