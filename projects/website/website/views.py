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
# pylint: disable=duplicate-code.
# pylint: disable=broad-exception-caught.

from datetime import timedelta, datetime
import pandas as pd
import os
import sys
sys.path.insert(0,'..')
from algo_scrapers.danish_ticker_scraper import OMXC25scraper
from algo_scrapers.omxs30_scraper import OMXS30scraper
from algo_scrapers.s_and_p_scraper import SAndPScraper
from algo_scrapers.obx_scraper import OBXscraper
from algos.algo1 import Algo1
from algos.gap_detector import GapDetector
from django.shortcuts import render
from django.http import JsonResponse
from data.finance_database import DatabaseScheduler, Database
from pathlib import Path
from django.shortcuts import redirect
from .forms import DateForm

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
        new_df.index = pd.to_datetime(extracted_rows['Date'])


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

def gap_detector_get_signals(start_date, end_date, specific_date, market):
    """
    Method for collecting relevant objects for the Gapdetector algo.
    This objects should then be cast into the django app.

    Parameters:
    _________
        start_date (str): Start date for the signal analysis in the format 'YYYY-MM-DD'.
        end_date (str): End date for the signal analysis in the format 'YYYY-MM-DD'.
        specific_date (str): String to control if a specific signal date is wanted.
        market (str): Variable to control which market we want to run the algo for.

    Returns:
    _________
    signals_list (list): List of DataFrames containing gap signals for each ticker.
    backtested_list (list): List of backtested returns DataFrames for each ticker.
    trade_returns_list (list): List of DataFrames containing trade returns for each ticker.
    """
    signals_list = []
    backtested_list = []
    trade_returns_list = []
    all_data = {}

    # Code section to control scraper:
    if market == "USA":
        tickers_list0 = SAndPScraper()
        tickers_list = tickers_list0.run_scraper()

    elif market == "Denmark":
        tickers_list0 = OMXC25scraper()
        tickers_list = tickers_list0.run_scraper()
    elif market == "Sweden":
        tickers_list0 = OMXS30scraper()
        tickers_list = tickers_list0.run_scraper()

    for ticker in tickers_list:
        try:
            if market == "USA":
                db_instance = Database()
                db_path = Path.home() / "Desktop" / "Database" / "SandP.db"

                data = db_instance.retrieve_data_from_database(start_date=start_date,
                                                               end_date=end_date,
                                                               ticker=ticker,
                                                               database_path=db_path)
            else:
                instance_database0 = Database(start=start_date,
                                              end=end_date,
                                              ticker=ticker)
                data = instance_database0.get_price_data()

            data.set_index('Date', inplace=True)
            all_data[ticker] = data
        except Exception as e:
            print(f"Error fetching data for ticker {ticker}: {e}")
            continue

    for ticker in tickers_list:
        if ticker not in all_data:
            continue

        instance = GapDetector(start_date=start_date, end_date=end_date, ticker=ticker, data=all_data[ticker])

        try:
            # Apply the combined strategy
            data, gap_up, gap_down = instance.detect_gaps_with_macd(gap_threshold=1.5)

            # Check if there are any signals before appending
            if gap_up.any() or gap_down.any():
                # Create a DataFrame for signals
                signals_df = pd.DataFrame({
                    'Date': data.index,
                    'Gap_Up': gap_up,
                    'Gap_Down': gap_down
                })
                signals_df['Ticker'] = ticker

                # Append the DataFrame to the list
                signals_list.append(signals_df)

                # Backtest the strategy for this ticker
                backtested_returns, trades_df = instance.backtest_gap_strategy(gap_up, gap_down, specific_date)
                backtested_df = pd.DataFrame({
                    'Date': data.index[:len(backtested_returns)],
                    'Cumulative_Returns': backtested_returns
                })
                backtested_df['Ticker'] = ticker
                backtested_list.append(backtested_df)
                trade_returns_list.append(trades_df)

        except Exception as e:
            print(f"Error processing ticker {ticker}: {e}")
            continue

    return signals_list, backtested_list, trade_returns_list




