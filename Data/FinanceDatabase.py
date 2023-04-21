"""
Main Finance Database script.
"""
# Reference: https://www.youtube.com/watch?v=5bUn-D4eL4k&t=0s
# Load packages:
#import sqlalchemy
import pandas as pd
###############################################################################
# DATABASE
###############################################################################
import sqlite3
import yfinance as yf
from openpyxl import load_workbook
from operator import itemgetter

#import yahoo_fin.stock_info as si # Use this to scrape ticker lists. Can only be used for popular exchanges, however. http://theautomatic.net/yahoo_fin-documentation/


## Definition of stuff:
C25_tickers = ['ROCK-B.CO','GMAB.CO','NDA-DK.CO','CHR.CO','ISS.CO','RBREW.CO',
               'DEMANT.CO','MAERSK-B.CO','CARL-B.CO','BAVA.CO','VWS.CO','NZYM-B.CO',
               'NOVO-B.CO','DANSKE.CO','MAERSK-A.CO','DSV.CO','TRYG.CO','PNDORA.CO',
               'NETC.CO','JYSK.CO','COLO-B.CO','FLS.CO','GN.CO','AMBU-B.CO','ORSTED.CO']

## ------------ Helper functions: ------------  ##
def exchange_components(market = "^OMXC25"):
    
    """
    Purpose of function: Download tickers and store them in the database. The function is 
    index based. This means that it will download and store indices instead of single stocks/tickers.
    
    Markets currently supported are: "^OMXC25", "OBX.OL", "^GSPC".
    
    """
        
    # Loop over the tickers:
    if market == "^OMXC25":
        tickers = ['ROCK-B.CO','GMAB.CO','NDA-DK.CO','CHR.CO','ISS.CO','RBREW.CO',
                       'DEMANT.CO','MAERSK-B.CO','CARL-B.CO','BAVA.CO','VWS.CO','NZYM-B.CO',
                       'NOVO-B.CO','DANSKE.CO','MAERSK-A.CO','DSV.CO','TRYG.CO','PNDORA.CO',
                       'NETC.CO','JYSK.CO','COLO-B.CO','FLS.CO','GN.CO','AMBU-B.CO','ORSTED.CO']
        
        #sp_assets = pd.read_html(
                #'https://en.wikipedia.org/wiki/OMX_Copenhagen_25')[0] # FIX THIS LATER, IF YOU WANT TO SCRAPE!

        #tickers = sp_assets['Ticker symbol'].str.replace('.', '-').tolist() # FIX THIS LATER, IF YOU WANT TO SCRAPE!
        
        for ticker in tickers:
                #mStock = yf.download(ticker + ".CO") # FIX THIS LATER, IF YOU WANT TO SCRAPE!
            mStock = yf.download(ticker)
            ## Setup of database: ##
            connDatabase = sqlite3.connect('/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading/Data/Database/Database^OMXC25.db') # Create a db file with a connection.
            #connDatabase = sqlite3.connect(':memory:') # Fresh database.
            cDatabase = connDatabase.cursor()
            
            mStock.to_sql(ticker,connDatabase,if_exists='replace')
    elif market == "OBX.OL":
        tickers = ['AKRBP','EQNR']
        for ticker in tickers:
            mStock = yf.download(ticker)
            ## Setup of database: ##
            connDatabase = sqlite3.connect('/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading/Data/Database/DatabaseOBXOL.db') # Create a db file with a connection.
            #connDatabase = sqlite3.connect(':memory:') # Fresh database.
            cDatabase = connDatabase.cursor()
            
            mStock.to_sql(ticker,connDatabase,if_exists='replace')
    elif market == "^GSPC":
        sp_assets = pd.read_html(
                'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]

        tickers = sp_assets['Symbol'].str.replace('.', '-').tolist()
        for ticker in tickers:
            mStock = yf.download(ticker)
            ## Setup of database: ##
            connDatabase = sqlite3.connect('/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading/Data/Database/Database^GSPC.db') # Create a db file with a connection.
            #connDatabase = sqlite3.connect(':memory:') # Fresh database.
            cDatabase = connDatabase.cursor()
        
            mStock.to_sql(ticker,connDatabase,if_exists='replace')
    
    # Determine what to return:
    return tickers
        
def download_data(ticker = 'FLS', start = None):
    
    """
    
    start: Specifies the start date for the data we want to look at. Should be written in the form 'YYYY-mm-d'
    
    The function returns the ticker/stock data as a pandas dataframe.
    """
    
    # This function should be a modified version of the "Select_components_historical" function.
    
        
    ## Find out which market we are in part 2: ## (Maybe define class for the code below:)
    sp_assets_OMX = pd.read_html(
                'https://en.wikipedia.org/wiki/OMX_Copenhagen_25')[0]

    tickers_OMX = sp_assets_OMX['Ticker symbol'].str.replace('.', '-').tolist()
    
    
    sp_assets_GSPC = pd.read_html(
                'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]

    tickers_GSPC = sp_assets_GSPC['Symbol'].str.replace('.', '-').tolist()
    

    if ticker in tickers_OMX:
        connDatabase = sqlite3.connect('/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading/Data/Database/Database^OMXC25.db')
    elif ticker in tickers_GSPC:
        connDatabase = sqlite3.connect('/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading/Data/Database/Database^GSPC.db')
    
    ## Build query: ##
    query = """SELECT * FROM""" + " " + "[" + ticker + "]"
    query = str(query)
     
        
    df = pd.read_sql_query(query, connDatabase)
    # We have now downloaded the data from our database. Hence, we are ready to do date-adjusting:
    if start is None:
        df = df
    else:
        # We now want to extract only the relevant/specified dates:
        iStart = df.Date[df.Date == start + " " + '00:00:00'].index.tolist()
        iStart = ' '.join([str(elem) for i,elem in enumerate(iStart)])
        iStart = int(iStart)
        df = df.tail(len(df)-iStart)

        # Do some last setup of the df dataframe, before we pass it to stock_list
        df = df.reset_index(drop = True) # Reset the index.
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].dt.strftime('%m-%d-%Y') # Adjust date format.
            
    # Specify what to return:
    return df

for ticker in ['TSLA','DSV']:
    print(download_data(ticker=ticker)[['Date','Adj Close']])
    
#############################################################################################################################

# Below is the new data setup:
import yfinance as yf
import datetime
import pandas as pd

from datetime import date, timedelta


class Database():
        
    end = date.today()
    start = end - timedelta(days=3*365)
    
    end = end.strftime("%Y-%m-%d")
    start = start.strftime("%Y-%m-%d")

    def __init__(self,start=start,end=end):
        self.start = start
        self.end = end
        
    def get_PriceData(start=start,end=end, ticker = 'TSLA'):

        ticker = yf.download(tickers = ticker,start = start, end = end)
        return ticker
    
    def get_DividendData(ticker=ticker,start=start,end=end):
        ticker_info = yf.Ticker(ticker)
        ticker_div = ticker_info.dividends
        
        return ticker_div

    if __name__ == '__main__':
        print('Done')
    
    
#ob = Database()
f = Database.get_DividendData(ticker = 'FLS.CO')
    
class Database_Economic():
    # Code here.
        # Database containing economic variables from FRED etc.



    

        
        

        
    
    
    
    
    
    

