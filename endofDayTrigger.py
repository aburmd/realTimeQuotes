import schedule
import time
import datetime
import os
import pytz
import alignUTCTime
import quoteToFile as q
import sys
import coreLogic as core
import main5 as m5
import emailContent
from mailjet_rest import Client as mail
import getAuth as auth

api_val=auth.getAPIKey('jet')
api_token=auth.getSecret('jet')

# Variable to track whether the job has executed
job_executed = False
env=os.environ['en']
stock=sys.argv[1]

def job():
    global job_executed
    if not job_executed:
        prefer_timezone = alignUTCTime.getPreferTZDate('US/Eastern')
        localTimeHour=prefer_timezone.strftime("%H")
        localTimeMin=prefer_timezone.strftime("%M")
        localTimeZone=alignUTCTime.timeZoneFinder(prefer_timezone.strftime("%z"))
        print("Local time is {}:{} {}".format(localTimeHour,localTimeMin,localTimeZone))
        q.quoteStoreIndex(stock,'1')
        job_executed = True
        email_message=emailContent.data
        head='EndofDay Trigger {}'.format(stock.upper()) + '-' + "Executed From {} Machine".format(env)
        email_message['Messages'][0]['Subject'] = head
        body="Temp set-up - login to verify for {} price as market close in 15 mins".format(stock.upper())
        email_message['Messages'][0]['HTMLPart'] = '<h3> '+ body +'<\h3>'
        mailjet = mail(auth=(api_val, api_token), version='v3.1')
        result = mailjet.send.create(data=email_message)
        print(body)

# Schedule the job to run every 0th and 30th minute between 9 am to 5 pm

schedule.every().day.at("12:45").do(job)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
    
    # Check if the job has executed, and reset the variable
    if job_executed:
        job_executed = False      