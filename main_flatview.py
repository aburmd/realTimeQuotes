def currentCandle(s):
    tm=s.split(":")
    if int(tm[1])<30:
        return tm[0]+':'+'00'
    else:
        return tm[0]+':'+'30'

def previousCandle(s):
    tm=currentCandle(s)
    tm=s.split(":")
    if tm[1]=='30':
        return tm[0]+':'+'00'
    else:
        val=str(int(tm[0])-1)
        if len(val)==1:
            val='0'+val
        return val+':'+'30'

import json
import random
from polygon import RESTClient as SQ
from urllib3 import HTTPResponse
from typing import cast
import datetime
from mailjet_rest import Client as mail
import os
sqClient=SQ(api_key='vubKg43HwaEXAfS6tDyrYlegAewlaJJM')
aggs = cast(HTTPResponse,sqClient.get_aggs("QQQ",30,"minute","2024-01-19","2024-01-20",raw=True,),)
#get results in byte as type
my_bytes_value=aggs.data
#converting byte into str
my_json = my_bytes_value.decode('utf8').replace("'", '"')
#converting str into dict
data = json.loads(my_json)
#converting dict into json
s = json.dumps(data, indent=4, sort_keys=True)
#return the results as list.. to crossverify check the first element in an array
data['results'][0]
import datetime
#time_in_millis = 1596542285000
time_in_millis = data['results'][0]['t']
res={}
for a in data['results']:
    tm=datetime.datetime.fromtimestamp(a['t'] / 1000.0, tz=datetime.timezone.utc).strftime("%H:%M")
    if tm not in res:
        res[tm]=[a['o'],a['c']]
    else:
        res[tm].append([a['o'],a['c']])
        
for i in range(1,9):
    key1='0'+str(i)+':'+'00'
    key2='0'+str(i)+':'+'30'
    res[key1]=random.choice(list(res.values()))
    res[key2]=random.choice(list(res.values()))
   
time_now=datetime.datetime.now().strftime("%H:%M") 
cur_val=res[currentCandle(time_now)]

mail_trigger=False
if cur_val[1] < cur_val[0]:
    mail_trigger=True

API_KEY = os.environ['ussr']
API_SECRET = os.environ['test']

data = {
  'Messages': [
    {
      "From": {
        "Email": "aburmd@gmail.com",
        "Name": "Me"
      },
      "To": [
        {
          "Email": "abudigitalworld@gmail.com",
          "Name": "You"
        }
      ],
      "Subject": "QQQ 30mins Candle is Red!",
      "TextPart": "Greetings from Mailjet!",
      "HTMLPart": "<h3>Dear Abu, Please monitor 5 mins chart and take action accordingly <a href=\"https://www.mailjet.com/\">Mailjet</a>!</h3><br />May the delivery force be with you!"
    }
  ]
}

data = {
  'Messages': [
    {
      "From": {
        "Email": "aburmd@gmail.com",
        "Name": "Me"
      },
      "To": [
        {
          "Email": "@gmail.com",
          "Name": "You"
        }
      ],
      "Subject": "QQQ 30mins Candle is Red!",
      "TextPart": "Greetings from Mailjet!",
      "HTMLPart": "<h3>Dear Abu, Please monitor 5 mins chart and take action accordingly <a href=\"https://www.mailjet.com/\">Mailjet</a>!</h3><br />May the delivery force be with you!"
    }
  ]
}

 


if mail_trigger:
    mailjet = mail(auth=(API_KEY, API_SECRET), version='v3.1')
    result = mailjet.send.create(data=data)
    print(result)
    


'''
ref: 
how to convert bytes to dict, dict to json
https://stackoverflow.com/questions/40059654/convert-a-bytes-array-into-json-format
how to get real-time aggregate data
https://polygon-api-client.readthedocs.io/en/latest/Getting-Started.html

export ussr=''
export test=''
'''