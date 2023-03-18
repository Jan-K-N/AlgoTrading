def MACD(ticker = 'FLS'):
    #df = Select_components_historical(ticker_list=ticker_list)
    df = download_data(ticker=ticker)
    #df_dict={}
    # Insert data. Our object is of type dict, so we must use df[][]
    #for i in ticker_list:
    df['EMA12'] = df.Close.ewm(span = 12).mean()
    df['EMA26'] = df.Close.ewm(span = 26).mean()
    df['MACD'] = df.EMA12 - df.EMA26
    df['signal'] = df.MACD.ewm(span = 9).mean()
    
    #df.update(df)
    
    return df

MACD()

def MACD_strategy(ticker = 'FLS', transaction_costs = 0.1):
    
    """
    
    Output:
    Returns: A series with return from each trade.
    
    
    """
    
    
    # Make containers: #
    dfReturns = []
    Buy,Sell = [], []
    iAvgProfit = []
    profitsrel = []

    df = MACD(ticker = ticker)
    
    # Strategy:
    for i in range(2,len(df)): # We are excluding the two first rows. Therefore, starting the loop at 2.
        if df.MACD.iloc[i] > df.signal.iloc[i] and df.MACD.iloc[i-1] < df.signal.iloc[i-1]:
            Buy.append(i) # Get the row number, where the buying condition is fullfilled.
        elif df.MACD.iloc[i] < df.signal.iloc[i] and df.MACD.iloc[i-1] > df.signal.iloc[i-1]: # Smaller and not the day before.
            Sell.append(i)
    # Backtest:
    Realbuys = [i + 1 for i in Buy]
    Realsells = [i + 1 for i in Sell]
    
    Buyprices = df[['Date','Open']].iloc[Realbuys]
    Sellprices = df[['Date','Open']].iloc[Realsells]
    
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
    # Store in lOut:
    lOut = {'Buy prices':Buyprices,
            'Sellprices':Sellprices,
            'Returns':profitsrel,
            'Average profit':iAvgProfit}
    return lOut


test = MACD_strategy(ticker = 'TSLA',transaction_costs=0)['Buy prices']
test['Date'] == '2022-11-28 00:00:00'

def find_MACD_signal(ticker = None, market = None, tdelta = 0):
    """
    The purpose of this function is to find out, if there is a recent MACD buying signal for a given ticker/market.
    
    Inputs:
        tdelta: Number of days we wish to go back to see, if there has been a trading signal.
    
    """
    # Load some modules:
    from datetime import datetime
    from datetime import timedelta
    
    # Call the MACD_strategy function:
    if market != None:
        # Call exchange_components function.
        tickers = exchange_components(market = market)
        
        # Get the date:
        d = datetime.now().date() - timedelta(tdelta)
        d_final = str(d) + " " + "00:00:00"
        # Now loop over the tickers:
        for ticker in tickers:
            MACD = MACD_strategy(ticker = ticker)#['Buy prices']
            
        
        
        
        
        
    
    

 
plt.plot(test)
