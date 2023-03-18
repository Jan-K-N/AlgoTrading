# Reference: https://www.youtube.com/watch?v=hSPmj7mK6ng

# --- Import modules --- #
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash.dependencies import Input,Output
import dash_core_components as dcc
from dash import Dash, dcc, html, Input, Output 
import dash_html_components as html





# ------- Data:  ------- #
avocado = pd.read_csv('/Users/Jan/Desktop/Løst/avocado_updated_2020.csv')

# ------- Create the app:  ------- #
app = dash.Dash()

# ------- Layout:  ------- #
app.layout = html.Div(children=[
    html.H1(children='Avocado Prices Dashboard'),
    dcc.Dropdown(id='geo-dropdown',
                    options=[{'label': i, 'value': i}
                        for i in avocado['geography'].unique()],
                    value='New York'),
    dcc.Graph(id='price-graph')

])

# ------- Callback:  ------- #
@app.callback(
    Output(component_id='price-graph',component_property='figure'),
    Input(component_id='geo-dropdown',component_property='value')
)
def update_graph(selected_geography):
    filtered_avocado = avocado[avocado['geography'] == selected_geography]
    line_fig = px.line(filtered_avocado,
                        x = 'date', y = 'average_price',
                        color='type',
                        title = f'Avocado Prices in {selected_geography}')
    return line_fig

# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)

########################### OWN VERSION: ###########################

# ------- Data:  ------- #
testdf = Select_components_historical(ticker_list = ['FLS.CO'])



testdf = testdf[ticker].stack().reset_index()
testdf = testdf.rename(columns={testdf.columns[2]: 'Closing Price'})



# ------- Create the app:  ------- #
# Create the app:
app = dash.Dash()

# ------- Layout:  ------- #
app.layout = html.Div([

    html.H1("Stocks", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_ticker",
                 options=[
                     {"label": "FLS.CO", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])

# ------- Callback:  ------- #
@app.callback(
    Output(component_id='price-graph',component_property='figure'),
    Input(component_id='geo-dropdown',component_property='value')
)
def update_graph(selected_geography):
    filtered_avocado = avocado[avocado['geography'] == selected_geography]
    line_fig = px.line(filtered_avocado,
                        x = 'date', y = 'average_price',
                        color='type',
                        title = f'Avocado Prices in {selected_geography}')
    return line_fig

# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)