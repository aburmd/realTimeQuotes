import schedule
import time
from datetime import datetime
import getInstance
import os

def job():
    instancesList=getInstance.listInstances()
    responseList=[]
    for i in instancesList:
        responseList.append(getInstance.getTerminateInstance(i))
        print("Running EC2 Intance:{} is terminated".format(i))
    print(f"Job executed at: {datetime.now()}")

# Schedule the job
if os.environ['en']=='local':
    schedule.every().monday.at("12:35").do(job)
    schedule.every().tuesday.at("12:35").do(job)
    schedule.every().wednesday.at("12:35").do(job)
    schedule.every().thursday.at("12:35").do(job)
    schedule.every().friday.at("12:35").do(job)
else:
    schedule.every().monday.at("20:35").do(job)
    schedule.every().tuesday.at("20:35").do(job)
    schedule.every().wednesday.at("20:35").do(job)
    schedule.every().thursday.at("20:35").do(job)
    schedule.every().friday.at("20:35").do(job) 
while True:
    schedule.run_pending()
    time.sleep(1)
