"""
Views for KN Trading Django web application:

This module contains Django views for the KN Trading web application.
The views include functions to retrieve trading signals data, render
the home page with news content and trading signals for Danish stocks,
and render the about page.

Functions:
    - get_signals_data(scraper: object, start_date: str, end_date: str) -> list:
        Retrieves trading signals data for a given scraper, start date, and end date.

    - home(request) -> HttpResponse:
        Renders the home page with news content and trading signals data for Danish stocks.

    - about(request) -> HttpResponse:
        Renders the about page.

Dependencies:
    - datetime: Module for working with dates and times.
    - sys: System-specific parameters and functions.
    - pandas: Data manipulation library.
    - danish_ticker_scraper: Custom module for scraping Danish stock tickers.
    - render: Function for rendering HTML responses in Django.
    - algo1: Custom module for implementing trading algorithms.
"""
# myapp/views.py
# pylint: disable=wrong-import-order.
# pylint: disable=wrong-import-position.
# pylint: disable=unused-variable.
# pylint: disable=too-many-locals.
from datetime import timedelta, datetime
import pandas as pd

import sys
sys.path.insert(0,'..')
from algo_scrapers.danish_ticker_scraper import OMXC25scraper
from algo_scrapers.omxs30_scraper import OMXS30scraper
from algo_scrapers.s_and_p_scraper import SAndPScraper
from algo_scrapers.obx_scraper import OBXscraper
from django.shortcuts import render
from algos.algo1 import Algo1


