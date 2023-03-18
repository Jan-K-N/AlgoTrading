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

# Below is old code.






def Select_components(ticker_list=C25_tickers, Sheet_name='Sheet'):
    
    """
    # Description of this function: #
    # The function will download the tickers, given as input, and extract the lastest adj.closing prices.
    # Finally, these will be stored/reported in our front-end excel document.
    """
    


    # Update the SQL-database with the newest data:
    exchange_components(tickers=ticker_list)

    db_list = []
    df2 = pd.DataFrame()
    for db_name in cDatabase.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
        db_list.append(db_name)
    for x in range(0, len(db_list)):
        # We now build the string ticker we want to search for:
        sTicker = str(db_list[x])
        sTicker2 = sTicker.replace("('", '')
        sTicker_final = sTicker2.replace("',)", '')

        if sTicker_final in ticker_list:
            # Build query:
            query = """SELECT * FROM""" + " " + "[" + sTicker_final + "]" + " " + """ORDER BY Date DESC LIMIT 1"""
            query = str(query)
            # Save:
            df = pd.read_sql_query(query, connDatabase)
            df.insert(0, '', sTicker_final)
            iClose = df[df.columns[[0, 6]]]
            df2 = pd.concat([iClose, df2], ignore_index=True)

            df2.to_excel("/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading/FrontEnd/AlgoFrontEnd.xlsx",
                         sheet_name=Sheet_name,
                         startrow=0,
                         startcol=0,
                         index=False)

def Select_components_historical(ticker_list=C25_tickers, start = None):
    
    """
    
    ## Basic description of this function ##
    This function will pull ticker data from our SQL-database.
    
    """
    
    ## Inputs: 
        # ticker_list: This is the tickers, we want to get data about.


    # Update the SQL-database with the newest data:
    exchange_components(tickers=ticker_list)
    # Make some containers:
    db_list=[]
    stock_list={}
    stock_list2_names=[]
    # Open loop:
    for db_name in cDatabase.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
        db_list.append(db_name)
    for x in range(0, len(db_list)):
        # We now build the string ticker we want to search for:
        sTicker = str(db_list[x])
        sTicker2 = sTicker.replace("('", '')
        sTicker_final = sTicker2.replace("',)", '')
        if sTicker_final in ticker_list:
            stock_list2_names.append(sTicker_final)
            # Build query:
            query = """SELECT * FROM""" + " " + "[" + sTicker_final + "]"
            query = str(query)
            # Save:
            df = pd.read_sql_query(query, connDatabase)
            #df.insert(0, '', sTicker_final)
            if start is None:
                # Since no start date is provided to use, we do some 
                # last setup of the df dataframe, before we pass it to stock_list
                df = df.reset_index(drop = True) # Reset the index.
                df['Date'] = pd.to_datetime(df['Date'])
                df['Date'] = df['Date'].dt.strftime('%m-%d-%Y') # Adjust date format.
                # Pass df to stock_list
                stock_list.update({sTicker_final:df})
            else:
                # Extract relevant dates:
                iStart = df.Date[df.Date == start + " " + '00:00:00'].index.tolist()
                iStart = ' '.join([str(elem) for i,elem in enumerate(iStart)])
                iStart = int(iStart)
                df = df.tail(len(df)-iStart)

                # Do some last setup of the df dataframe, before we pass it to stock_list
                df = df.reset_index(drop = True) # Reset the index.
                df['Date'] = pd.to_datetime(df['Date'])
                df['Date'] = df['Date'].dt.strftime('%m-%d-%Y') # Adjust date format.
                # Pass df to stock_list
                stock_list.update({sTicker_final:df})
    # Return:
    return stock_list

def MACD_to_sql(ticker_list = C25_tickers,Buy = None):
    if Buy == True:
        ## Setup of database: ##
        connDatabaseMACD = sqlite3.connect('/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading/Data/Database/DatabaseMACDBuy.db') # Create a db file with a connection.
        #connDatabase = sqlite3.connect(':memory:') # Fresh database.
        cDatabaseMACD = connDatabaseMACD.cursor()
        for ticker in ticker_list:
            pdMACD = MACD_strategy([ticker])[0]
            pdMACD = pd.DataFrame(pdMACD)
            pdMACD.to_sql(str(ticker),connDatabaseMACD, if_exists = 'replace')
            connDatabaseMACD.commit()
    else:
        ## Setup of database: ##
        connDatabaseMACD = sqlite3.connect('/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading/Data/Database/DatabaseMACDSell.db') # Create a db file with a connection.
        #connDatabase = sqlite3.connect(':memory:') # Fresh database.
        cDatabaseMACD = connDatabaseMACD.cursor()
        for ticker in ticker_list:
            pdMACD = MACD_strategy([ticker])[1]
            pdMACD = pd.DataFrame(pdMACD)
            pdMACD.to_sql(str(ticker),connDatabaseMACD, if_exists = 'replace')
            connDatabaseMACD.commit()
    return print("Done")
