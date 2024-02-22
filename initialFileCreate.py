'''
This module will create all necessary files to run the process.

'''
import os
import getStored as store
trend=os.environ['Trend']
stockList=['ndx','qqq']
duration='30'
durationType='min'
def fileCreate(stock):
    os.system("touch ~/Desktop/DataStore/data/{}_{}{}.txt".format(stock,duration,durationType))
    os.system("touch ~/Desktop/DataStore/metadata/{}.txt".format(stock))
    metaDataConst={}
    metaDataConst['trend']=trend
    metaDataConst['alert']='F'
    metaDataConst['stock']=stock
    metaDataConst['5']='stop'
    metaDataConst['30']='start'
    resp=store.writeToFile(stock,'metaData',[metaDataConst])
    return resp

for f in stockList:
    resp=fileCreate(f)
    print(f)
