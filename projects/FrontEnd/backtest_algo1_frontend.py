"""
Main script for the algo1 backtest frontend.
"""
# pylint: disable=import-error.
# pylint: disable=wrong-import-order
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

sys.path.insert(0,'/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos_backtest')

from algo1_backtest import Algo1Backtest

class Algo1BacktestApp:
    """
    A Streamlit app for backtesting and visualizing returns using Algo1Backtest.

    Attributes:
        title (str): The title of the app.
        default_start_date (str): The default start date for the date input field.
        default_end_date (str): The default end date for the date input field.
    """

    def __init__(self):
        """Initialize the Algo1BacktestApp class."""
        self.title = "Algo1 Backtest Returns. Simple returns."
        self.default_start_date = '2010-02-01'
        self.default_end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    def run(self):
        """
        Run the Algo1BacktestApp.

        This method executes the app by displaying the title, getting the date inputs,
        getting the ticker input, running the backtest, and displaying the returns chart.
        """
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
        """Display the title of the app."""
        st.title(self.title)

    def get_date_inputs(self):
        """
        Get the start and end date inputs.

        Returns:
            Tuple[str, str]: The start date and end date in ISO format.
        """
        start_date = st.date_input('Start Date',
                                   value=datetime.fromisoformat(self.default_start_date).date())
        end_date = st.date_input('End Date',
                                 value=datetime.fromisoformat(
                                     self.default_end_date).date())
        start_date_iso = start_date.isoformat()
        end_date_iso = end_date.isoformat()
        return start_date_iso, end_date_iso

    def get_ticker_input(self):
        """
        Get the ticker input.

        Returns:
            List[str]: The list of tickers.
        """
        ticker_input = st.text_input('Tickers (comma-separated)', value='TSLA, AAPL, GOOGL')
        tickers = [ticker.strip() for ticker in ticker_input.split(',')]
        return tickers

    def run_backtest(self, start_date, end_date, tickers):
        """
        Run the backtest for the given tickers.

        Args:
            start_date (str): The start date in ISO format.
            end_date (str): The end date in ISO format.
            tickers (List[str]): The list of tickers.

        Returns:
            List[pd.DataFrame]: The list of dataframes containing
             'Buy Date', 'Sell Date', and 'Returns' columns.
        """
        returns_df_list = []
        for ticker in tickers:
            instance_backtest = Algo1Backtest(start_date=start_date,
                                              end_date=end_date,
                                              tickers_list=[ticker])
            returns_df_list.extend(instance_backtest.backtest_returns())
        return returns_df_list

    def display_returns_chart(self, combined_df):
        """
        Display the returns chart.

        Args:
            combined_df (pd.DataFrame):
             The combined dataframe containing 'Sell Date', 'Returns', and 'Ticker' columns.
        """
        fig = px.line(combined_df, x='Sell Date', y='Returns', color='Ticker',
                      title='Algo1 Backtest Returns')
        st.plotly_chart(fig)


if __name__ == "__main__":
    app = Algo1BacktestApp()
    app.run()
