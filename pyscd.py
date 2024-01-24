import os
import schedule
import time

env=os.environ['en']

def job():
    print("Job executed at:", time.strftime("%Y-%m-%d %H:%M:%S"))
    if env=='local':
        os.system("/usr/bin/python3 /Users/abuhura/Desktop/desktop_19thSep2023/Training/workspace/realTimeQuotes/mainRealQuotes.py &")
        os.system("/usr/bin/python3 /Users/abuhura/Desktop/desktop_19thSep2023/Training/workspace/realTimeQuotes/mainSendmail.py &")
    else:
        os.system("/usr/bin/python3 /home/ec2-user/workspace/realTimeQuotes/mainRealQuotes.py &")
        os.system("/usr/bin/python3 /home/ec2-user/workspace/realTimeQuotes/mainSendmail.py &")
        
schedule.every().hour.at(":00").do(job)
schedule.every().hour.at(":30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)