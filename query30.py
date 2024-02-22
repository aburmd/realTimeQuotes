import schedule
import time
import datetime
import os
import pytz
import alignUTCTime
import quoteToFile as q
import sys
import main1 as m
import coreLogic as core

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
        if int(localTimeHour) in range(9,16):
            print("Good news! The market is now open, and I'm eager to monitor your stock price. I'll keep you informed if your conditions align positively.")
            res=''
            if core.check30MinTrigger(stock):
                q.quoteStoreIndex(stock,'5')
                res=m.mainE(stock,'5')
            print(res)
        else:
            print("The market has closed. I trust you had a fantastic day of trading!")
        job_executed = True

# Schedule the job to run every 0th and 30th minute between 9 am to 5 pm
schedule.every().hour.at(":00").do(job)
schedule.every().hour.at(":30").do(job)
# Run the scheduler

while True:
    schedule.run_pending()
    time.sleep(1)
    
    # Check if the job has executed, and reset the variable
    if job_executed:
        job_executed = False      