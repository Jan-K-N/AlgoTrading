"""
Main script for scraping FXRates.
"""
import requests
import pandas as pd
import xmltodict

class ExchangeRatesScraper:
    """
    A class for scraping exchange rates from Danmarks Nationalbank's website
    and converting amounts between currencies based on the scraped data.

    Args:
        url (str): The URL of the website containing the exchange rate data.

    Attributes:
        url (str): The URL of the website containing the exchange rate data.

    Methods:
        scrape(): Scrapes the exchange rates from the website and returns the data as a DataFrame.
        convert(amount, from_currency, date): Converts an amount from one currency to 'DKK'
            based on the exchange rate on a given date.

    """
    def __init__(self, url:str)->None:
        """
        Initializes an instance of ExchangeRatesScraper with the specified URL.

        Args:
            url (str): The URL of the website containing the exchange rate data.
        """
        self.url = url

    def scrape(self):
        """
        Scrapes the exchange rates published on Danmarks Nationalbank's website.
        The prices are in Danish kroner for 1 units of the foreign currency.

        Returns:
            pandas.DataFrame: A DataFrame containing the scraped data with columns:
                - 'Date': The date of the exchange rate observation.
                - 'Currency': The currency code.
                - 'Exchange Rate': The exchange rate value.
        """
        response = requests.get(self.url,timeout=10)
        xml_data = response.content
        data_dict = xmltodict.parse(xml_data)
        data = []
        for obs in data_dict['gesmes:Envelope']['Cube']['Cube']:
            date = obs['@time']
            for series in obs['Cube']:
                currency = series['@currency']
                rate = series['@rate']
                if rate != '-':  # Skip '-' values
                    rate = float(rate) / 100
                else:
                    rate = 0
                data.append([date, currency, rate])
        data = pd.DataFrame(data, columns=['Date', 'Currency', 'Exchange Rate'])
        return data

    def convert(self, amount:float, from_currency:str, date:str):
        """
        Converts an amount from one currency to 'DKK' on the exchange rate on a given date.

        Args:
            amount (float): The amount to be converted.
            from_currency (str): The currency code of the original currency.
            date (str): The date in the format 'YYYY-MM-DD' for which the exchange rate is required.

        Returns:
            float or None: The converted amount if the exchange rate is found, otherwise None.

        Raises:
            None

        Examples:
            >>> ExchangeRatesScraper.convert(100, 'USD', '2022-05-12')
            121.5
            >>> ExchangeRatesScraper.convert(50, 'EUR', '2023-01-01')
            65.0
            >>> ExchangeRatesScraper.convert(200, 'GBP', '2023-04-27')
            None
        """
        rates = self.scrape()
        rate = rates.loc[(rates['Currency'] == from_currency) & (rates['Date'] == date),
        'Exchange Rate']
        if not rate.empty:
            rate = float(rate)
            converted_amount = amount * rate
            return converted_amount

        return None
