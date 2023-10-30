"""
Front end dash for algo1. The app is made in dash, and it
outputs the trading signals from algo1 based on the market
input given by the user. A progress bar is included in
the app to indicated how far the app is from being
done executing.
"""
# pylint: disable=wrong-import-order.
# pylint: disable=wrong-import-position.
# pylint: disable=import-error.
# pylint: disable=too-many-arguments.
# pylint: disable=too-many-locals.
# pylint: disable=unused-argument.
from datetime import datetime, timedelta
from dash import dash_table
from dash import html
from dash import dcc
import sys
sys.path.insert(0, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects')
sys.path.insert(1, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
sys.path.insert(2, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos')
import dash
import dash_bootstrap_components as dbc
from multiprocessing import Process, Queue
import pandas as pd
from algo1 import Algo1
from algo_scrapers.s_and_p_scraper import SAndPScraper
from algo_scrapers.dax_scraper import DAXScraper
from algo_scrapers.danish_ticker_scraper import OMXC25scraper
from algo_scrapers.obx_scraper import OBXscraper
from algo_scrapers.omxs30_scraper import OMXS30scraper
from algo_scrapers.omxh25_scraper import OMXH25scraper

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the process_tickers function to process tickers in parallel
def process_tickers(queue_tickers, market, start_date,
                    end_date, consecutive_days, consecutive_days_sell, tickers):
    """
    Process a chunk of tickers and generate trading signals for each ticker.

    Parameters:
    -----------
        queue_tickers (Queue):
            A queue for storing the output results.
        start_date (str):
            The start date for retrieving price data in the format 'YYYY-MM-DD'.
        end_date (str):
            The end date for retrieving price data in the format 'YYYY-MM-DD'.
        consecutive_days (int):
            The number of consecutive days the conditions should be met for generating signals.
        tickers (list):
            A list of ticker symbols to process.

    Returns:
    --------
        None:
            The processed results are placed in the queue.
    """
    output_list = []
    for ticker1 in tickers:
        try:
            instance_1 = Algo1(ticker=ticker1,
                               start_date=start_date,
                               end_date=end_date,
                               consecutive_days=consecutive_days,
                               consecutive_days_sell=consecutive_days_sell)
            signals_1 = instance_1.generate_signals()
        except KeyError as error:
            print(f"KeyError for {ticker1}: {str(error)}")
            continue
        except ValueError as error:
            print(f"ValueError for {ticker1}: {str(error)}")
            continue

        condition1 = signals_1[ticker1 + '_Buy'] == 1
        condition2 = signals_1[ticker1 + '_Sell'] == 1

        combined_condition = condition1 | condition2

        extracted_rows = signals_1[combined_condition]

        new_df = pd.DataFrame()
        new_df["Ticker"] = [ticker1] * len(extracted_rows)
        new_df["Buy"] = [1 if b else "" for b in extracted_rows[ticker1 + '_Buy']]
        new_df["Sell"] = [-1 if s else "" for s in extracted_rows[ticker1 + '_Sell']]
        new_df.index = extracted_rows['Date']

        if not new_df.empty:
            output_list.append(new_df)

    queue_tickers.put(output_list)

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
                        {'label': 'Norwegian', 'value': 'Norwegian'},
                        {'label': 'Swedish', 'value': 'Swedish'},
                        {'label': 'Finish', 'value': 'Finish'}
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
                    end_date=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                ),
                dcc.Input(
                    id='consecutive-days-input',
                    type='number',
                    placeholder='Consecutive Days',
                    value=4,
                ),
                dcc.Input(
                    id='consecutive-days-sell-input',
                    type='number',
                    placeholder='Consecutive Days sell',
                    value=1,
                ),
                html.Div(id='out-box')
            ],
            style={"display": "inline-block", "width": "100%"},
        )
    ]
)

@app.callback(
    [dash.dependencies.Output('progress-bar', 'value'),
     dash.dependencies.Output('out-box', 'children')],
    [dash.dependencies.Input('market-dropdown', 'value'),
     dash.dependencies.Input('date-range-picker', 'start_date'),
     dash.dependencies.Input('date-range-picker', 'end_date'),
     dash.dependencies.Input('consecutive-days-input', 'value'),
     dash.dependencies.Input('consecutive-days-sell-input', 'value')]
)
def update_out_box(market, start_date, end_date, consecutive_days, consecutive_days_sell):
    """
    Update the output box with trading signals for the chosen market and time period.

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
        consecutive_days (int):
            The number of consecutive days the conditions should be met for generating signals.

    Returns:
    --------
        Tuple of (int, html.Div):
            An integer indicating the progress value of the progress bar
            and a div element containing tables with the generated signals for each ticker.
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
    elif market == 'Norwegian':
        instance_norwegian = OBXscraper()
        tickers_list = instance_norwegian.run_scraper()
    elif market == 'Swedish':
        instance_swedish = OMXS30scraper()
        tickers_list = instance_swedish.run_scraper()
    elif market == 'Finish':
        instance_finish = OMXH25scraper()
        tickers_list = instance_finish.run_scraper()

    num_tickers = len(tickers_list)
    num_processes = 4  # adjust based on system's capabilities
    tickers_per_process = num_tickers // num_processes

    # Create a queue for retrieving processed results
    results_queue = Queue()
    processes = []

    for i in range(num_processes):
        start_index = i * tickers_per_process
        end_index = (i + 1) * tickers_per_process if i != num_processes - 1 else num_tickers
        tickers_chunk = tickers_list[start_index:end_index]
        ticker_process = Process(target=process_tickers, args=(results_queue,
                                                  market,
                                                  start_date,
                                                  end_date,
                                                  consecutive_days,consecutive_days_sell,
                                                  tickers_chunk))
        ticker_process.start()
        processes.append(ticker_process)

    for ticker_process in processes:
        ticker_process.join()

    all_results = []
    for _ in range(num_processes):
        result_chunk = results_queue.get()
        all_results.extend(result_chunk)

    if not all_results:
        return 0, html.Div(children=["No signals found for the chosen period"])

    ticker_tables = [
        html.Div(
            children=[
                html.H2(f"{all_results[i]['Ticker'].iloc[0]} Signals"),
                dash_table.DataTable(
                    id=f"{all_results[i]['Ticker'].iloc[0]}-table",
                    columns=[{"name": "Date", "id": "Date"},
                             {"name": "Buy", "id": "Buy"},
                             {"name": "Sell", "id": "Sell"}],
                    data=all_results[i].reset_index().to_dict("records"),
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
        ) for i in range(len(all_results))
    ]

    # Calculate progress value based on the number of processed tickers
    progress_value = 100

    return progress_value, ticker_tables

if __name__ == "__main__":
    app.run_server(debug=True)
