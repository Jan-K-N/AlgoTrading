"""
Main script for ticker scraper in dax. The class in the script
outputs the ticker codes in the Dax.
"""

import requests
from bs4 import BeautifulSoup


class DAXScraper:
    def __init__(self):
        self.base_url = 'https://www.deutsche-boerse.com'
        self.ticker_url = self.base_url + '/dbg-en/products-services/indices/selection-indices/dax-constituents'

    def scrape_ticker_codes(self):
        response = requests.get(self.ticker_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        ticker_table = soup.find('table', {'class': 'table-blue'})
        ticker_rows = ticker_table.find_all('tr')

        ticker_codes = []

        for row in ticker_rows[1:]:
            columns = row.find_all('td')
            ticker_code = columns[1].text.strip()
            ticker_codes.append(ticker_code)

        return ticker_codes


# Example usage
scraper = DAXScraper()
ticker_codes = scraper.scrape_ticker_codes()

print(ticker_codes)

