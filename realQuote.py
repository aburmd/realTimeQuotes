from polygon import RESTClient as SQ
import getAuth as auth
import getTypeConvertor as conv
import getFormatConvertor as formater
import random

api_val=auth.getAPIKey('poly')
sqClient=SQ(api_key=api_val)

def getQuote(startdate,enddate):
    '''
    Enter start and end date with YYYY-MM-DD format for getting aggregated quotes
    response stored as bytes
    '''
    resBytes = conv.convHTTPResponseToByte(sqClient.get_aggs("QQQ",30,"minute",startdate,enddate,raw=True,))
    res=conv.convByteToDict(resBytes.data)
    return res


def defaultQuoteGenerator(quotes):
    for i in range(24):
        key1='0'+str(i)+':'+'00'
        key2='0'+str(i)+':'+'30'
        quotes[key1]=random.choice([['101.01','100.01']])
        quotes[key2]=random.choice([['101.01','100.01']])
    return quotes
    
def storeQuotes(args,quotes):
    quotes=defaultQuoteGenerator(quotes)
    outPut=args
    for element in outPut:
        if element=='':
            continue
        elementHashMap=conv.convStrToHashMap(element)
        print(type(elementHashMap))
        print(elementHashMap)
        print(type(elementHashMap['t']))
        print(elementHashMap['t'])
        tm=formater.getHoursMin(elementHashMap['t'])
        quotes[tm]=[elementHashMap['o'],elementHashMap['c']]
    return quotes
    