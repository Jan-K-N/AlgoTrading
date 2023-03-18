




### Consider deleting this script!



## ---- Import functions ## ----
from multiprocessing.dummy import Array
import matplotlib.pyplot as plt
from AlgoTrading.Data.FinanceDatabase import Select_components_historical
import datetime as dt
plt.style.use("classic")  # Here we add a style to our plots.

def MA_crossover(ticker_list = 'FLS.CO',
                 start = '2015-01-14',
                 ma_1 = 30,
                 ma_2 = 100,
                 transaction_costs = 0.1):
    ## ---- References ## ----

    ## ---- Inputs explained ## ----
    # ticker_list: Stocks to be considered. Should be of the form: ticker_list = ['ticker']
    # start: This is the start time-stamp to consider.
    # end: The end time-stamp to consider.
    # ma_1: Length of the shortes moving average.
    # ma_2: Length of the longets moving average.
    # iColum = 0: Adjusted closing price will be used.
    # strat_plot: Boolean variable indicating if a plot of the strategy should be produced or not. Default is "False".

    ## ---- Setup ## ----
    lReturn = {}
    profitsrel = []
    Buy,Sell = [], []
    buy_signals = [] # Will contain the actual buying price.
    sell_signals = [] # Will contain the actual selling price. 
    trigger = 0  # Without this, we cannot notice changes.
    iAvgProfit = []
    ## ---- Get data ## ----
    data = Select_components_historical(ticker_list=[ticker_list],start = start)
    data[ticker_list][f'SMA_{ma_1}'] = data[ticker_list]['Adj Close'].rolling(window=ma_1).mean()
    data[ticker_list][f'SMA_{ma_2}'] = data[ticker_list]['Adj Close'].rolling(window=ma_2).mean()
    data[ticker_list] = data[ticker_list].iloc[ma_2:]  # Let the data begin from ma_2
    for x in range(len(data[ticker_list])):
        # First we implement the buy signal:
        if data[ticker_list][f'SMA_{ma_1}'].iloc[x] > data[ticker_list][f'SMA_{ma_2}'].iloc[x] and trigger != 1:
            buy_signals.append(data[ticker_list]['Adj Close'].iloc[x])
            sell_signals.append(float('nan'))
            Buy.append(x) # Row number of buy signal.
            trigger = 1
        elif data[ticker_list][f'SMA_{ma_1}'].iloc[x] < data[ticker_list][f'SMA_{ma_2}'].iloc[x] and trigger != -1:
            buy_signals.append(float('nan'))
            sell_signals.append(data[ticker_list]['Adj Close'].iloc[x])
            Sell.append(x) # Row number of selling signal is appended here.
            trigger = -1
        else:
            buy_signals.append(float('nan'))
            sell_signals.append(float('nan'))
    data[ticker_list]['Buy Signals'] = buy_signals
    data[ticker_list]['Sell Signals'] = sell_signals
    
    # The buy_signals and the sell_signals are the buy and the sell prices. Hence, I can now compute the returns:
    # First, we compute the actual buys (next day after the signal, since we are based on the closing price.)
    Realbuys = [i+1 for i in Buy]
    Realsells = [i+1 for i in Sell]

    Buyprices = data[ticker_list][['Date','Open']].iloc[Realbuys]
    Sellprices = data[ticker_list][['Date','Open']].iloc[Realsells]

    # Omit the case, where the first point is a selling point:
    if Sellprices.index[0] < Buyprices.index[0]:
        Sellprices = Sellprices.drop(Sellprices.index[0])
    elif Buyprices.index[-1] > Sellprices.index[-1]:
        Buyprices = Buyprices.drop(Buyprices.index[-1])
    
    # Compute the return of the strategy:
    for i in range(len(Sellprices)):
        profitsrel.append(((Sellprices['Open'].iloc[i] - Sellprices['Open'].iloc[i]*transaction_costs  ) 
                            - (Buyprices['Open'].iloc[i]) + Sellprices['Open'].iloc[i]*transaction_costs   )/(Buyprices['Open'].iloc[i] + Sellprices['Open'].iloc[i]*transaction_costs  ))
    # Average profit:
    iAvgProfit = sum(profitsrel)/len(profitsrel)
    
    lReturn.update({"Return series":profitsrel})
    lReturn.update({"Average return":iAvgProfit})

    # Make the list to return:
    return print(lReturn)

MA_crossover()

ticker_list = ["FLS.CO","TRYG.CO","GMAB.CO"]

for ticker in ticker_list:
    MA_crossover(ticker)
    
