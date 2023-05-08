"""
Front end dash for algo1. The app is beta.
"""
import sys
sys.path.insert(0, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects')
sys.path.insert(1, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
sys.path.insert(2, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos')
sys.path.insert(3, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algo_scrapers')
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from datetime import datetime as dt
from algo1 import Algo1
from s_and_p_scraper import SAndPScraper
from dax_scraper import DAXScraper

# Instance of scrapers:
instanceSP500 = SAndPScraper()
SP500Tickers = instanceSP500.run_scraper()

instanceDAX = DAXScraper()
DAXTickers = instanceDAX.run_scraper()


# # Instantiate the Algo1 class with multiple tickers
# algo_instance = Algo1(start_date='2020-05-02', end_date='2023-05-04', tickers_list=SP500Tickers)
# output_list = algo_instance.algo1_loop()

# Create the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(
    children=[
        html.H1("Algo1 Loop Output"),
        html.Div(
            children=[
                dcc.Dropdown(
                    id='market-dropdown',
                    options=[
                        {'label': 'S&P 500', 'value': 'SP500'},
                        {'label': 'DAX', 'value': 'DAX'}
                    ],
                    value='SP500',
                    clearable=False
                ),
                dcc.DatePickerRange(
                    id='date-range-picker',
                    start_date_placeholder_text='Start Date',
                    end_date_placeholder_text='End Date',
                    min_date_allowed="2010-01-01",
                    max_date_allowed="2023-05-08",
                    initial_visible_month="2021-01-01",
                    start_date="2021-01-01",
                    end_date="2023-05-08"
                )
            ],
            style={"display": "inline-block", "width": "100%"},
        ),
        html.Div(id='out-box')
    ]
)


@app.callback(
    dash.dependencies.Output('out-box', 'children'),
    dash.dependencies.Input('market-dropdown', 'value'),
    dash.dependencies.Input('date-range-picker', 'start_date'),
    dash.dependencies.Input('date-range-picker', 'end_date')
)
def update_out_box(market, start_date, end_date):
    if market == 'SP500':
        tickers_list = SP500Tickers
    elif market == 'DAX':
        tickers_list = DAXTickers

    algo_instance = Algo1(start_date=start_date, end_date=end_date, tickers_list=tickers_list)
    output_list = algo_instance.algo1_loop()

    # Check if output_list is empty
    if not output_list:
        return html.Div(children=["No signals found for the chosen period"])

    # Create DataTable for each ticker
    ticker_tables = [
        html.Div(
            children=[
                html.H2(f"{ticker} Signals"),
                dash_table.DataTable(
                    id=f"{ticker}-table",
                    columns=[{"name": "Date", "id": "Date"},
                             {"name": "Buy", "id": "Buy"},
                             {"name": "Sell", "id": "Sell"}],
                    data=output_list[i].reset_index().to_dict("records"),
                    style_table={"overflowX": "scroll"},
                    style_data_conditional=[
                        {
                            'if': {
                                'filter_query': '{Buy} = 1',
                                'column_id': 'Buy'
                            },
                            'backgroundColor': '#3D9970'
                        },
                        {
                            'if': {
                                'filter_query': '{Sell} = 1',
                                'column_id': 'Sell'
                            },
                            'backgroundColor': '#FF4136'
                        }
                    ]
                )
            ]
        ) for i, ticker in enumerate(tickers_list)
    ]

    return ticker_tables

if __name__ == "__main__":
    app.run_server(debug=True)