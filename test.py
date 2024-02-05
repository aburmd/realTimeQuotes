import alignUTCTime
import realQuote
import getStored
import getTypeConvertor as conv
import getFormatConvertor as frmt
import getAuth as auth
import os
import json
import sys

from mailjet_rest import Client as mail
import emailContent
api_val=auth.getAPIKey('jet')
api_token=auth.getSecret('jet')
mail_trigger=False
env=os.environ['en']
stock=sys.argv[1]
trendChk=getStored.fileReader('trend',stock)
if trendChk[0]=='':
    Trend=os.environ['Trend']
else:
    trendChkDict=json.loads(trendChk[0])
    Trend=trendChkDict['trend']
print("Enter timeZone in the below format US/Eastern,America/Los_Angeles")
#tmz=input()
tmz='America/Los_Angeles'
res=alignUTCTime.getPreferTZDate(tmz)
startdate=res.strftime("%Y-%m-%d")
enddate=res.strftime("%Y-%m-%d")
typ='tiingo'
headers = {'Content-Type': 'application/json'}
dataOutput=realQuote.getQuote1(startdate,enddate,typ,stock)
#This data(dataOutput) is available in list, it gets stored in a file.
getStored.fileWriter(dataOutput,'store',stock)
print("Verify Current Time")
print("Current Time with timezone is {} and {}".format(res.strftime("%H:%M"),tmz))
print("verify {} mins candle price for the stock {}".format(30,stock))
priceList=getStored.fileReader('store',stock)
print("price gets stored in dictionary with key as candle interval \n")
print(" and value as actual record,here it gets stored as {} {} interval".format(30,'Min'))
priceDict={}
actualTime=str(res.strftime("%H:%M"))
queryTime=alignUTCTime.round_down_to_nearest_30_minutes(actualTime)
for e in priceList:
    if e=='':
        continue
    elementHashMap=conv.convStrToHashMap(e)
    date_UTC=alignUTCTime.convSTDDateTime(elementHashMap['date'])
    date_EST=alignUTCTime.getPreferTZDate(tmz,date_UTC)
    key=str(date_EST.strftime("%H:%M"))
    elementHashMap['date']=str(date_EST.strftime('%Y-%m-%d %H:%M'))
    if tmz=='US/Eastern':
        elementHashMap['tz']='EST'
    elif tmz=='America/Los_Angeles':
        elementHashMap['tz']='PST'
    else:
        elementHashMap['tz']='UTC'
    priceDict[key]=elementHashMap
#print(priceDict)
print("The Current Time is {} {}".format(actualTime,priceDict[queryTime]['tz']))
print("The corresponding queryTime is {} {}".format(queryTime,priceDict[queryTime]['tz']))
print("Actual Value is {}".format(priceDict[queryTime]))
if Trend=="up":
    if priceDict[queryTime]['open'] > priceDict[queryTime]['close']:
        print('T')
        print(Trend)
        mail_trigger=True
        email_message=emailContent.data
        email_message['Messages'][0]['To'][0]['Email']='seng'
        email_message['Messages'][0]['To'][0]['Name']='Ab'
        head='Trend Reversal for {}'.format(stock.upper()) + '-' + 'Red(Possibly going down)' + '-' + "Executed From {} Machine".format(env)
        email_message['Messages'][0]['Subject'] = head
        body="Mail Trggered - Recent observations in the {} candle, showing an opening at {} and a closing at {}, suggest a possible trend reversal".format(stock.upper(),priceDict[queryTime]['open'],priceDict[queryTime]['close'])
        email_message['Messages'][0]['HTMLPart'] = '<h3> '+ body +'<\h3>'
        email_message['Messages'][0]['To'][0]['Email']+='s87@gmail.com'
else:
    if priceDict[queryTime]['open'] < priceDict[queryTime]['close']:
        print('F')
        print(Trend)
        mail_trigger=True
        email_message=emailContent.data
        email_message['Messages'][0]['To'][0]['Email']='seng'
        email_message['Messages'][0]['To'][0]['Name']='Ab' 
        head='Trend Reversal for {}'.format(stock.upper()) + '-' + 'Green(Possibly going up)' + '-' + "Executed From {} Machine".format(env)
        email_message['Messages'][0]['Subject'] = head
        body="Mail Trggered - Recent observations in the {} candle, showing an opening at {} and a closing at {}, suggest a possible trend reversal".format(stock.upper(),priceDict[queryTime]['open'],priceDict[queryTime]['close'])
        email_message['Messages'][0]['HTMLPart'] = '<h3> '+ body +'<\h3>'
        email_message['Messages'][0]['To'][0]['Email']+='s87@gmail.com'
           
if mail_trigger:
    if Trend=="up":
        print("success")
        getStored.fileWriter([{'trend':'down'}],'trend',stock)
        print("Job Executed with mail Trigger - Reversal occur and going to {} trend".format('down'))
    else:
        getStored.fileWriter([{'trend':'up'}],'trend',stock)
        print("Job Executed with mail Trigger - Reversal occur and going to {} trend".format('up'))
    mailjet = mail(auth=(api_val, api_token), version='v3.1')
    result = mailjet.send.create(data=email_message)
    print(body)
else:
    print("Job Executed with mail Not Triggered - Continue with {} trend".format(Trend))
