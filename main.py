import os

env=os.environ['en']

if env=='local':
    os.system("/usr/bin/python3 /Users/abuhura/Desktop/desktop_19thSep2023/Training/workspace/realTimeQuotes/mainRealQuotes.py &")
    os.system("/usr/bin/python3 /Users/abuhura/Desktop/desktop_19thSep2023/Training/workspace/realTimeQuotes/mainSendmail.py &")
else:
    os.system("/usr/bin/python3 /home/ec2-user/workspace/realTimeQuotes/mainRealQuotes.py &")
    os.system("/usr/bin/python3 /home/ec2-user/workspace/realTimeQuotes/mainSendmail.py &")