import os
import requestStockQuote as quote
import getStored as store
import coreLogic as core
import constructEmail as email
import getTypeConvertor as conv
import sys

def mainE(stock,duration):
    durationType='min'
    filetype='store'
    fileName=stock+'_'+duration+durationType
    resT=store.readFromFile(fileName,filetype)
    res=[]
    for e in resT:
        if e=='':
            continue
        elementHashMap=conv.convStrToHashMap(e)
        res.append(elementHashMap)
    print(res)
    #identify current Trend
    trend,isAlerted=core.currentTrend(stock)
    isAlerted=False if isAlerted=='F' else True
    alert=core.reverseCandle(stock,res,trend,isAlerted)
    res='Fail'
    if alert:
        newtrend='up' if trend=='down' else 'down'
        mailType=email.constEmailDetails(newtrend,stock)
        data=email.constructMail(mailType,'alert')
        email.sendMail(data)
        metaDataConst={}
        metaDataConst['trend']='up' if trend=='down' else 'down'
        metaDataConst['alert']='T'
        metaDataConst['stock']=stock
        metaDataConst['5']='start'
        metaDataConst['30']='stop'
        store.writeToFile(stock,'metaData',[metaDataConst])
        res='Success'
    return res