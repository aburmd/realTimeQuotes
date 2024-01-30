
from mailjet_rest import Client as mail
import getAuth as auth
import emailContent
import getFormatConvertor as formater
import alignUTCTime
import schedule
from datetime import datetime
import time

api_val=auth.getAPIKey('jet')
api_token=auth.getSecret('jet')
res=alignUTCTime.getPreferTZDate('US/Eastern')

def job():
    global job_executed
    if not job_executed:
        mailjet = mail(auth=(api_val, api_token), version='v3.1')
        email_message=emailContent.data
        email_message['Messages'][0]['Subject']='Reg - Delete Instance to avoid being overcharged'
        email_message['Messages'][0]['HTMLPart']='Only 5 mins for 1hour run - Can Terminate the EC2'
        result = mailjet.send.create(data=email_message)
        job_executed = True

schedule.every().hour.at(":55").do(job)
# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
    
    # Check if the job has executed, and reset the variable
    if job_executed:
        job_executed = False

print("Job Executed")