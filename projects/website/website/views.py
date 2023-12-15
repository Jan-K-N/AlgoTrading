# myapp/views.py
from django.http import HttpResponse
from datetime import timedelta, date

import sys
print(sys.path)
sys.path.append("/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos")
sys.path.append('/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algo_scrapers')
import pandas as pd

from danish_ticker_scraper import OMXC25scraper
from django.shortcuts import render
from algo1 import Algo1

# tickers = ['TSLA', 'FLS.CO', 'AAPL']
#
# start_date = "2021-01-01"
# end_date = "2023-01-01"
#
# output_list = []
# for ticker1 in tickers:
#     try:
#         instance_1 = Algo1(ticker=ticker1,
#                            start_date=start_date,
#                            end_date=end_date,
#                            consecutive_days=1,
#                            consecutive_days_sell=1)
#         signals_1 = instance_1.generate_signals()
#     except KeyError as error:
#         print(f"KeyError for {ticker1}: {str(error)}")
#         continue
#     except ValueError as error:
#         print(f"ValueError for {ticker1}: {str(error)}")
#         continue
#
#     condition1 = signals_1[ticker1 + '_Buy'] == 1
#     condition2 = signals_1[ticker1 + '_Sell'] == -1
#
#     combined_condition = condition1 | condition2
#
#     extracted_rows = signals_1[combined_condition]
#
#     new_df = pd.DataFrame()
#     new_df["Ticker"] = [ticker1] * len(extracted_rows)
#     new_df["Buy"] = [1 if b else "" for b in extracted_rows[ticker1 + '_Buy']]
#     new_df["Sell"] = [-1 if s else "" for s in extracted_rows[ticker1 + '_Sell']]
#     new_df.index = extracted_rows['Date']
#
#     if not new_df.empty:
#         output_list.append(new_df)
#
#
# signals_data = [
#     {'Ticker': output_list[0].iloc[-1].Ticker,'Buy':output_list[0].iloc[-1].Buy,'Sell':output_list[0].iloc[-1].Sell,
#      'Date':output_list[0].index[-1].strftime('%Y-%m-%d %H:%M:%S')},
#     {'Ticker': output_list[1].iloc[-1].Ticker,'Buy':output_list[1].iloc[-1].Buy,'Sell':output_list[1].iloc[-1].Sell,
#      'Date':output_list[1].index[-1].strftime('%Y-%m-%d %H:%M:%S')},
#     {'Ticker': output_list[2].iloc[-1].Ticker,'Buy':output_list[0].iloc[-1].Buy,'Sell':output_list[2].iloc[-1].Sell,
#      'Date':output_list[2].index[-1].strftime('%Y-%m-%d %H:%M:%S')},
#
# ]

print("k")


def home(request):
    # You can add your news content here later
    news_content = []

    # tickers = ['TSLA', 'FLS.CO', 'AAPL']
    scraper_instance = OMXC25scraper()
    tickers = scraper_instance.run_scraper()

    start_date = "2021-01-01"
    end_date = "2023-01-01"

    output_list = []
    for ticker1 in tickers:
        try:
            instance_1 = Algo1(ticker=ticker1,
                               start_date=start_date,
                               end_date=end_date,
                               consecutive_days=1,
                               consecutive_days_sell=1)
            signals_1 = instance_1.generate_signals()
        except KeyError as error:
            print(f"KeyError for {ticker1}: {str(error)}")
            continue
        except ValueError as error:
            print(f"ValueError for {ticker1}: {str(error)}")
            continue

        condition1 = signals_1[ticker1 + '_Buy'] == 1
        condition2 = signals_1[ticker1 + '_Sell'] == -1

        combined_condition = condition1 | condition2

        extracted_rows = signals_1[combined_condition]

        new_df = pd.DataFrame()
        new_df["Ticker"] = [ticker1] * len(extracted_rows)
        new_df["Buy"] = [1 if b else "" for b in extracted_rows[ticker1 + '_Buy']]
        new_df["Sell"] = [-1 if s else "" for s in extracted_rows[ticker1 + '_Sell']]
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


    # Pass the news content to the template
    context = {'news_content': news_content,
               'signals_data':signals_data
               }

    return render(request, 'myapp/home.html', context)

def about(request):
    return render(request, 'myapp/about.html')
