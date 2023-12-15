# myapp/views.py
from django.http import HttpResponse
from datetime import timedelta, date

import sys
print(sys.path)
sys.path.append("/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos")
import pandas

from django.shortcuts import render
from algo1 import Algo1

instance = Algo1(start_date="2021-01-01", end_date="2023-01-01", consecutive_days = 1,
                 ticker = 'TSLA')



def home(request):
    # You can add your news content here later
    news_content = []

    # instance = Algo1(start_date = "2021-01-01",end_date="2023-01-01",
    #                  tickers_list=['TSLA','AAPL','FLS.CO'])
    # import pdb; pdb.set_trace()
    # k = instance.algo1_loop()

    signals_data = [
        {'ticker': 'AAPL', 'signal': 'Buy', 'price': 165.25, 'date': '2023-12-01'},
        {'ticker': 'GOOGL', 'signal': 'Sell', 'price': 2800.50, 'date': '2023-12-02'},
        # Add more signals as needed
    ]

    # Pass the news content to the template
    context = {'news_content': news_content,
               'signals_data':signals_data
               }

    return render(request, 'myapp/home.html', context)

def about(request):
    return render(request, 'myapp/about.html')
