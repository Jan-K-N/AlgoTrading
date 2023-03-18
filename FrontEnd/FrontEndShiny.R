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

##############################################################################   
######################## New FrontEnd:######################################## 
##############################################################################

############ R-preface:
# This preface will mainly be concered with loading various databases from SQLLITE:
CallDatabase <- function(sData = NULL, start = "01-14-2021"){
  
  ## -- Basic setup -- ##
  start = as.Date(start, format =  "%m-%d-%Y")
  dates <- seq(as.Date(start), Sys.Date(), by = 'days')
  
  mDates = matrix(data = NA, nrow = length(dates), ncol = 25 )
  lOut = list()
  arrayOut = array(data = NA, dim = c(2,dim(mDates)[1],25))

  if(sData == 'C25'){
    
    ## -- MACD algo -- ##
    con <- dbConnect(RSQLite::SQLite(), "/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading/Data/Database/DatabaseMACDBuy.db")
    
    alldat <- lapply(setNames(nm = dbListTables(con)), dbReadTable, conn = con) # Get all database input in one enviroment.
    
    # Setup of the alldat list:
    for(i in 1:length(alldat)){
      # Remove the index column: 
      alldat[[i]] = alldat[[i]][,-c(1)]
      # Format to class date:
      alldat[[i]][,1] = as.Date(c(alldat[[i]][,1]), format = "%m-%d-%Y" )
      # Extract the relevant dates:
      alldat[[i]] = alldat[[i]][-c(1:which.closest(c(alldat[[i]][,1]), as.Date(start))),] # Let the series begin from the date closest to start.
      

      
    }
    
    for(myDate in as.character(dates)){
      for(j in 1:dim(mDates)[1]){
        for(j1 in 1:25){
          if(isTRUE(myDate == alldat[[j1]][j,1])){
            # arrayOut[1,,j1] = alldat[[j1]][j,2]
            # arrayOut[2,,j1] = myDate
            mDates[j,j1] = alldat[[j1]][j,1]
            mDates[j,j1] = as.Date(mDates[j,j1],format =  "%m-%d-%Y", origin = start)
            #lOut[[j1]] = arrayOut  
            #print(myDate)
          }
          # else{
          #   mDates[j,j1] = 0
          }
          
        }
      #}
      #cat(myDate, " ")
    }
    
    
    
    
  }else if(sData == 'S&P500'){
    
    
  }else if(sData == 'MACD sell'){

    
    
    
  }
  
  # Return statement:
  return(alldat)
  
}

test = CallDatabase(sData = 'C25')



test[[1]][,1] = as.Date(c(test[[1]][,1]), format = "%m-%d-%Y" )
start = as.Date(start, format =  "%m-%d-%Y")
test[[1]]= test[[1]][-c(1:which.closest(c(test[[1]][,1]), as.Date(start,format = "%m-%d-%Y"))),]



############ 1.0: User interface.
ui <- fluidPage(
  
  titlePanel("AlgoTrader"),
  selectInput("Market", label = "Market", choices = c("C25")),
  
  # Range input:
  # dateRangeInput('dataRange',
  #                label = 'Filter stock dates',
  #                start = as.Date('2020-06-01'), end = as.Date('2020-10-01')),
  
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
    
    if(input$datset == 'C25'){
      alldatdf = as.data.frame(alldat[input$dataset])
      
    }
    
    
    

    
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

for (myDate in as.character(dates)){
  for(i in 1:length(alldat)){
    if(myDate == alldat[[i]][,1]){
      print(myDate)
    }
  }
 
} 


















