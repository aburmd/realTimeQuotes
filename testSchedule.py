from schedule import every, repeat, run_pending
import time
from mailjet_rest import Client as mail
import getAuth as auth
import emailContent

api_val=auth.getAPIKey('jet')
api_token=auth.getSecret('jet')

@repeat(every(1).minutes)
def job():
    mail_trigger=True
    if mail_trigger:
        mailjet = mail(auth=(api_val, api_token), version='v3.1')
        email_message=emailContent.data
        email_message['Messages'][0]['HTMLPart']+='</br>'+'Test'
        result = mailjet.send.create(data=email_message)
        print(result)
    print("Job is running...")

while True:
    run_pending()
    time.sleep(1)