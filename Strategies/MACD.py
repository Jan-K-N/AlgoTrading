def MACD_strategy(ticker_list = ['FLS.CO']):
    # Make containers: #
    #dfReturns = pd.DataFrame(index=range(2),columns=range(1))
    dfReturns = []
    Buy,Sell = [], []
    iAvgProfit = []
    profitsrel = []

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
    return iAvgProfit

# Example of usage:
test = MACD_strategy(ticker_list = ['FLS.CO'])
test

# Example of usage:
ticker_list2 = ['FLS.CO','TRYG.CO','DANSKE.CO','JYSK.CO']
for ticker in ticker_list2:
    MACD_strategy([ticker])*100 