####### MACD front-end function: #######

# ------ Description of the function ------#
# The goal of this function is allow the user to give a dateRangeinput. The 
# dateRangeInput should be given as the last 30 days or something like that. The function, 
# should then report if there has been any buying or selling signals for that period.

MACD_FrontEnd <- function(sTicker = NULL, df = NULL, start = '09-27-2022'){
  require(assertive.base)
  require(birk)
  
  ## --- Data setup --- ##
    
    if(is.null(sTicker)){
      # Since no ticker is given, we download data from the whole market:
      
      
    }
  
    ## Download data from database: ##
    con <- dbConnect(RSQLite::SQLite(), "/Users/Jan/Desktop/Programmering/Stocks_algo/AlgoTrading/Data/Database/DatabaseMACDBuy.db")
    
    # Build the query to get the data:
    str1 = 'SELECT'
    str2 = '*'
    str3 = 'FROM'
    str4 = parenthesize(
      sTicker,
      type = "square_brackets")
    query = paste(str1,str2,str3,str4,sep=" ")
    
    res <- dbSendQuery(con,query)
    mData =  as.data.frame(dbFetch(res))
    # Remove the index column:
    mData = mData[,-1]
  
    # Extract relevant dates and do the relevant formatting:
    mData[,1] = as.Date(mData[,1], format = "%m-%d-%Y")
    mData = mData[-c(1:which.closest(c(mData[,1]), as.Date(start))),] # Let mData begin from the date closest to the start value.
    rownames(mData) <- 1:nrow(mData) # Adjust rownames.
    



  
  return(mData)
  
}
