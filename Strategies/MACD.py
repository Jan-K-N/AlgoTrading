def MACD(ticker_list = ['FLS.CO','TRYG.CO']):
    df = Select_components_historical(ticker_list=ticker_list)
    df_dict={}
    # Insert data. Our object is of type dict, so we must use df[][]
    for i in ticker_list:
        df[i]['EMA12'] = df[i].Close.ewm(span = 12).mean()
        df[i]['EMA26'] = df[i].Close.ewm(span = 26).mean()
        df[i]['MACD'] = df[i].EMA12 - df[i].EMA26
        df[i]['signal'] = df[i].MACD.ewm(span = 9).mean()
        
        df_dict.update(df)
    
    return df_dict


def MACD_strategy(ticker_list = ['FLS.CO']):
    # Make containers: #
    dfReturns = []
    Buy,Sell = [], []
    iAvgProfit = []
    profitsrel = []
    lOut = []

    df = MACD(ticker_list = ticker_list)
    
    # Strategy:
    counter = 0 
    for ticker in df.keys():
        for i in range(2,len(df[ticker])): # We are excluding the two first rows.
            if df[ticker]['MACD'].iloc[i] > df[ticker]['signal'].iloc[i] and df[ticker]['MACD'].iloc[i-1] < df[ticker]['signal'].iloc[i-1]:
                Buy.append(i) # Get the row number, where the buying condition is fullfilled.
            elif df[ticker]['MACD'].iloc[i] < df[ticker]['signal'].iloc[i] and df[ticker]['MACD'].iloc[i-1] > df[ticker]['signal'].iloc[i-1]:
                Sell.append(i)
        # Backtest: #
        Realbuys = [i+1 for i in Buy]
        Realsells = [i+1 for i in Sell]
        # The prices:
        Buyprices = df[ticker][['Date','Open']].iloc[Realbuys]
        Sellprices = df[ticker][['Date','Open']].iloc[Realsells]
        # Omit case, where the first point is a selling point:
        if Sellprices.index[0] < Buyprices.index[0]:
            Sellprices = Sellprices.drop(Sellprices.index[0])
        elif Buyprices.index[-1] > Sellprices.index[-1]:
            Buyprices = Buyprices.drop(Buyprices.index[-1])
        # Compute the return of the strategy:
        
        for i in range(len(Sellprices)):
            profitsrel.append((Sellprices['Open'].iloc[i]- Buyprices['Open'].iloc[i])/Buyprices['Open'].iloc[i])
        # Average profit:
        iAvgProfit = sum(profitsrel)/len(profitsrel)
    # Store in lOut:
    lOut =  Buyprices,Sellprices
    return lOut
