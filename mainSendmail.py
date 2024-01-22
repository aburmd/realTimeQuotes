
from mailjet_rest import Client as mail
import getAuth as auth
import emailContent
import realQuote
import getFormatConvertor as formater

api_val=auth.getAPIKey('jet')
api_token=auth.getSecret('jet')
mail_trigger=False

file = open(auth.file_path,'r')
res=file.read()
data=res.split("\n")

quotes=realQuote.defaultQuoteGenerator({})
quotes=realQuote.storeQuotes(data,quotes)
cur_val=quotes[formater.currentCandle(formater.getCurHoursMin())]

if cur_val[1] < cur_val[0]:
    mail_trigger=True
print(cur_val)
if mail_trigger:
    mailjet = mail(auth=(api_val, api_token), version='v3.1')
    email_message=emailContent.data
    email_message['Messages'][0]['HTMLPart']+='</br>'+' Previous Close:'+ str(cur_val[0])+' Current Close:'+ str(cur_val[1]) + ' at '+ formater.getCurHoursMinPST()+ 'PST'
    result = mailjet.send.create(data=email_message)
    print(result)