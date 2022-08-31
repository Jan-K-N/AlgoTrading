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
import yahoo_fin.stock_info as si # Use this to scrape ticker lists. Can only be used for popular exchanges, however.

## Setup of database: ##
connDatabase = sqlite3.connect('/Users/Jan/Desktop/Løst/Programmering/Stocks_algo/AlgoTrading/Data/Database/Database.db') # Create a db file with a connection.
#connDatabase = sqlite3.connect(':memory:') # Fresh database.
cDatabase = connDatabase.cursor()

## Functions: ##
def exchange_components(tickers):
    # Purpose of function: Download tickers and store them in the database.
    # Loop over the tickers:
    for ticker in tickers:
        mStock = yf.download(ticker)
        mStock.to_sql(ticker,connDatabase,if_exists='replace')

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