"""
Front end dash for algo1. The app is beta.
"""
import sys
import dash
import dash_table
import dash_html_components as html
# pylint: disable=import-error
# pylint: disable=wrong-import-position
sys.path.insert(0, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects')
sys.path.insert(1, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/data')
sys.path.insert(2, '/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos')
from algo1 import Algo1

# Instantiate the Algo1 class with multiple tickers
algo_instance = Algo1(
    tickers_list=['AAPL', 'GOOGL'],
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
                    columns=[{"name": "Date", "id": "Date"},
                             {"name": "Buy", "id": "Buy"},
                             {"name": "Sell", "id": "Sell"}],
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
