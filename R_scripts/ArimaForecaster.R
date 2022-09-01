###### Function for ARIMA(p,I,q) forecasting ####### 

vY = read.csv("/Users/Jan/Desktop/LøstFB.csv")
vY = vY[-c(1:700),]
plot(vY[,2],type = "l")

library(forecast)
library("RSQLite")
library(XLConnect)
library(xlsx)

install.packages("openxlsx")
install.packages("data.table")
# Requiring the packages to be used in the code
library(openxlsx)
library(data.table)

con <- dbConnect(RSQLite::SQLite(), "/Users/Jan/Desktop/Løst/Programmering/Stocks_algo/AlgoTrading/Data/Database/Database.db")

res <- dbSendQuery(con,"SELECT * FROM C25 ORDER BY Date DESC LIMIT 1;")
lol = as.data.frame(dbFetch(res)[6])

wb = createWorkbook()

saveWorkbook(wb,"/Users/Jan/Desktop/test2.xlsx", overwrite = TRUE )

writeData(wb,1,lol)

write.xlsx(lol,"/Users/Jan/Desktop/test2.xlsx", sheetName = "Sheet 1",
           startCol = "B",
           startRow = 1)

forecast_arima <- function(vY, w_size = 500){
  
  ## Description of the function ##
  # This function will fit a (optimal) simple arima(p,I,q) model. 
  # This includes various cyclical components. After this, 
  # forecasts will be performed and saved in a vector.
  
  ## Inputs ##
  # vY: Time-series to be forecasted. Usually a series with closing prices.
  # w_size: Window size to fit the initial model.
  
  ## Setup ##
  vY        = as.numeric(vY)
  vForecast = as.numeric() # Vector to store our forecasts in later.
  T         = length(vY[,2])
  iEval     = T - w_size # Number of observations left to be forecasted.
  
  
  
  ## Modelling ##
  lFit = auto.arima(vY[,2],seasonal = TRUE,ic = 'aicc')
  plot(vY[,2], type = "l")
  lines(fitted(lFit), col = "red")
  plot(forecast(lFit, h=1))

    
  lFit = auto.arima(vY[1:(w_size),2])
  vForecast = forecast(lFit, h = 1)$mean

  plot(vY[1:w_size,2], type = 'l')
  points(vForecast)
  lines(vForecast, col = "red")
  
}            
