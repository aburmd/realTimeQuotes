'''
This library helps to convert a format of a data from rare format to commonly 
used format such hours,mins as hh:min.
'''
import datetime
from pytz import timezone

'''
datetime library is widely used for datetime values. Hence, converting any values to datetime objects,
gives more options to utilize further
'''

def getHoursMin(millsec):
    dt=datetime.datetime.fromtimestamp(millsec / 1000.0, tz=datetime.timezone.utc)
    return dt.strftime("%H:%M")

def getCurHoursMin():
    now_pst = datetime.datetime.now()
    pacific= timezone('US/Pacific')
    eastern = timezone('US/Eastern')
    dt1 = pacific.localize(now_pst, is_dst=True)
    est_dt=dt1.astimezone(eastern)
    return est_dt.strftime("%H:%M") 

def getCurHoursMinPST():
    now_pst = datetime.datetime.now()
    return now_pst.strftime("%H:%M") 

def getCurDate():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def currentCandle(s):
    tm=s.split(":")
    if int(tm[1])<30:
        return tm[0]+':'+'00'
    else:
        return tm[0]+':'+'30'