import alignUTCTime
import realQuote
import getStored
import getTypeConvertor as conv
import getFormatConvertor as frmt
import getAuth as auth

from mailjet_rest import Client as mail
import emailContent
api_val=auth.getAPIKey('jet')
api_token=auth.getSecret('jet')
mail_trigger=False

print("Enter timeZone in the below format US/Eastern,America/Los_Angeles")
#tmz=input()
tmz='America/Los_Angeles'
res=alignUTCTime.getPreferTZDate(tmz)
#print("enter startdate,endDate and tiingo for getting stock quote")
#print("1.enter startdate: ")
startdate=res.strftime("%Y-%m-%d")
#print("2.enter endDate: ")
enddate=res.strftime("%Y-%m-%d")
#print("3.enter tiingo: ")
#typ=input()
typ='tiingo'
#print("3.enter stock symbol: ")
#stock=input()
stock='qqq'
headers = {'Content-Type': 'application/json'}
#print(realQuote.getQuote(startdate,enddate,typ))
dataOutput=realQuote.getQuote1(startdate,enddate,typ,stock)
#This data is available in list, it gets stored in a file.
getStored.fileWriter(dataOutput)
print("Verify Current Time")
print("Current Time with timezone is {} and {}".format(res.strftime("%H:%M"),tmz))
print("verify {} mins candle price for the stock {}".format(30,stock))
priceList=getStored.fileReader()
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
print(priceDict)
print("The Current Time is {} {}".format(actualTime,priceDict[queryTime]['tz']))
print("The corresponding queryTime is {} {}".format(queryTime,priceDict[queryTime]['tz']))
print("Actual Value is {}".format(priceDict[queryTime]))

if priceDict[queryTime]['close'] < priceDict[queryTime]['open']:
    mail_trigger=True
if mail_trigger:
    mailjet = mail(auth=(api_val, api_token), version='v3.1')
    email_message=emailContent.data
    email_message['Messages'][0]['HTMLPart']+='</br>'+ "At {} {}, QQQ Current 30mins candle {} closes lesser than with open value {}".format(actualTime,priceDict[queryTime]['tz'],priceDict[queryTime]['close'],priceDict[queryTime]['open'])
    result = mailjet.send.create(data=email_message)
    print("Mail Trggered with message as QQQ Current 30mins candle {} closes lesser than with open value {}".format(priceDict[queryTime]['close'],priceDict[queryTime]['open']))

print("Job Executed")