##########################################################################################################################################################
######################################################################################## Frontend lol: ############################################
##########################################################################################################################################################
###### Function for ARIMA(p,I,q) forecasting ####### 
library(forecast)
library("RSQLite")
#library(XLConnect)
#library(xlsx)
#library(reticulate) # By this we can talk with python.
library(assertive.base)
library(reshape2)
library(data.table)
library(tseries)
library(dplyr)
library(ggplot2)

# Shiny
library(shiny)
library(bslib)

# Modelling:
library(modeldata)
library(DataExplorer)

# Widgets:
library(plotly)

# Core:
library(tidyverse)


## Download data from database: ##
con <- dbConnect(RSQLite::SQLite(), "/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading/Data/Database/Database.db")

alldat <- lapply(setNames(nm = dbListTables(con)), dbReadTable, conn = con) # Get all database input in one enviroment.

# Convert all dates to class data:
for(i in 1:(length(alldat)-1)){
  alldat[[i]][,1] = as.Date(alldat[[i]][,1], format = "%Y-%m-%d")
}


############ 1.0: User interface.
ui <- fluidPage(
  
  titlePanel("AlgoTrader"),
  selectInput("dataset", label = "Ticker", choices = names(alldat)),
  
  # Range input:
  dateRangeInput('dataRange',
                 label = 'Filter stock dates',
                 start = as.Date('2020-06-01'), end = as.Date('2020-10-01')),
  
  dateInput('dataRange1',
                 label = 'Filter stock dates',
                 start = as.Date('2020-06-01')),
  
  column(6,
         dataTableOutput('my_table')
  ),
  column(8,
         plotOutput("plot"))


)

############ 2.0: Server.
# Here we run actual R-code.
server <- function(input,output,session){

#-------------------- R-code body --------------------#
  
# Convert to dataframe. This is done in a reactive enviroment:
  data <- reactive({
  
    alldatdf = as.data.frame(alldat[input$dataset])
    
    # Convert date colum to class date:
    alldatdf[,1] = as.Date(alldatdf[,1], format = "%Y-%m-%d")
    alldatdf_DAT = alldatdf[,1]
    
    lOut = list("alldatdf" = alldatdf,
                "alldatdf_DAT" = alldatdf_DAT)
    # Specify what to return:
    return(lOut)
    
  })
  
# We now make a function which returns the filtered data in a dataframe:
  alldatdfFiltered <- reactive({
    alldatdfFiltereddf <-  data()[["alldatdf"]] %>% dplyr::filter(data()[["alldatdf_DAT"]] >= input$dataRange[1] & data()[["alldatdf_DAT"]] <= input$dataRange[2])
    
    return(alldatdfFiltereddf)
  })
  
  alldatdfFiltered1 <- reactive({
    alldatdfFiltereddf1 <-  data()[["alldatdf"]] %>% dplyr::filter(data()[["alldatdf_DAT"]] >= input$dataRange1[1])
    
    return(alldatdfFiltereddf1)
  })
  
  
# Plot:
  ###### The below works! ###### 
                          # forecastplot <- reactive({
                          #   f = forecast_arima(sTicker = input$dataset, maxp = 1, maxq = 1, h =5)[["Forecast"]]
                          #   return(f)
                          # })
  
  ###### The below works! ###### 
                          # df2 <- reactive({
                          #   alldatdfFiltered()
                          #   return(df2)
                          # })

  ###### The below is in progress! ###### 
                forecastplot <- reactive({
                  
                  # Call Filter function 1:
                  k <- alldatdfFiltered1()
                  f = forecast_arima(sTicker = NULL, df = k, maxp = 1, maxq = 1, h = 3, start = input$dataRange1[1])[["Forecast"]]
                  return(f)
                })

#-------------------- Output: --------------------#  

  output$my_table <- renderDataTable({
    alldatdfFiltered() #[c(1,6)]

  })
  
  ###### The below works! ######
                                    output$plot <- renderPlot({
                                      plot(forecastplot(), type = "l")
                                    })


}
shinyApp(ui,server)





######### lol




data <- function(){
  alldatdf = as.data.frame(alldat[input$dataset])
  
  # Convert date colum to class date:
  alldatdf[,1] = as.Date(alldatdf[,1], format = "%Y-%m-%d")
  alldatdf_DAT = alldatdf[,1]
  
  lOut = list("alldatdf" = alldatdf,
              "alldatdf_DAT" = alldatdf_DAT)
  # Specify what to return:
  return(lOut)
}
  

  



























