"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('danish/', views.danish_signals,name='danish_signals'),
    path('sweden/', views.sweden_signals, name='sweden_signals'),
    path('american/', views.american_signals, name='american_signals'),
    path('danish_navigation/',views.danish_navigation,name='danish_navigation'),
    path('american_navigation/',views.american_navigation,name='american_navigation'),
    path('danish_backtest/',views.danish_backtest,name='danish_backtest'),
    path('about/', views.about, name='about'),
]
