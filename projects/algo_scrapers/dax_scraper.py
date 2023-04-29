"""
Main script for ticker scraper in dax. The class in the script
outputs the ticker codes in the Dax.
"""
import requests
from bs4 import BeautifulSoup
import schedule
import datetime
import time
import argparse
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class DAXScraper:
    def __init__(self):
        self.base_url = 'https://en.wikipedia.org'
        self.ticker_url = self.base_url + '/wiki/DAX'

    def scrape_ticker_codes(self):
        try:
            response = requests.get(self.ticker_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table', {'class': 'wikitable sortable'})
            rows = table.find_all('tr')

            ticker_codes = []

            for row in rows[1:]:
                columns = row.find_all('td')
                ticker_code = columns[3].text.strip()
                ticker_codes.append(ticker_code)

            return ticker_codes

        except requests.exceptions.RequestException as e:
            logging.error("Error occurred while accessing the website: %s", str(e))
            return None

    def run_scraper(self):
        ticker_codes=self.scrape_ticker_codes()
        print("Ticker Codes:",ticker_codes)

# Create an instance of the scraper
scraper = DAXScraper()

def schedule_scraper():
    scraper.run_scraper()

# Define the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--now', action='store_true', help='Run the script immediately')

args = parser.parse_args()

if args.now:
    print("Running the script now...")
    scraper.run_scraper()
else:
    # Schedule the scraper to run every Friday at 12:00
    schedule.every().friday.at("12:00").do(schedule_scraper)

    # Run the scheduler continuously
    while True:
        schedule.run_pending()
        now = datetime.datetime.now()
        print("Waiting for the next scheduled run...", now)
        # Sleep for a while before checking the schedule again
        time.sleep(60)  # Sleep for 60 seconds between schedule checks

## To run the script now, we can write the following in the terminal:
# python script.py --now

## To schedule the script, we can run:
# python script.py

#, where script.py is the name of our script.


