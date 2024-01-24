from polygon import RESTClient as SQ
import getAuth as auth
import getTypeConvertor as conv
import getFormatConvertor as formater
import random
import requests

headers = {'Content-Type': 'application/json'}

def getQuote(startdate,enddate,typ):
    '''
    Enter start and end date with YYYY-MM-DD format for getting aggregated quotes
    response stored as bytes
    '''
    res=''
    if typ=='poly':
        api_val=auth.getAPIKey('poly')
        sqClient=SQ(api_key=api_val)
        stock='QQQ'
        resBytes = conv.convHTTPResponseToByte(sqClient.get_aggs("QQQ",30,"minute",startdate,enddate,raw=True,))
        res=conv.convByteToDict(resBytes.data)
    elif typ=='tiingo':
        api_val=auth.getAPIKey('tiingo')
        '''Try to pass the data after converting local to UTC date as startDate'''
        startDate=startdate
        stock='qqq'
        url='https://api.tiingo.com/iex/{}/prices?startDate={}&resampleFreq=30min&columns=open,high,low,close,volume&token={}'.format(stock,startDate,api_val)
        print(url)
        requestResponse = requests.get(url, headers=headers)
        res=requestResponse.json()
        print("tiingo API provides {} items for the stock {}".format(len(res),stock))
    return res

def getQuote1(startdate,enddate,typ,stock):
    '''
    Enter start and end date with YYYY-MM-DD format for getting aggregated quotes
    response stored as bytes
    '''
    res=''
    if typ=='poly':
        api_val=auth.getAPIKey('poly')
        sqClient=SQ(api_key=api_val)
        stock=stock.upper()
        resBytes = conv.convHTTPResponseToByte(sqClient.get_aggs("QQQ",30,"minute",startdate,enddate,raw=True,))
        res=conv.convByteToDict(resBytes.data)
    elif typ=='tiingo':
        api_val=auth.getAPIKey('tiingo')
        '''Try to pass the data after converting local to UTC date as startDate'''
        startDate=startdate
        stock=stock
        url='https://api.tiingo.com/iex/{}/prices?startDate={}&resampleFreq=30min&columns=open,high,low,close,volume&token={}'.format(stock,startDate,api_val)
        print(url)
        requestResponse = requests.get(url, headers=headers)
        res=requestResponse.json()
        print("tiingo API provides {} items for the stock {}".format(len(res),stock))
    return res

def defaultQuoteGenerator(quotes):
    for i in range(24):
        key1='0'+str(i)+':'+'00'
        key2='0'+str(i)+':'+'30'
        quotes[key1]=random.choice([['101.01','100.01']])
        quotes[key2]=random.choice([['101.01','100.01']])
    return quotes
    
def storeQuotes(args,quotes,typ):
    quotes=defaultQuoteGenerator(quotes)
    outPut=args
    if typ=='poly':
        for element in outPut:
            if element=='':
                continue
            elementHashMap=conv.convStrToHashMap(element)
            tm=formater.getHoursMin(elementHashMap['t'])
            quotes[tm]=[elementHashMap['o'],elementHashMap['c']]
    elif typ=='tiingo':
        for element in outPut:
            if element=='':
                continue
            elementHashMap=conv.convStrToHashMap(element)
            tm=formater.getHoursMin(elementHashMap['date'],'tiingo')
            quotes[tm]=[elementHashMap['open'],elementHashMap['close']]
    return quotes

def storeQuotes1(args,quotes,typ,key):
    outPut=args
    if typ=='poly':
        for element in outPut:
            if element=='':
                continue
            elementHashMap=conv.convStrToHashMap(element)
            tm=formater.getHoursMin(elementHashMap['t'])
            quotes[tm]=[elementHashMap['o'],elementHashMap['c']]
    elif typ=='tiingo':
        for element in args:
            if element=='':
                continue
            elementHashMap=conv.convStrToHashMap(element)
            quotes[key]=elementHashMap
    return quotes
