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
        if int(localTimeHour) in range(9,23):
            print("Good news! The market is now open, and I'm eager to monitor your stock price. I'll keep you informed if your conditions align positively.")
            if core.checkFiveMinTrigger(stock):
                q.quoteStoreIndex(stock,'5')
                m5.main5(stock,'30','5')
                
        else:
            print("The market has closed. I trust you had a fantastic day of trading!")
        job_executed = True

# Schedule the job to run every 0th and 30th minute between 9 am to 5 pm

schedule.every().hour.at(":00").do(job)
schedule.every().hour.at(":08").do(job)
schedule.every().hour.at(":10").do(job)
schedule.every().hour.at(":15").do(job)
schedule.every().hour.at(":20").do(job)
schedule.every().hour.at(":25").do(job)
schedule.every().hour.at(":30").do(job)
schedule.every().hour.at(":36").do(job)
schedule.every().hour.at(":37").do(job)
schedule.every().hour.at(":42").do(job)
schedule.every().hour.at(":50").do(job)
schedule.every().hour.at(":55").do(job)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
    
    # Check if the job has executed, and reset the variable
    if job_executed:
        job_executed = False      