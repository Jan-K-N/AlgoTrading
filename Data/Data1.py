#### Function to download and return closing price. Possibility to insert in path. ####

# Load packages:
import yfinance as yf
import datetime as dt

# Define the function:
def Stocks_closing_price(vStockList,
                         start = dt.datetime.now() - dt.timedelta(days = 365 *3),
                         end = dt.datetime.now(),
                         iColum = 'Adj Close'):
    ## Inputs: ##
    # vStockList: String vector with ticker codes to be searched for.
    # start: Start period to be considered. Default value is set to the last three years.
    # end: End period to be considered. Default value is set to today.

    ## Start the function: ##
    mData = yf.download(vStockList, start = start, end = end)

    # Specify what to return:
    if iColum == 0:
        return mData
    else:
        return mData[[iColum]]
