"""
Front-end beta: Basic front end project made
to invstigate the possibilities with streamlit.
"""
import sys
import os
import pandas as pd
import streamlit as st
import dash_table

# pylint: disable=import-error
# pylint: disable=wrong-import-position
sys.path.insert(0, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects')
sys.path.insert(1, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
from finance_database import Database
sys.path.insert(2, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos')
from algo1 import Algo1


# st.title('AlgoTrading: Stock comparison')
#
# tickers = ('TSLA','AAPL')
#
# # dropdown = st.multiselect('Pick your asset',
# #                           tickers)
#
#
# # if len(dropdown) > 0:
# start = st.date_input('Start', value=pd.to_datetime('2023-05-01'))
# end = st.date_input('End', value=pd.to_datetime('today'))
# instance = Algo1(start_date='2019-01-01', end_date='2023-04-25',tickers_list=['TSLA','AAPL'])
# df1 = instance.algo1_loop()
#
# # Display each DataFrame
# for idx, df in enumerate(df1):
#     st.write(f"DataFrame {idx + 1}:",unsafe_allow_html=True)
#     st.dataframe(df)
#     # st.write("---")  # Add a separator between DataFrames
#
#
# # # /Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/FrontEnd/front_end.py
import pandas as pd
import dash
import dash_table
import dash_html_components as html

# Instantiate the Algo1 class with multiple tickers
algo_instance = Algo1(
    tickers_list=['AAPL', 'GOOGL','TSLA'],
    start_date='2020-01-01',
    end_date='2023-03-20'
)

# Get the output from algo1_loop method
output_list = algo_instance.algo1_loop()

# Create the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(
    children=[
        html.H1("Algo1 Loop Output")
    ] + [
        html.Div(
            children=[
                html.H2(f"{ticker} Signals"),
                dash_table.DataTable(
                    id=f"{ticker}-table",
                    columns=[{"name": "Date", "id": "Date"}, {"name": "Buy", "id": "Buy"}, {"name": "Sell", "id": "Sell"}],
                    data=output_list[i].reset_index().to_dict("records"),
                    style_table={"overflowX": "scroll"},
                ),
            ],
            style={"display": "inline-block", "width": "50%"},
        ) for i, ticker in enumerate(algo_instance.tickers_list)
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)