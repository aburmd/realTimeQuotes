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
tmz=os.environ['tmz']
def getHoursMin(date_string,typ):
    if typ=='tiingo':
        dt = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        dt=datetime.datetime.fromtimestamp(date_string / 1000.0, tz=datetime.timezone.utc)
        pacific= timezone('US/Pacific')
        dt=dt.astimezone(pacific)
    return dt.strftime("%H:%M")

def getCurHoursMin():
    pacific= timezone('US/Pacific')
    eastern = timezone('US/Eastern')
    if (tmz == 'local' or tmz == 'pst'):
        now_pst = datetime.datetime.now()
        est_dt = pacific.localize(now_pst, is_dst=True)
        #est_dt=est_dt.astimezone(eastern)
    else:
        now_utc = datetime.datetime.now()
        est_dt=now_utc.astimezone(eastern)
        print("current time in est is {}".format(est_dt))
    return est_dt.strftime("%H:%M")
 

def getCurHoursMinPST():
    pacific= timezone('US/Pacific')
    now_pst = datetime.datetime.now()
    if not (tmz == 'local' or tmz == 'pst'):
        now_pst=now_pst.astimezone(pacific)
    return now_pst.strftime("%H:%M")

def getCurDate():
    pacific= timezone('US/Pacific')
    now_pst = datetime.datetime.now()
    if not (tmz == 'local' or tmz == 'pst'):
        now_pst=now_pst.astimezone(pacific)
    return now_pst.strftime("%Y-%m-%d")

def currentCandle(s):
    tm=s.split(":")
    if int(tm[1])<30:
        if int(tm[0])==0:
            tm[0]='23'
        else:
            tm[0]= str(int(tm[0])-1) if len(str(int(tm[0])-1))==2 else '0'+str(int(tm[0])-1)
        return tm[0]+':'+'00'
    else:
        return tm[0]+':'+'00'
    
def getDate():
    tm = getCurHoursMin()
    res=tm.split(":")
    is_yesterday=False
    if (int(res[0]) <= 1 and int(res[1]) < 30) or (int(res[0]) >= 20):
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
    