# def gap_detector_signals(request):
#     start_date = request.GET.get('start_date', (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
#     end_date = request.GET.get('end_date', datetime.now().strftime('%Y-%m-%d'))
#     specific_date = request.GET.get('specific_date', '')
#     market = request.session.get('market', 'USA')
#
#     signals_list, specific_date_signals_list, backtested_list, trade_returns_list = gap_detector_get_signals(
#         start_date=start_date,
#         end_date=end_date,
#         specific_date=specific_date,
#         market=market
#     )
#
#     context = {
#         'signals_list': signals_list,
#         'specific_date_signals_list': specific_date_signals_list,
#         'backtested_list': backtested_list,
#         'trade_returns_list': trade_returns_list,
#     }
#
#     return render(request, 'myapp/gap_detector_signals.html', context)
# myapp/views.py

def gap_detector_signals(request):
    extracted_rows = []
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            specific_date = form.cleaned_data['specific_date']
            market = form.cleaned_data['market']

            # Retrieve the signals for the selected dates and market
            signals_list, backtested_list, trade_returns_list = gap_detector_get_signals(
                start_date, end_date, specific_date, market)

            # Iterate over signals_list
            for df in signals_list:
                # Extract rows where 'Date' equals specific_date
                rows = df[df['Date'] == specific_date]
                for _, row in rows.iterrows():
                    extracted_rows.append(row.to_dict())

            # Print extracted_rows to inspect its content
            print("Extracted Rows:")
            for row in extracted_rows:
                print(row)

            # Similarly, process backtested_list and trade_returns_list as needed

    else:
        form = DateForm()

    context = {
        'form': form,
        'extracted_rows': extracted_rows
    }
    return render(request, 'myapp/gap_detector_signals.html', context)

def get_signals_for_dates(start_date, end_date, specific_date):
    # Placeholder function - replace with actual data retrieval logic
    # Example DataFrame
    data = {
        'Date': [specific_date, start_date, end_date],
        'Ticker': ['AAPL', 'GOOGL', 'MSFT'],
        'Gap_Up': [True, False, True],
        'Gap_Down': [False, True, False],
    }
    df = pd.DataFrame(data)
    return [df]


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
    request.session['market'] = 'USA'
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

def run_database_script():
    """
    Runs the database script to update the database with new data.

    This function executes the database script to update the database with new data.
    It retrieves data from various sources, processes it, and inserts it into the database.

    Note: This function is designed to be called periodically to keep the database up to date.

    Dependencies:
    - SAndPScraper: Custom module for scraping S&P stock tickers.
    - Database: Custom module for database operations.
    - DatabaseScheduler: Custom module for scheduling database operations.
    """
    tickers_list0 = SAndPScraper()

    instance_database0 = Database(start="2019-01-01",
                                 end=datetime.today().strftime("%Y-%m-%d"),
                                 scraper=tickers_list0)

    # Create the 'Database' folder on the user's desktop if it doesn't exist
    desktop_path = Path.home() / "Desktop"
    database_folder_path = desktop_path / "Database"
    if not database_folder_path.exists():
        os.makedirs(database_folder_path)

    db_path = database_folder_path / "SandP.db"

    db_scheduler = DatabaseScheduler(instance_database0, database_path=db_path)

    # Schedule the insertion of price data every minute
    db_scheduler.run_insert_price_data()

# pylint: disable=unused-argument
def run_script_view(request):
    """
    Runs the database update script view.

    This function is a view that handles requests to run the database update script.
    It calls the `run_database_script()` function, which updates the database with new data.
    If the script runs successfully, it returns a JSON response indicating success.
    If an error occurs during script execution, it returns a JSON response with the error message.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - JsonResponse: A JSON response indicating success or failure of the script execution.
    """
    try:
        run_database_script()  # Call the function that runs the script
        return JsonResponse({'success': True, 'message': 'Database updated successfully'})
    except Exception as error:
        return JsonResponse({'success': False, 'message': str(error)})

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

# if __name__ == "__main__":
#     k = gap_detector_get_signals(start_date="2022-01-01",
#                                  end_date="2024-01-01",
#                                  specific_date="2023-01-01",
#                                  market = "Denmark")
#     print("k")