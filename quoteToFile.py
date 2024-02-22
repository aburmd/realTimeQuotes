import os
import requestStockQuote as quote
import getStored as store
import coreLogic as core
import constructEmail as email
import getFormatConvertor as frmt
import alignUTCTime
import sys

def quoteStore(stock,duration):
    tz=os.environ['tz']
    date=alignUTCTime.getPreferTZDate(frmt.timeZoneDict[tz]).strftime("%Y-%m-%d")
    apitype='tiingo'
    durationType='min'
    # Request the stock price
    resT=quote.getQuote(apitype,stock,date,duration,durationType)
    fileName=stock+'_'+duration+durationType
    #fileName=stock
    filetype='data'
    # Store the stock price list in amzn_2024-02-07_30min.txt
    resp=store.writeToFile(fileName,filetype,resT)
    return resp

def quoteStoreIndex(stock,duration):
    tz=os.environ['tz']
    date=alignUTCTime.getPreferTZDate(frmt.timeZoneDict[tz]).strftime("%Y-%m-%d")
    apitype='twData'
    durationType='min'
    # Request the stock price
    resT=quote.getQuote(apitype,stock,date,duration,durationType)
    fileName=stock+'_'+duration+durationType
    #fileName=stock
    filetype='data'
    # Store the stock price list in amzn_2024-02-07_30min.txt
    resp=store.writeToFile(fileName,filetype,resT)
    return resp