"""
Main script for scraping FXRates.
"""
import requests
import pandas as pd
import xmltodict

class ExchangeRatesScraper:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        response = requests.get(self.url)
        xml_data = response.content
        data_dict = xmltodict.parse(xml_data)
        data = []
        for obs in data_dict['gesmes:Envelope']['Cube']['Cube']:
            date = obs['@time']
            for series in obs['Cube']:
                currency = series['@currency']
                rate = series['@rate']
                data.append([date, currency, rate])
        return pd.DataFrame(data, columns=['Date', 'Currency', 'Exchange Rate'])

if __name__ == '__main__':
    url = 'https://www.nationalbanken.dk/_vti_bin/DN/DataService.svc/CurrencyRatesHistoryXML?lang=en'
    scraper = ExchangeRatesScraper(url)
    k = scraper.scrape()
    print(k)




