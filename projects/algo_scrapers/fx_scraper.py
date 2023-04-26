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

    def convert(self, amount, from_currency, to_currency, date):
        rates = self.scrape()
        rate = rates.loc[(rates['Currency'] == to_currency) & (rates['Date'] == date), 'Exchange Rate']
        if not rate.empty:
            rate = float(rate)
            converted_amount = amount * rate
            return converted_amount
        else:
            return None

if __name__ == '__main__':
    url = 'https://www.nationalbanken.dk/_vti_bin/DN/DataService.svc/CurrencyRatesHistoryXML?lang=en'
    scraper = ExchangeRatesScraper(url)
    rates = scraper.scrape()
    print(rates)

    amount = 100 # e.g. 100 EUR
    from_currency = 'USD'
    to_currency = 'EUR'
    date = '2023-04-25'
    converted_amount = scraper.convert(amount, from_currency, to_currency, date)
    print(f'{amount} {from_currency} is {converted_amount:.2f} {to_currency} on {date}')



