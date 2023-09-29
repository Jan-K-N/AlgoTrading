# """
# Front end dash for algo1. The app is made in dash, and it
# outputs the trading signals from algo1 based on the market
# input given by the user. A progress bar is included in
# the app to indicated how far the app is from being
# done executing.
# """
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
sys.path.insert(3, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos_backtest')
# pylint: disable=import-error
# pylint: disable=wrong-import-position
from algos.algo1 import Algo1
from algo_scrapers.s_and_p_scraper import SAndPScraper
from algo_scrapers.dax_scraper import DAXScraper
from algo_scrapers.danish_ticker_scraper import OMXC25scraper
from algo_scrapers.obx_scraper import OBXscraper
from algo_scrapers.omxs30_scraper import OMXS30scraper
from algo_scrapers.omxh25_scraper import OMXH25scraper
from algo1_backtest import Algo1Backtest
#
# # Create the Dash app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#
# # Define the app layout
# app.layout = html.Div(
#     children=[
#         html.H1("Algo1 signal finder"),
#         html.Div(
#             children=[
#                 dbc.Progress(value=0, id='progress-bar', style={'width': '50%', 'margin': 'auto'}),
#                 dcc.Dropdown(
#                     id='market-dropdown',
#                     options=[
#                         {'label': 'DAX', 'value': 'DAX'},
#                         {'label': 'S&P 500', 'value': 'SP500'},
#                         {'label': 'NASDAQ Copenhagen', 'value': 'NASDAQ Copenhagen'},
#                         {'label': 'OBX', 'value': 'OBX'},
#                         {'label': 'OMXS30', 'value': 'OMXS30'},
#                         {'label': 'OMXH25', 'value': 'OMXH25'}
#                     ],
#                     value='DAX',
#                     clearable=False
#                 ),
#                 dcc.DatePickerRange(
#                     id='date-range-picker',
#                     start_date_placeholder_text='Start Date',
#                     end_date_placeholder_text='End Date',
#                     min_date_allowed="2015-01-01",
#                     max_date_allowed=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
#                     initial_visible_month=datetime.now().strftime('%Y-%m-%d'),
#                     start_date=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
#                     end_date=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
#                 ),
#                 html.Div(id='out-box')
#             ],
#             style={"display": "inline-block", "width": "100%"},
#         )
#     ]
# )
#
#
# # def count_changes(df):
# #     """
# #     Count the number of changes in position (Buy to Sell or Sell to Buy) in the given DataFrame.
# #
# #     Parameters:
# #     -----------
# #     df (pd.DataFrame):
# #         DataFrame containing 'Buy' and 'Sell' columns.
# #
# #     Returns:
# #     -----------
# #     int: Number of changes in position.
# #     """
# #     if 'Buy' in df.columns and 'Sell' in df.columns:
# #         # Convert 'Buy' column values to numeric values and fill NaN values with 0
# #         df_numeric = df.replace({'Buy': 1, 'Sell': -1}).fillna(0)
# #
# #         # Convert 'Buy' column to numeric (in case it's not already)
# #         df_numeric['Buy'] = pd.to_numeric(df_numeric['Buy'], errors='coerce')
# #
# #         # Add a new column 'Changes' representing the count of changes in position
# #         df_numeric['Changes'] = ((df_numeric['Buy'].diff() != 0) & (df_numeric['Buy'] != 0)).sum()
# #
# #         # Return the count of changes
# #         return df_numeric['Changes'].sum()
# #     else:
# #         return 0
#
#
#
#
# @app.callback(
#     [dash.dependencies.Output('progress-bar', 'value'),
#      dash.dependencies.Output('out-box', 'children')],
#     [dash.dependencies.Input('market-dropdown', 'value'),
#      dash.dependencies.Input('date-range-picker', 'start_date'),
#      dash.dependencies.Input('date-range-picker', 'end_date')]
# )
# def update_out_box(market:str, start_date:str, end_date:str)->(int, html.Div):
#     """
#     Update the output box with signals for the chosen market and time period.
#
#     Parameters:
#     -----------
#     market (str):
#         The market for which the signals are generated.
#     start_date (str):
#         The start date of the time period for which the signals are generated,
#         in the format 'YYYY-MM-DD'.
#     end_date (str):
#         The end date of the time period for which the signals are generated,
#         in the format 'YYYY-MM-DD'.
#
#     Returns:
#     -----------
#     (int, html.Div): An integer indicating the progress value of the progress bar and
#                     a div element containing tables with the generated signals for each ticker.
#     """
#     if market == 'DAX':
#         instance_dax = DAXScraper()
#         tickers_list = instance_dax.run_scraper()
#
#     elif market == 'SP500':
#         instance_sp500 = SAndPScraper()
#         tickers_list = instance_sp500.run_scraper()
#
#     elif market == 'NASDAQ Copenhagen':
#         instance_nasdaq_copenhagen = OMXC25scraper()
#         tickers_list = instance_nasdaq_copenhagen.run_scraper()
#
#     elif market == 'OBX':
#         instance_obx = OBXscraper()
#         tickers_list = instance_obx.run_scraper()
#
#     elif market == 'OMXS30':
#         instance_omxs30 = OMXS30scraper()
#         tickers_list = instance_omxs30.run_scraper()
#
#     elif market == 'OMXH25':
#         instance_omxh25 = OMXH25scraper()
#         tickers_list = instance_omxh25.run_scraper()
#
#     algo_instance = Algo1Backtest(start_date=start_date, end_date=end_date, tickers_list=tickers_list)
#     output_list = algo_instance.algo1_loop()
#
#     # Check if output_list is empty
#     if not output_list:
#         return 0, html.Div(children=["No signals found for the chosen period"])
#
#     # Compute volatility for each ticker
#     volatility_df = algo_instance.compute_volatility()
#
#     # Merge the volatility information with the output_list
#     for i in range(len(output_list)):
#         ticker = output_list[i]['Ticker'].iloc[0]
#         volatility_value = volatility_df.loc[ticker, 'Volatility']
#         output_list[i]['Volatility'] = volatility_value
#
#     # Sort output_list based on volatility in descending order
#     output_list.sort(key=lambda x: x['Volatility'], reverse=True)
#
#     ticker_tables = [
#         html.Div(
#             children=[
#                 html.H2(f"{output_list[i]['Ticker'].iloc[0]} Signals (Volatility: {output_list[i]['Volatility']:.2f})"),
#                 dash_table.DataTable(
#                     id=f"{output_list[i]['Ticker'].iloc[0]}-table",
#                     columns=[
#                         {"name": "Date", "id": "Date"},
#                         {"name": "Buy", "id": "Buy"},
#                         {"name": "Sell", "id": "Sell"},
#                         {"name": "Volatility", "id": "Volatility"}],
#                     data=output_list[i].reset_index().to_dict("records"),
#                     style_table={"overflowX": "scroll"},
#                     style_data_conditional=[
#                         {
#                             'if': {
#                                 'filter_query': '{Buy} = 1',
#                                 'column_id': 'Buy'
#                             },
#                             'backgroundColor': '#3D9970'
#                         },
#                         {
#                             'if': {
#                                 'filter_query': '{Sell} = -1',
#                                 'column_id': 'Sell'
#                             },
#                             'backgroundColor': '#FF4136'
#                         }
#                     ]
#                 )
#             ]
#         ) for i in range(len(output_list))
#     ]
#
#     # Calculate progress value based on the number of processed tickers
#     progress_value = int(len(output_list) / len(tickers_list) * 100)
#
#     return progress_value, ticker_tables
#
#
# if __name__ == "__main__":
#     app.run_server(debug=True)
"""
Front end dash for algo1 backtest. The app is made in dash, and it
outputs the trading signals from algo1 based on the market input given by the user.
A progress bar is included in the app to indicated how far the app is from being
done executing.
"""
# import sys
# from datetime import datetime, timedelta
# import dash
# from dash import dash_table
# from dash import html
# from dash import dcc
# import dash_bootstrap_components as dbc
# import pandas as pd
#
# sys.path.insert(0, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects')
# sys.path.insert(1, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
# # pylint: disable=import-error
# # pylint: disable=wrong-import-position
# from algos.algo1 import Algo1
# from algo_scrapers.s_and_p_scraper import SAndPScraper
# from algo_scrapers.dax_scraper import DAXScraper
# from algo_scrapers.danish_ticker_scraper import OMXC25scraper
# from algo_scrapers.obx_scraper import OBXscraper
# from algo_scrapers.omxs30_scraper import OMXS30scraper
# from algo_scrapers.omxh25_scraper import OMXH25scraper
# from algos_backtest import Algo1Backtest

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
    """
    Count the number of changes in position (Buy to Sell or Sell to Buy) in the given DataFrame.

    Parameters:
    -----------
    df (pd.DataFrame):
        DataFrame containing 'Buy' and 'Sell' columns.

    Returns:
    -----------
    int: Number of changes in position.
    """
    if 'Buy' in df.columns and 'Sell' in df.columns:
        # Convert 'Buy' column values to numeric values and fill NaN values with 0
        df_numeric = df.replace({'Buy': 1, 'Sell': -1}).fillna(0)

        # Convert 'Buy' column to numeric (in case it's not already)
        df_numeric['Buy'] = pd.to_numeric(df_numeric['Buy'], errors='coerce')

        # Add a new column 'Changes' representing the count of changes in position
        df_numeric['Changes'] = ((df_numeric['Buy'].diff() != 0) & (df_numeric['Buy'] != 0)).sum()

        # Return the count of changes
        return df_numeric['Changes'].sum()
    else:
        return 0


@app.callback(
    [dash.dependencies.Output('progress-bar', 'value'),
     dash.dependencies.Output('out-box', 'children')],
    [dash.dependencies.Input('market-dropdown', 'value'),
     dash.dependencies.Input('date-range-picker', 'start_date'),
     dash.dependencies.Input('date-range-picker', 'end_date')]
)
def update_out_box(market: str, start_date: str, end_date: str) -> (int, html.Div):
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

    algo_instance = Algo1Backtest(start_date=start_date, end_date=end_date, tickers_list=tickers_list)

    # Call compute_volatility method to get volatility for each ticker
    volatility_df = algo_instance.compute_volatility()

    # Sort tickers based on volatility
    tickers_sorted = volatility_df.sort_values(by='Volatility', ascending=False)['Ticker'].tolist()

    # Run algo1 with the sorted tickers
    algo_instance.tickers_list = tickers_sorted
    output_list = algo_instance.run_algo1()

    # Check if output_list is empty
    if not output_list:
        return 0, html.Div(children=["No signals found for the chosen period"])

    # Sort output_list based on the count of changes
    output_list.sort(key=count_changes, reverse=True)

    ticker_tables = [
        html.Div(
            children=[
                html.H2(f"{output_list[i]['Ticker'].iloc[0]} Signals"),
                dash_table.DataTable(
                    id=f"{output_list[i]['Ticker'].iloc[0]}-table",
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
                                'filter_query': '{Sell} = -1',
                                'column_id': 'Sell'
                            },
                            'backgroundColor': '#FF4136'
                        }
                    ]
                )
            ]
        ) for i in range(len(output_list))
    ]

    # Calculate progress value based on the number of processed tickers
    progress_value = int(len(output_list) / len(tickers_list) * 100)

    return progress_value, ticker_tables


if __name__ == "__main__":
    app.run_server(debug=True)

