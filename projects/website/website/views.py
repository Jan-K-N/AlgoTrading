# myapp/views.py
from django.http import HttpResponse
from datetime import timedelta, date, datetime

import sys
sys.path.append("/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos")
sys.path.append('/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algo_scrapers')
import pandas as pd

from danish_ticker_scraper import OMXC25scraper
from omxs30_scraper import OMXS30scraper
from django.shortcuts import render
from algo1 import Algo1

print("k")

# def get_signals_data(scraper, start_date, end_date):
#     signals_data = []
#
#     tickers_list = scraper.run_scraper()
#
#     for ticker in tickers_list:
#         try:
#             instance = Algo1(ticker=ticker,
#                              start_date=start_date,
#                              end_date=end_date,
#                              consecutive_days=1,
#                              consecutive_days_sell=1)
#             signals = instance.generate_signals()
#         except KeyError as error:
#             print(f"KeyError for {ticker}: {str(error)}")
#             continue
#         except ValueError as error:
#             print(f"ValueError for {ticker}: {str(error)}")
#             continue
#
#         condition1 = signals[ticker + '_Buy'] == 1
#         condition2 = signals[ticker + '_Sell'] == -1
#
#         combined_condition = condition1 | condition2
#
#         extracted_rows = signals[combined_condition]
#
#         new_df = pd.DataFrame()
#         new_df["Ticker"] = [ticker] * len(extracted_rows)
#         new_df["Buy"] = [1 if b else "" for b in extracted_rows[ticker + '_Buy']]
#         new_df["Sell"] = [-1 if s else "" for s in extracted_rows[ticker + '_Sell']]
#         new_df.index = extracted_rows['Date']
#
#         if not new_df.empty:
#             signals_data.append(new_df)
#
#     return signals_data
#
# def home(request):
#     news_content = []
#
#     default_end_date = datetime.now().strftime('%Y-%m-%d')
#     default_start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
#
#     if request.method == 'GET':
#         start_date = request.GET.get('start_date', default_start_date)
#         end_date = request.GET.get('end_date', default_end_date)
#     else:
#         start_date = default_start_date
#         end_date = default_end_date
#
#     omxc25_scraper = OMXC25scraper()
#     swedish_stocks_scraper = OMXS30scraper()
#
#     omxc25_signals_data = get_signals_data(omxc25_scraper, start_date, end_date)
#     swedish_stocks_signals_data = get_signals_data(swedish_stocks_scraper, start_date, end_date)
#
#     context = {
#         'news_content': news_content,
#         'omxc25_signals_data': omxc25_signals_data,
#         'swedish_stocks_signals_data': swedish_stocks_signals_data,
#         'start_date': start_date,
#         'end_date': end_date,
#     }
#
#     return render(request, 'myapp/home.html', context)
#
# def about(request):
#     return render(request, 'myapp/about.html')
def get_signals_data_as_list(scraper, start_date, end_date):
    signals_data = []

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

        # Convert the index to datetime if it's not already
        if not isinstance(extracted_rows.index, pd.DatetimeIndex):
            extracted_rows.index = pd.to_datetime(extracted_rows.index)

        new_data = extracted_rows.copy()

        # Format the date column
        new_data['Date'] = new_data.index.strftime('%Y-%m-%d')

        # Convert to a list of dictionaries
        new_data_list = new_data.reset_index().to_dict(orient='records')

        if new_data_list:
            signals_data.extend(new_data_list)

    return signals_data

def home(request):
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
    swedish_stocks_scraper = OMXS30scraper()

    omxc25_signals_data = get_signals_data_as_list(omxc25_scraper, start_date, end_date)
    swedish_stocks_signals_data = get_signals_data_as_list(swedish_stocks_scraper, start_date, end_date)

    context = {
        'news_content': news_content,
        'omxc25_signals_data': omxc25_signals_data,
        'swedish_stocks_signals_data': swedish_stocks_signals_data,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'myapp/home.html', context)

def about(request):
    return render(request, 'myapp/about.html')
