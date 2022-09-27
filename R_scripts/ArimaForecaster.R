###### Function for ARIMA(p,I,q) forecasting ####### 
library(forecast)
library("RSQLite")
library(XLConnect)
library(xlsx)
#library(reticulate) # By this we can talk with python.
library(assertive.base)
library(reshape2)
library(data.table)
library(tseries)

for_errors <- function(y,yhat){
  ehat <- tail(y, n = length(yhat))  - yhat   # tail specifies that we want the n last obs in the vector
  mse <- ((1/length(ehat)*(sum(ehat^2)))^0.5)
  mae <- (1/length(ehat)*sum(abs(ehat)))
  
  list.out <- list(
    "ehat" = ehat ,
    "msfe" = mse ,
    "mae" = mae
  )
  return(list.out)
}


forecast_arima <- function(sTicker = NULL, df = NULL, w_size = 200, start = "2019-01-15",h = 1,
                           maxp = 1, maxq = 1){
  
  ## Description of the function ##
  # This function will fit a (optimal) simple arima(p,I,q) model. 
  # This includes various cyclical components. After this, 
  # forecasts will be performed and saved in a vector.
  
  ## Inputs ##
  # sTicker: Time-series to be forecasted. Usually a series with closing prices.
  # w_size: Window size to fit the initial model.
  
  if(is.null(df)){
    ## Download data from database: ##
    con <- dbConnect(RSQLite::SQLite(), "/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading/Data/Database/Database.db")
    
    # Build the query to get the data:
    str1 = 'SELECT'
    str2 = '*'
    str3 = 'FROM'
    str4 = parenthesize(
      sTicker,
      type = "square_brackets")
    query = paste(str1,str2,str3,str4,sep=" ")
    
    res <- dbSendQuery(con,query)
    mData =  as.data.frame(dbFetch(res)[,c(1,6)])
  
    # Extract relevant dates:
    mData[,1] = as.Date(mData[,1], format = "%Y-%m-%d")
    #mData = mData[-c(1:which(mData$Date == paste(start,'00:00:00', sep = " "))),]
    mData = mData[-c(1:(which(mData[,1] == start))-1),]
    rownames(mData) <- 1:nrow(mData) # Adjust rownames.
  }
  # else{
    # if(dim(df)[2] == 2){
    #   mData = df
    #   # Extract relevant dates:
    #   #mData = mData[-c(1:which(mData[,1] == paste(start,'00:00:00', sep = " "))),]
    #   mData = mData[-c(1:which(mData[,1] == start)),]
    #   rownames(mData) <- 1:nrow(mData) # Adjust rownames.
    # }
    #else{
      df = as.data.frame(df)
      mData = df[,c(1,6)]
      mData[,1] = as.Date(mData[,1], format = "%Y-%m-%d")
      # Extract relevant dates:
      #mData = mData[-c(1:which(mData[,1] == paste(start,'00:00:00', sep = " "))),]
      mData = mData[-c(1:which(mData[,1] == start)),]
      rownames(mData) <- 1:nrow(mData) # Adjust rownames.
    # }


  #}
  

  
  ##--- Setup: ---##
  nModels = maxp * maxq
  T         = dim(mData)[1]
  iEval     = (T - w_size) # Number of observations left to be forecasted.
  mForecast = (matrix(data = 0, nrow = iEval , ncol = nModels)) # Matrix to store our forecasts in later.
  iTrain    = w_size
  lFit     = list()
  lForecast = list()
  #vErrors = matrix(data = NA, nrow = 1, ncol = nModels)
  vErrors = array(data = NA, dim = c(1,nModels,3))
    # [,,1] Will be the actual errors.
    # [,,2] p order.
    # [,,3] q order.
  ##--- Algo begin: ---##
    # Steps: Make this approach iterative, i.e., repeat the rutine each time a new observation becomes available.
      # 1: Fit the model on training data.
        # Use IC.
      # 2: Forecast using the model selected in 1.
      # 3: Compute errors.
      # 4: Select the model with the smallest errors.
      # 5: Compute actual out-of-sample forecasts.
  
  mCombi = expand.grid(seq(1:maxp),seq(1:maxq))
  for(i in 1:(iEval)){
    for(j in 1:nModels){
        ## 1: Fit the models:
        p = mCombi[j,1]
        q = mCombi[j,2]
        
        if(adf.test(mData[,2])$p.value > 0.05){
          lFit[[j]] = Arima(mData[1:(iTrain + (i) - 1), 2], order = c(p,1,q),
                            optim.control = list(maxit = 8000))
          # lFit[[j]] = auto.arima(mData[1:(iTrain + (i) - 1), 2])
        }else{
              
          lFit[[j]] = Arima(mData[1:(iTrain + (i) - 1), 2], order = c(p,0,q),
                            optim.control = list(maxit = 8000))
          # lFit[[j]] = auto.arima(mData[1:(iTrain + (i) - 1), 2])
        }
        
        ## 2: Forecasts and store the forecasts:
        lForecast[[j]]    = forecast(lFit[[j]],h=h)
        mForecast[i,j] = as.matrix(lForecast[[j]]$mean)[h,]  

        }
  }
  
  ## 3: Compute errors.
  for(j in 1:nModels){
    vErrors[1,j,1] = for_errors(mData[,2],mForecast[,j])$mae
    vErrors[1,j,2] = mCombi[j,1]
    vErrors[1,j,3] = mCombi[j,2]
  }
  
  ## 4: Select the model with the smallest errors.
  iMin = which.min(vErrors[,,1])
  finalp = vErrors[1,iMin,2]
  finalq = vErrors[1,iMin,3]
  
  ## 5: Compute actual out-of-sample forecasts.
  fitfinal = Arima(mData[,2], order = c(finalp,1,finalq),optim.control = list(maxit = 8000))
  forecastfinal = forecast(fitfinal, h = h)
  #plotfinal = plot(forecastfinal)
  
  # Return:
  lOut = list("ForecastObject" = forecastfinal,
              "Forecast" = forecastfinal$mean)
  return(lOut)
  
}         

test = forecast_arima(df = FLStest[,c(1,6)], h = 6)
test = forecast_arima(sTicker = 'AMBU-B.CO', h = 6)
test[["Forecast"]]

dim(FLStest[,c(1,6)])[2]
