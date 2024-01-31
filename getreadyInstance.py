import schedule
import time
from datetime import datetime
import addInstance
import os

def job():
    addInstance.create()
    

# Schedule the job
if os.environ['en']=='local':
    schedule.every().monday.at("12:35").do(job)
    schedule.every().tuesday.at("03:33").do(job)
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