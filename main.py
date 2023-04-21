"""
This is the main script. From this script we will call the functions from the other scripts,
and then inspect them and do analysis. This involves making various charts etc.
"""



import os

os.chdir(r"/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading") # Change wd.

######################## Chart 1: Plot of stock:
    
# https://github.com/markumreed/data_science_for_everyone/blob/main/bokeh_project/myFinanceDashboard/bokeh_finance_example.py
    
    
from Data.FinanceDatabase import exchange_components, download_data
import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import Dropdown, Select 
from bokeh.layouts import column, row
from bokeh.io import curdoc


data = download_data(ticker = 'FLS')['Close']





from datetime import datetime

from datetime import timedelta

dt = datetime.now()
dt


# get current date
d = datetime.now().date() - timedelta(0)






print(str(d) + "00:00:00")




# get weekday
print(d.strftime('%w'))
