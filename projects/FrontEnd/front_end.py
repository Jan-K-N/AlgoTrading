"""
Front-end beta: Basic front end project made
to invstigate the possibilities with streamlit.
"""
import sys
import os
import pandas as pd
import streamlit as st

# pylint: disable=import-error
# pylint: disable=wrong-import-position
sys.path.insert(0, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects')
sys.path.insert(1, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
from finance_database import Database
sys.path.insert(2, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos')
from algo1 import Algo1


st.title('AlgoTrading: Stock comparison')

tickers = ('TSLA','AAPL')

# dropdown = st.multiselect('Pick your asset',
#                           tickers)


# if len(dropdown) > 0:
start = st.date_input('Start', value=pd.to_datetime('2023-05-01'))
end = st.date_input('End', value=pd.to_datetime('today'))
instance = Algo1(start_date='2019-01-01', end_date='2023-04-25',tickers_list=['TSLA','AAPL'])
df1 = instance.algo1_loop()
st.dataframe(df1,use_container_width=True)


# /Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/FrontEnd/front_end.py
