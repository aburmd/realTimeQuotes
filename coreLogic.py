import getStored as store
import os
import json
import pandas as pd
import ast

def currentTrend(fileName):
    Trend=''
    trendChk=store.readFromFile(fileName,'metaData')
    trendChkDict=json.loads(trendChk[0])
    Trend=trendChkDict['trend']
    Alert=trendChkDict['alert']
    return [Trend,Alert]

def checkFiveMinTrigger(stock):
    status=False
    trendChk=store.readFromFile(stock,'metaData')
    trendChkDict=json.loads(trendChk[0])
    status=True if trendChkDict['5']=='start' else False
    print('Received a 5mins Candle trigger as {}'.format(trendChkDict['5']))
    return status

def check30MinTrigger(stock):
    status=False
    trendChk=store.readFromFile(stock,'metaData')
    trendChkDict=json.loads(trendChk[0])
    status=True if trendChkDict['30']=='start' else False
    print('Received a 30mins Candle trigger as {}'.format(trendChkDict['30']))
    return status


def reverseCandle(stock,quoteList,trend,isAlerted):
    if not isAlerted:
        if not len(quoteList)>0:
            return False
        res=quoteList[-1]
        op=res['open']
        cl=res['close']
        alert=True if (trend=='up' and op > cl) or (trend=='down' and cl > op) else False
        return alert
    return False

def load_txt_to_dataframe(file_path):
    with open(file_path, 'r') as file:
        # Read lines and convert each line to a dictionary
        dict_list = [ast.literal_eval(line) for line in file]
    
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(dict_list)
    return df
