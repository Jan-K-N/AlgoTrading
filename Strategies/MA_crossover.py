## ---- Import functions ## ----
import matplotlib.pyplot as plt
from AlgoTrading.Data.Data1 import Stocks_closing_price
import datetime as dt
plt.style.use("dark_background")  # Here we add a style to our plots.

def MA_crossover(vStockList,
                 start = dt.datetime.now() - dt.timedelta(days = 365 *3),
                 end = dt.datetime.now(),
                 ma_1 = 30,
                 ma_2 = 100,
                 iColum = 0,
                 strat_plot = False):

    ## ---- References ## ----
    # https://www.youtube.com/watch?v=FEDBsbTFG1o

    ## ---- Inputs explained ## ----
    # start: This is the start time-stamp to consider.
    # end: The end time-stamp to consider.
    # ma_1: Length of the shortes moving average.
    # ma_2: Length of the longets moving average.
    # iColum = 0: Adjusted closing price will be used.
    # strat_plot: Boolean variable indicating if a plot of the strategy should be produced or not. Default is "False".

    ## ---- Setup ## ----
    buy_signals = []
    sell_signals = []
    trigger = 0  # Without this, we cannot notice changes.

    ## ---- Get data ## ----
    data = Stocks_closing_price(vStockList,start = start, end = end, iColum = iColum)

    if iColum == 0:
        data[f'SMA_{ma_1}'] = data['Adj Close'].rolling(window=ma_1).mean()
        data[f'SMA_{ma_2}'] = data['Adj Close'].rolling(window=ma_2).mean()
    else:
        data[f'SMA_{ma_1}'] = data[iColum].rolling(window=ma_1).mean()
        data[f'SMA_{ma_2}'] = data[iColum].rolling(window=ma_2).mean()

    data = data.iloc[ma_2:]  # Let the data begin from ma_2

    for x in range(len(data)):
        # First we implement the buy signal:
        if data[f'SMA_{ma_1}'].iloc[x] > data[f'SMA_{ma_2}'].iloc[x] and trigger != 1:
            buy_signals.append(data['Adj Close'].iloc[x])
            sell_signals.append(float('nan'))
            trigger = 1
        elif data[f'SMA_{ma_1}'].iloc[x] < data[f'SMA_{ma_2}'].iloc[x] and trigger != -1:
            buy_signals.append(float('nan'))
            sell_signals.append(data['Adj Close'].iloc[x])
            trigger = -1
        else:
            buy_signals.append(float('nan'))
            sell_signals.append(float('nan'))

    data['Buy Signals'] = buy_signals
    data['Sell Signals'] = sell_signals

    if strat_plot == True:
        plt.plot(data['Adj Close'], label="Share Price", alpha=0.5)
        plt.plot(data[f'SMA_{ma_1}'], label=f"SMA_{ma_1}", color="orange", linestyle="--")
        plt.plot(data[f'SMA_{ma_2}'], label=f"SMA_{ma_2}", color="pink", linestyle="--")
        plt.scatter(data.index, data['Buy Signals'], label="Buy Signal", marker="^", color="#00ff00", lw=3)
        plt.scatter(data.index, data['Sell Signals'], label="Sell Signal", marker="v", color="#ff0000", lw=3)
        plt.legend(loc="upper left")

    return print(data,
                 plt.show)
