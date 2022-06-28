#### Function to download and return closing price. Possibility to insert in path. ####

# Load packages:
import yfinance as yf

# Define the function:
def Stocks_closing_price(vStockList, start, end):
    ## Inputs: ##
    # vStockList: String vector with ticker codes to be searched for.
    # start: Start period to be considered.
    # end: End period to be considered.

    ## Start the function: ##
    mData = yf.download(vStockList, start = start, end = end)

    # Specify what to return:
    return mData
