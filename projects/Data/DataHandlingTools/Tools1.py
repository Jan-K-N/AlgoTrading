# Start by loading some packages:
import matplotlib.pyplot as plt
#%matplotlib inline
import yfinance as yf
import numpy as np
import seaborn as sns

data = yf.download(['AAPL'], start="2020-02-21")
data2 = yf.download(['TSLA'], start="2020-02-21")

data.head()
data2.head()



data['Adj Close'].plot()
plt.show()



######## Functions ########

#### Function 1: Correlation between tickers:
    
      
def series_corr(ticker_list=['AAPL','TSLA'],start = "2020-02-21",par="Adj Close", pct_changes = False):
    """
    
    Inputs:
    ----------
    ticker_list: TYPE, optional
        DESCRIPTION. The default is ['AAPL','TSLA'].
    start: TYPE, optional
        DESCRIPTION. The default is "2020-02-21".
    par: TYPE, optional
        Parameter to set the column of the ticker to be inspected. The default is Open. Possible values are: "Open","Close"...
    pct_changes: TYPE, optional
        DESCRIPTION. The default is False.

    
    The function returns the correlation matrix. When pct_changes is set to "True", the function returns the correlation matrix as percentage changes.
    -------
    corr_data : TYPE
        DESCRIPTION.

    """
            
    #### Download data:
    
    # Set up pandas dataframe:
    data = pd.DataFrame(columns=ticker_list)
    # Retrive the data from our database:
    for ticker in ticker_list:
        data[ticker] = download_data(ticker = ticker, start = start)[par]
  
    
    if pct_changes:
        corr_data = data.pct_change().corr(method = "pearson")
    else:
        corr_data = data.corr(method = "pearson")
        
    # Tell the function what to return. 
    return corr_data

series_corr()

#### Function 2: Correlation between tickers above certain threshold:
test = series_corr(ticker_list=["DPZ", "AAPL", "GOOG", "AMD", "GME", "SPY", "NFLX", "BA", "WMT","TWTR","GS","XOM","NKE","FEYE", "FB","BRK-B", "MSFT"],
                   par = "Adj Close")

def series_corr_threshold(corr=test,thres = 0.9):
    #### Inputs:
    # corr: pd which is the correlation matrix.
    
    #### Helper functions:
    
    # Find the correlations above a certain threshold:
    corr = corr.mask(np.triu(np.ones(corr.shape)).astype(bool)).stack() # Stack the corr matrix, so that we remove duplicates.
    corr = corr[(corr>thres)]
    
    return print(corr.index)
    

testfunction = series_corr_threshold(thres = 0.95)
testfunction 

# Let's investigate MSFT and GOOG:
    
##### Trading strategy:


#### Function 3: Compute return of a stock
def returns(ticker = 'FLS',start = None, ):
    """
    Insert description here.
    """
    
    # Start by downloading the data from the database:
    data = download_data(ticker = ticker, start = None)
    
    
    
    