def get_signals_data(scraper: object, start_date: str, end_date: str,
                     consecutive_days: int = 1, consecutive_days_sell: int = 1):
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
                             consecutive_days=consecutive_days,
                             consecutive_days_sell=consecutive_days_sell)
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
    Renders the home page.

    Parameters:
    _________
        request: The HTTP request object.

    Returns:
    _________
        HttpResponse: The rendered HTML response for the home page.
    """

    return render(request, 'myapp/home.html')

def danish_signals(request):
    """
     Renders the Danish page with trading signals data for Danish stocks.

     Parameters:
     _________
         request: The HTTP request object.

     Returns:
     _________
         HttpResponse: The rendered HTML response for the Danish page.
     """

    default_end_date = datetime.now().strftime('%Y-%m-%d')
    default_start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    if request.method == 'GET':
        start_date = request.GET.get('start_date', default_start_date)
        end_date = request.GET.get('end_date', default_end_date)
        consecutive_days = int(request.GET.get('consecutive_days', 1))
        consecutive_days_sell = int(request.GET.get('consecutive_days_sell', 1))
    else:
        start_date = default_start_date
        end_date = default_end_date
        consecutive_days = 1
        consecutive_days_sell = 1

    omxc25_scraper = OMXC25scraper()

    # Pass consecutive_days and consecutive_days_sell to get_signals_data function
    omxc25_signals_data = get_signals_data(omxc25_scraper, start_date, end_date,
                                           consecutive_days, consecutive_days_sell)
    context = {
        'omxc25_signals_data': omxc25_signals_data,
        'start_date': start_date,
        'end_date': end_date,
        'consecutive_days': consecutive_days,
        'consecutive_days_sell': consecutive_days_sell,
    }


    return render(request, 'myapp/danish_signals.html', context)

def sweden_signals(request):
    """
    Renders the Swedish page with trading signals.

    Parameters:
    _________
        request: The HTTP request object.

    Returns:
    _________
        HttpResponse: The rendered HTML response for the Swedish page.
    """

    default_end_date = datetime.now().strftime('%Y-%m-%d')
    default_start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    if request.method == 'GET':
        start_date = request.GET.get('start_date', default_start_date)
        end_date = request.GET.get('end_date', default_end_date)
        consecutive_days = int(request.GET.get('consecutive_days', 1))
        consecutive_days_sell = int(request.GET.get('consecutive_days_sell', 1))
    else:
        start_date = default_start_date
        end_date = default_end_date
        consecutive_days = 1
        consecutive_days_sell = 1

    omxs30_scraper = OMXS30scraper()

    omxs30_signals_data = get_signals_data(omxs30_scraper, start_date, end_date,
                                           consecutive_days,consecutive_days_sell)

    context = {
        'omxs30_signals_data': omxs30_signals_data,
        'start_date': start_date,
        'end_date': end_date,
        'consecutive_days': consecutive_days,
        'consecutive_days_sell': consecutive_days_sell,
    }

    return render(request, 'myapp/sweden_signals.html', context)

def danish_navigation(request):
    """
    Renders the danish_navigation page.

    Parameters:
    _________
        request: The HTTP request object.

    Returns:
    _________
        HttpResponse: The rendered HTML response for the danish_navigation page.
    """

    return render(request, 'myapp/danish_navigation.html')

def american_navigation(request):
    """
    Renders the american_navigation page.

    Parameters:
    _________
        request: The HTTP request object.

    Returns:
    _________
        HttpResponse: The rendered HTML response for the american_navigation page.
    """

    return render(request, 'myapp/american_navigation.html')

def algo1_navigation(request):
    """
    Renders the algo1_navigation page.

    Parameters:
    _________
        request: The HTTP request object.

    Returns:
    _________
        HttpResponse: The rendered HTML response for the algo1_navigation page.
    """

    return render(request, 'myapp/algo1_navigation.html')

def sentinel_navigation(request):
    """
    Renders the sentinel_navigation page.

    Parameters:
    _________
        request: The HTTP request object.

    Returns:
    _________
        HttpResponse: The rendered HTML response for the sentinel_navigation page.
    """

    return render(request, 'myapp/sentinel_navigation.html')

def database_status(request):
    """
    Renders the database_status page.

    Parameters:
    _________
        request: The HTTP request object.

    Returns:
    _________
        HttpResponse: The rendered HTML response for the database_status page.
    """

    return render(request, 'myapp/database_status.html')





def sentinel_signals_american(request):
    """
    Renders the sentinel_signals_american page.

    Parameters:
    _________
        request: The HTTP request object.

    Returns:
    _________
        HttpResponse: The rendered HTML response for the sentinel_signals_american page.
    """

    return render(request, 'myapp/sentinel_signals_american.html')


def norwegian_navigation(request):
    """
    Renders the norwegian_navigation page.

    Parameters:
    _________
        request: The HTTP request object.

    Returns:
    _________
        HttpResponse: The rendered HTML response for the norwegian_navigation page.
    """

    return render(request, 'myapp/norwegian_navigation.html')

def american_signals(request):
    """
     Renders the American page with trading signals data for American stocks.

     Parameters:
     _________
         request: The HTTP request object.

     Returns:
     _________
         HttpResponse: The rendered HTML response for the American page.
     """

    default_end_date = datetime.now().strftime('%Y-%m-%d')
    default_start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    if request.method == 'GET':
        start_date = request.GET.get('start_date', default_start_date)
        end_date = request.GET.get('end_date', default_end_date)
        consecutive_days = int(request.GET.get('consecutive_days', 1))
        consecutive_days_sell = int(request.GET.get('consecutive_days_sell', 1))
    else:
        start_date = default_start_date
        end_date = default_end_date
        consecutive_days = 1
        consecutive_days_sell = 1

    sandp_scraper = SAndPScraper()

    # Pass consecutive_days and consecutive_days_sell to get_signals_data function
    sandp_signals_data = get_signals_data(sandp_scraper, start_date, end_date,
                                           consecutive_days, consecutive_days_sell)
    context = {
        'sandp_signals_data': sandp_signals_data,
        'start_date': start_date,
        'end_date': end_date,
        'consecutive_days': consecutive_days,
        'consecutive_days_sell': consecutive_days_sell,
    }

    return render(request, 'myapp/american_signals.html', context)


def norwegian_signals(request):
    """
     Renders the Norwegian page with trading signals data for Norwegian stocks.

     Parameters:
     _________
         request: The HTTP request object.

     Returns:
     _________
         HttpResponse: The rendered HTML response for the Norwegian page.
     """

    default_end_date = datetime.now().strftime('%Y-%m-%d')
    default_start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    if request.method == 'GET':
        start_date = request.GET.get('start_date', default_start_date)
        end_date = request.GET.get('end_date', default_end_date)
        consecutive_days = int(request.GET.get('consecutive_days', 1))
        consecutive_days_sell = int(request.GET.get('consecutive_days_sell', 1))
    else:
        start_date = default_start_date
        end_date = default_end_date
        consecutive_days = 1
        consecutive_days_sell = 1

    obx_scraper = OBXscraper()

    # Pass consecutive_days and consecutive_days_sell to get_signals_data function
    obx_signals_data = get_signals_data(obx_scraper, start_date, end_date,
                                           consecutive_days, consecutive_days_sell)
    context = {
        'obx_signals_data': obx_signals_data,
        'start_date': start_date,
        'end_date': end_date,
        'consecutive_days': consecutive_days,
        'consecutive_days_sell': consecutive_days_sell,
    }

    return render(request, 'myapp/norwegian_signals.html', context)

def danish_backtest(request):
    """
    Renders the Danish backtest page.

    Parameters:
    _________
        request: The HTTP request object.

    Returns:
    _________
        HttpResponse: The rendered HTML response for the backtest page.
    """

    return render(request,'myapp/danish_backtest.html')

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
