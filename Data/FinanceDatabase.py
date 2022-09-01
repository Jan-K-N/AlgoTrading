# Reference: https://www.youtube.com/watch?v=5bUn-D4eL4k&t=0s
# Load packages:
import sqlalchemy
import pandas as pd

###############################################################################
# DATABASE
###############################################################################
import sqlite3
import yfinance as yf
import pandas as pd
from openpyxl import load_workbook
import yahoo_fin.stock_info as si # Use this to scrape ticker lists. Can only be used for popular exchanges, however. http://theautomatic.net/yahoo_fin-documentation/

## Setup of database: ##
connDatabase = sqlite3.connect('/Users/Jan/Desktop/Løst/Programmering/Stocks_algo/AlgoTrading/Data/Database/Database.db') # Create a db file with a connection.
#connDatabase = sqlite3.connect(':memory:') # Fresh database.
cDatabase = connDatabase.cursor()

## Helper functions: ##
def exchange_components(tickers):
    # Purpose of function: Download tickers and store them in the database.
    # Loop over the tickers:
    for ticker in tickers:
        mStock = yf.download(ticker)
        #mStock = mStock.assign(Exchange = market)
        mStock.to_sql(ticker,connDatabase,if_exists='replace')

def Select_components(ticker_list=C25_tickers, Sheet_name='Sheet'):
    # Description of this function: #
    # The function will download the tickers, given as input, and extract the lastest adj.closing prices.
    # Finally, these will be stored/reported in our front-end excel document.

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

            df2.to_excel("/Users/Jan/Desktop/Løst/Programmering/Stocks_algo/AlgoTrading/FrontEnd/AlgoFrontEnd.xlsx",
                         sheet_name=Sheet_name,
                         startrow=0,
                         startcol=0,
                         index=False)

#### Download data:

## C25:
C25df = yf.download("^OMXC25")
C25df.to_sql('C25', connDatabase,if_exists='replace')
connDatabase.commit()

## Components of C25:

# Define tickers:
C25_tickers = ['ROCK-B.CO','GMAB.CO','NDA-DK.CO','CHR.CO','ISS.CO','RBREW.CO',
               'DEMANT.CO','MAERSK-B.CO','CARL-B.CO','BAVA.CO','VWS.CO','NZYM-B.CO',
               'NOVO-B.CO','DANSKE.CO','MAERSK-A.CO','DSV.CO','TRYG.CO','PNDORA.CO',
               'NETC.CO','JYSK.CO','COLO-B.CO','FLS.CO','GN.CO','AMBU-B.CO','ORSTED.CO']

exchange_components(tickers = C25_tickers)


## S&P500:
SP500df = yf.download("^GSPC")
SP500df.to_sql('S&P500', connDatabase,if_exists='replace')
connDatabase.commit()