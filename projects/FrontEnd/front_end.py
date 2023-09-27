"""
Front end dash for algo1. The app is made in dash, and it
outputs the trading signals from algo1 based on the market
input given by the user. A progress bar is included in
the app to indicated how far the app is from being
done executing.
"""
import sys
from datetime import datetime, timedelta
import dash
from dash import dash_table
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd

sys.path.insert(0, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects')
sys.path.insert(1, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
sys.path.insert(2, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos')
# pylint: disable=import-error
# pylint: disable=wrong-import-position
from algos.algo1 import Algo1
from algo_scrapers.s_and_p_scraper import SAndPScraper
from algo_scrapers.dax_scraper import DAXScraper
from algo_scrapers.danish_ticker_scraper import OMXC25scraper
from algo_scrapers.obx_scraper import OBXscraper
from algo_scrapers.omxs30_scraper import OMXS30scraper
from algo_scrapers.omxh25_scraper import OMXH25scraper

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = html.Div(
    children=[
        html.H1("Algo1 signal finder"),
        html.Div(
            children=[
                dbc.Progress(value=0, id='progress-bar', style={'width': '50%', 'margin': 'auto'}),
                dcc.Dropdown(
                    id='market-dropdown',
                    options=[
                        {'label': 'DAX', 'value': 'DAX'},
                        {'label': 'S&P 500', 'value': 'SP500'},
                        {'label': 'NASDAQ Copenhagen', 'value': 'NASDAQ Copenhagen'},
                        {'label': 'OBX', 'value': 'OBX'},
                        {'label': 'OMXS30', 'value': 'OMXS30'},
                        {'label': 'OMXH25', 'value': 'OMXH25'}
                    ],
                    value='DAX',
                    clearable=False
                ),
                dcc.DatePickerRange(
                    id='date-range-picker',
                    start_date_placeholder_text='Start Date',
                    end_date_placeholder_text='End Date',
                    min_date_allowed="2015-01-01",
                    max_date_allowed=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                    initial_visible_month=datetime.now().strftime('%Y-%m-%d'),
                    start_date=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                    end_date=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                ),
                html.Div(id='out-box')
            ],
            style={"display": "inline-block", "width": "100%"},
        )
    ]
)


def count_changes(df):
    if 'Buy' in df.columns:
        buy_values = pd.to_numeric(df['Buy'])
        sell_to_buy_changes = ((buy_values.diff() == -1) & (buy_values == 1)).sum()
        buy_to_sell_changes = ((buy_values.diff() == 1) & (buy_values == -1)).sum()
        return sell_to_buy_changes + buy_to_sell_changes
    return 0

@app.callback(
    [dash.dependencies.Output('progress-bar', 'value'),
     dash.dependencies.Output('out-box', 'children')],
    [dash.dependencies.Input('market-dropdown', 'value'),
     dash.dependencies.Input('date-range-picker', 'start_date'),
     dash.dependencies.Input('date-range-picker', 'end_date')]
)
def update_out_box(market:str, start_date:str, end_date:str)->(int, html.Div):
    """
    Update the output box with signals for the chosen market and time period.

    Parameters:
    -----------
    market (str):
        The market for which the signals are generated.
    start_date (str):
        The start date of the time period for which the signals are generated,
        in the format 'YYYY-MM-DD'.
    end_date (str):
        The end date of the time period for which the signals are generated,
        in the format 'YYYY-MM-DD'.

    Returns:
    -----------
    (int, html.Div): An integer indicating the progress value of the progress bar and
                    a div element containing tables with the generated signals for each ticker.
    """
    if market == 'DAX':
        instance_dax = DAXScraper()
        tickers_list = instance_dax.run_scraper()

    elif market == 'SP500':
        instance_sp500 = SAndPScraper()
        tickers_list = instance_sp500.run_scraper()

    elif market == 'NASDAQ Copenhagen':
        instance_nasdaq_copenhagen = OMXC25scraper()
        tickers_list = instance_nasdaq_copenhagen.run_scraper()

    elif market == 'OBX':
        instance_obx = OBXscraper()
        tickers_list = instance_obx.run_scraper()

    elif market == 'OMXS30':
        instance_omxs30 = OMXS30scraper()
        tickers_list = instance_omxs30.run_scraper()

    elif market == 'OMXH25':
        instance_omxh25 = OMXH25scraper()
        tickers_list = instance_omxh25.run_scraper()

    algo_instance = Algo1(start_date=start_date, end_date=end_date, tickers_list=tickers_list)
    output_list = algo_instance.algo1_loop()

    # Check if output_list is empty
    if not output_list:
        return 0, html.Div(children=["No signals found for the chosen period"])

    # Sort output_list based on the count of changes
    output_list.sort(key=count_changes, reverse=True)

    ticker_tables = [
        html.Div(
            children=[
                html.H2(f"{df['Ticker'].iloc[0]} Signals"),
                dash_table.DataTable(
                    id=f"{df['Ticker'].iloc[0]}-table",
                    columns=[{"name": "Date", "id": "Date"},
                             {"name": "Buy", "id": "Buy"},
                             {"name": "Sell", "id": "Sell"}],
                    data=df.reset_index().to_dict("records"),
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
                                'filter_query': '{Sell} = -1',
                                'column_id': 'Sell'
                            },
                            'backgroundColor': '#FF4136'
                        }
                    ]
                )
            ]
        ) for df in output_list
    ]

    # Calculate progress value based on the number of processed tickers
    progress_value = int(len(output_list) / len(tickers_list) * 100)

    return progress_value, ticker_tables


if __name__ == "__main__":
    app.run_server(debug=True)

