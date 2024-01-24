import os
import schedule
import time
import pytz

env=os.environ['en']

def job():
    print("Job executed at:", time.strftime("%Y-%m-%d %H:%M:%S"))
    if env=='local':
        os.system("/usr/bin/python3 /Users/abuhura/Desktop/desktop_19thSep2023/Training/workspace/realTimeQuotes/test.py &")
    else:
        os.system("/usr/bin/python3 /home/ec2-user/workspace/realTimeQuotes/test.py &")
        
# Set the time zone to Eastern Time (ET)
eastern_timezone = pytz.timezone('US/Eastern')

# Schedule the job to run every 0th and 30th minute between 9 am to 5 pm
for hour in range(9, 18):  # 9 am to 5 pm
    schedule.every().hour.at(f"{hour:02d}:00").do(job)
    schedule.every().hour.at(f"{hour:02d}:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)