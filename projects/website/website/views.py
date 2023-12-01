# myapp/views.py
from django.http import HttpResponse
from datetime import timedelta, date
from django.shortcuts import render

def home(request):
    # You can add your news content here later
    news_content = []

    # Pass the news content to the template
    context = {'news_content': news_content}
    return render(request, 'myapp/home.html', context)

def about(request):
    return HttpResponse("About Page")
