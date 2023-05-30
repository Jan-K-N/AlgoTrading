"""
Main script for the algo1 backtest frontend.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


import sys
sys.path.insert(0,'/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos_backtest')

from algo1_backtest import Algo1Backtest

class Algo1BacktestApp:
    def __init__(self):
        self.title = "Algo1 Backtest Returns. Simple returns."
        self.default_start_date = '2010-02-01'
        self.default_end_date = '2023-01-01'

    def run(self):
        self.show_title()
        start_date, end_date = self.get_date_inputs()
        tickers = self.get_ticker_input()

        returns_df_list = self.run_backtest(start_date, end_date, tickers)

        if returns_df_list:
            combined_df = pd.concat(returns_df_list, ignore_index=True)
            self.display_returns_chart(combined_df)
        else:
            st.write("No returns found for the selected tickers in the selected period.")

    def show_title(self):
        st.title(self.title)

    def get_date_inputs(self):
        start_date = st.date_input('Start Date', value=datetime.fromisoformat(self.default_start_date).date())
        end_date = st.date_input('End Date', value=datetime.fromisoformat(self.default_end_date).date())
        start_date_iso = start_date.isoformat()
        end_date_iso = end_date.isoformat()
        return start_date_iso, end_date_iso

    def get_ticker_input(self):
        ticker_input = st.text_input('Tickers (comma-separated)', value='TSLA, AAPL, GOOGL')
        tickers = [ticker.strip() for ticker in ticker_input.split(',')]
        return tickers

    def run_backtest(self, start_date, end_date, tickers):
        returns_df_list = []
        for ticker in tickers:
            instance_backtest = Algo1Backtest(start_date=start_date, end_date=end_date, tickers_list=[ticker])
            returns_df_list.extend(instance_backtest.backtest_returns())
        return returns_df_list

    def display_returns_chart(self, combined_df):
        fig = px.line(combined_df, x='Sell Date', y='Returns', color='Ticker',
                      title='Algo1 Backtest Returns')
        st.plotly_chart(fig)


if __name__ == "__main__":
    app = Algo1BacktestApp()
    app.run()
