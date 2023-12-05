# myapp/views.py
from django.http import HttpResponse
from datetime import timedelta, date
from django.shortcuts import render


def home(request):
    # You can add your news content here later
    news_content = []



    signals_data = [
        {'ticker': 'AAPL', 'signal': 'Buy', 'price': 150.25, 'date': '2023-12-01'},
        {'ticker': 'GOOGL', 'signal': 'Sell', 'price': 2800.50, 'date': '2023-12-02'},
        # Add more signals as needed
    ]

    # Pass the news content to the template
    context = {'news_content': news_content,
               'signals_data':signals_data}

    return render(request, 'myapp/home.html', context)

# def about(request):
#     return HttpResponse("About Page")
def about(request):
    return render(request, 'myapp/about.html')
