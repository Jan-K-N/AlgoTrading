"""
Front-end beta: Basic front end project made
to invstigate the possibilities with streamlit.
"""
import sys
import pandas as pd
import streamlit as st

# pylint: disable=import-error
# pylint: disable=wrong-import-position
sys.path.insert(1, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
from finance_database import Database

st.title('AlgoTrading: Stock comparison')

tickers = ('TSLA','AAPL')

dropdown = st.multiselect('Pick your asset',
                          tickers)

start = st.date_input('Start', value = pd.to_datetime('2021-01-01'))
end = st.date_input('End', value = pd.to_datetime('today'))


instance = Database()

if len(dropdown) > 0:
    df = instance.get_price_data(start=start, end=end, ticker=dropdown)
    df = df['Adj Close']
    st.line_chart(df)

# /Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/FrontEnd/front_end.py
