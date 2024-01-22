'''
This library helps to convert a format of a data from rare format to commonly 
used format such hours,mins as hh:min.
'''
import datetime
from pytz import timezone
from datetime import timedelta
import os

'''
datetime library is widely used for datetime values. Hence, converting any values to datetime objects,
gives more options to utilize further
'''
env=os.environ['en']
def getHoursMin(millsec):
    dt=datetime.datetime.fromtimestamp(millsec / 1000.0, tz=datetime.timezone.utc)
    return dt.strftime("%H:%M")

def getCurHoursMin():
    pacific= timezone('US/Pacific')
    eastern = timezone('US/Eastern')
    if env=='local':
        now_pst = datetime.datetime.now()
        dt1 = pacific.localize(now_pst, is_dst=True)
        est_dt=dt1.astimezone(eastern)
    else:
        now_utc = datetime.datetime.now()
        est_dt=now_utc.astimezone(eastern)
    return est_dt.strftime("%H:%M")
 

def getCurHoursMinPST():
    pacific= timezone('US/Pacific')
    now_pst = datetime.datetime.now()
    if env!='local':
        now_pst=now_pst.astimezone(pacific)
    return now_pst.strftime("%H:%M")

def getCurDate():
    pacific= timezone('US/Pacific')
    now_pst = datetime.datetime.now()
    if env!='local':
        now_pst=now_pst.astimezone(pacific)
    return now_pst.strftime("%Y-%m-%d")

def currentCandle(s):
    tm=s.split(":")
    if int(tm[1])<30:
        return tm[0]+':'+'00'
    else:
        return tm[0]+':'+'30'
    
def getDate():
    tm = getCurHoursMin()
    res=tm.split(":")
    is_yesterday=False
    if int(res[0]) <= 9 and int(res[1]) < 30:
        is_yesterday=True
    presentday=datetime.datetime.now()
    res=presentday
    if is_yesterday:
        yesterday = presentday - timedelta(1)
        if yesterday.isoweekday()==7:
            res = presentday - timedelta(3)
        elif yesterday.isoweekday()==6:
            res = presentday - timedelta(2)
        else:
            res=yesterday
    return res.strftime("%Y-%m-%d")
    