import datetime
import pytz
#from pytz import timezone
#from datetime import timedelta
import os

'''
tiingo response file contains data in UTC, we need to align with local and compare the data and time. 
This library bring this alignment.To maintain the standards, we try to keep all date/time in UTC 
and convert only when it reaches to end-users.
'''

def getPreferTZDate(tmzone,datevalue=None):
    '''Pick anyone from the list of timeZone and pass it on to get the prefer timezone dateTime
       US/Eastern,America/Los_Angeles '''
    # Get the current UTC time  
    utc_val = datetime.datetime.utcnow() - datetime.timedelta(hours=0, minutes=0)
    if datevalue:
        utc_val=datevalue
    # Find the prefer timezone
    prefer_timezone = pytz.timezone(tmzone)
    # Convert UTC time to prefer time
    prefer_timezone_val = utc_val.replace(tzinfo=pytz.utc).astimezone(prefer_timezone)
    # Print the local time and timezone
    #print("Time:", prefer_timezone_val.strftime('%Y-%m-%d %H:%M:%S'))
    #print("Timezone:", prefer_timezone_val)
    return prefer_timezone_val

def convSTDDateTime(date_string,format='%Y-%m-%dT%H:%M:%S.%fZ'):
    '''
    Please refer the format input and apply the format in string. 
    refer: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    For tiingo, '%Y-%m-%dT%H:%M:%S.%fZ'
    '''
    dt = datetime.datetime.strptime(date_string, format)
    return dt

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

def round_down_to_nearest_30_minutes(time_str):
    dt = datetime.datetime.strptime(time_str, "%H:%M")
    base_time = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 0, 0)
    rounded_time = base_time + datetime.timedelta(minutes=(dt.minute // 30) * 30)
    rounded_time_30 = rounded_time - datetime.timedelta(minutes=30)
    rounded_time_str = rounded_time_30.strftime("%H:%M")
    return rounded_time_str

def round_down_to_nearest_30_minutes1(time_str,*arg):
    mn=30
    if len(arg)>0:
        mn=int(arg[0])
    dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    base_time = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 0, 0)
    rounded_time = base_time + datetime.timedelta(minutes=(dt.minute // mn) * mn)
    rounded_time_30 = rounded_time - datetime.timedelta(minutes=mn)
    rounded_time_str = rounded_time_30.strftime("%Y-%m-%d %H:%M")
    return rounded_time_str

def timeZoneFinder(s):
    dct={'-0800':'PST','-0500':'EST','+0000':'UTC'}
    if s in dct:
        return dct[s]
    return s