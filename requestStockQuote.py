import getAuth as auth
import requests
import getTypeConvertor as conv
from polygon import RESTClient as SQ
import getFormatConvertor as frmt
import os
headers = {'Content-Type': 'application/json'}

def getQuoteTiingo(api,stock,stdate,enddate,duration,durationtype):
        apiVal=api
        startDate=stdate
        endDate=enddate
        url='https://api.tiingo.com/iex/{}/prices?startDate={}&endDate={}&resampleFreq={}{}&columns=open,high,low,close,volume&token={}'.format(stock,startDate,endDate,duration,durationtype,apiVal)
        #url='https://api.tiingo.com/tiingo/funds/{}?token=4fbd748b05ea85b5d9cf97c69aabbcd31d58bdf9
        requestResponse = requests.get(url, headers=headers)
        res=requestResponse.json()
        print("tiingo API provides {} items for the stock {}".format(len(res),stock))
        return res

def getQuotePoly(api,stock,stdate,enddate,duration,durationtype):
        apiVal=api
        sqClient=SQ(api_key=apiVal)
        startDate=stdate
        endDate=enddate
        resBytes = conv.convHTTPResponseToByte(sqClient.get_aggs(stock,duration,durationtype,startDate,endDate,raw=True,))
        res=conv.convByteToDict(resBytes.data)
        print("poly API provides {} items for the stock {}".format(len(res),stock))
        return res

def getQuoteTWData(api,stock,stdate,enddate,duration,durationtype):
        apiVal=api
        startDate=stdate+' 09:00:00'
        endDate=frmt.getPreferTZDate('Asia/Calcutta').strftime('%Y-%m-%d %H:%M:%S')
        url='https://api.twelvedata.com/time_series?apikey={}&start_date={}&end_date={}&interval={}{}&symbol={}&format=JSON&prepost=True'.format(apiVal,startDate,endDate,duration,durationtype,stock)
        print(url)
        requestResponse = requests.get(url, headers=headers)
        res=requestResponse.json()['values']
        print("12data API provides {} items for the index {}".format(len(res),stock))
        return res

def getQuote(apitype,stock,date,duration,durationtype):
        '''
        When comparing the dataset, 
        please note that the Tiingo and Poly APIs will match based on date and time except for the volume. 
        The volume in Tiingo represents IEX volume, while in Poly, it indicates total volume. 
        Please use these values appropriately.
        '''
        apiVal=''
        res=''
        startDate=date
        endDate=date
        if apitype=='tiingo':
                apiVal=auth.getAPIKey('tiingo')
                resp=getQuoteTiingo(apiVal,stock,startDate,endDate,duration,durationtype)
                res=frmt.stdResponse('tiingo',resp)
        if apitype=='poly':
                apiVal=auth.getAPIKey('poly')
                stock=stock.upper()
                duration=int(duration)
                durationtype="minute" if durationtype=='min' else durationtype
                resp=getQuotePoly(apiVal,stock,startDate,endDate,duration,durationtype)
                res=frmt.stdResponse('poly',resp['results'])
        if apitype=='twData':
                apiVal=auth.getAPIKey('twData')
                stock=stock.upper()
                resp=getQuoteTWData(apiVal,stock,startDate,endDate,duration,durationtype)
                res=frmt.stdResponse('twData',resp,duration)                
        return res