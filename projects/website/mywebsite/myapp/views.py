# myapp/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to My Website.")

def about(request):
    return HttpResponse("About Page")
