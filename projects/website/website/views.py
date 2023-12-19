# myapp/views.py
from datetime import timedelta, date, datetime

import sys
sys.path.append("/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos")
sys.path.append('/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algo_scrapers')
import pandas as pd

from danish_ticker_scraper import OMXC25scraper
from django.shortcuts import render
from algo1 import Algo1


def get_signals_data(scraper: object, start_date: str, end_date: str):
    """
    Retrieves trading signals data for a given scraper, start date, and end date.

    Parameters:
    _________
        scraper (object): An object with a 'run_scraper' method to retrieve a list of tickers.
        start_date (str): Start date for the signal analysis in the format 'YYYY-MM-DD'.
        end_date (str): End date for the signal analysis in the format 'YYYY-MM-DD'.

    Returns:
    _________
        list: A list of dictionaries, each containing trading signals data for a specific ticker.
        Each dictionary has keys 'Ticker', 'Buy', 'Sell', and 'Date'.
    """
    output_list = []
    tickers_list = scraper.run_scraper()

    for ticker in tickers_list:
        try:
            instance = Algo1(ticker=ticker,
                             start_date=start_date,
                             end_date=end_date,
                             consecutive_days=1,
                             consecutive_days_sell=1)
            signals = instance.generate_signals()
        except KeyError as error:
            print(f"KeyError for {ticker}: {str(error)}")
            continue
        except ValueError as error:
            print(f"ValueError for {ticker}: {str(error)}")
            continue

        condition1 = signals[ticker + '_Buy'] == 1
        condition2 = signals[ticker + '_Sell'] == -1

        combined_condition = condition1 | condition2

        extracted_rows = signals[combined_condition]

        new_df = pd.DataFrame()
        new_df["Ticker"] = [ticker] * len(extracted_rows)
        new_df["Buy"] = [1 if b else "" for b in extracted_rows[ticker + '_Buy']]
        new_df["Sell"] = [-1 if s else "" for s in extracted_rows[ticker + '_Sell']]
        new_df.index = extracted_rows['Date']

        if not new_df.empty:
            output_list.append(new_df)

        signals_data = []

        for i, output_df in enumerate(output_list):
            signal_entry = {
                'Ticker': output_df.iloc[-1].Ticker,
                'Buy': output_df.iloc[-1].Buy,
                'Sell': output_df.iloc[-1].Sell,
                'Date': output_df.index[-1].strftime('%Y-%m-%d'),
            }

            signals_data.append(signal_entry)

    return signals_data

def home(request):
    """
    Renders the home page with news content and trading signals data for Danish stocks.

    Parameters:
    _________
        request: The HTTP request object.

    Returns:
    _________
        HttpResponse: The rendered HTML response for the home page.
    """
    news_content = []

    default_end_date = datetime.now().strftime('%Y-%m-%d')
    default_start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    if request.method == 'GET':
        start_date = request.GET.get('start_date', default_start_date)
        end_date = request.GET.get('end_date', default_end_date)
    else:
        start_date = default_start_date
        end_date = default_end_date

    omxc25_scraper = OMXC25scraper()

    omxc25_signals_data = get_signals_data(omxc25_scraper, start_date, end_date)

    context = {
        'news_content': news_content,
        'omxc25_signals_data': omxc25_signals_data,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'myapp/home.html', context)

def about(request):
    """
    Renders the about page.

    Parameters:
    _________
        request: The HTTP request object.

    Returns:
    _________
        HttpResponse: The rendered HTML response for the about page.
    """
    return render(request, 'myapp/about.html')
