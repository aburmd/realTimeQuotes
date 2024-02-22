import coreLogic as core
import getTypeConvertor as conv
import getStored as store
import json
import constructEmail as email
# Example usage
def main5(file_path,bigV,smallV):
    file_path = file_path  # Change this to your text file's path
    Htrend=core.currentTrend(file_path)[0]
    file5=file_path+'_'+smallV+'min'
    file30=file_path+'_'+bigV+'min'
    resT30=store.readFromFile(file30,'store')
    res30=[]
    maxDate=''
    for e in resT30:
        if e=='':
            continue
        elementHashMap=conv.convStrToHashMap(e)
        maxDate=max(maxDate,elementHashMap['date'])
        res30.append(elementHashMap)
    print(maxDate)
    resT5=store.readFromFile(file5,'store')
    res5=[]
    for e in resT5:
        if e=='':
            continue
        elementHashMap=conv.convStrToHashMap(e)
        if elementHashMap['date']<maxDate:
            continue
        res5.append(elementHashMap)
    sorted_list = sorted(res5, key=lambda x: x['date'])
    if Htrend=='down':
        ll=float(sorted_list[0]['low'])
        lldate=sorted_list[0]['date']
        h=float(sorted_list[0]['high'])
        hdate=sorted_list[0]['date']
        lh=float(sorted_list[0]['high'])
        lhdate=sorted_list[0]['date']
        islhUpdateReq=True
        isLIgnore,isHIgnore=False,False
        for i in range(1,len(sorted_list)):
            if h<float(sorted_list[i]['high']):
                h,hdate=float(sorted_list[i]['high']),sorted_list[i]['date']
            if ll>=float(sorted_list[i]['low']):
                ll,lldate=float(sorted_list[i]['low']),sorted_list[i]['date']
                if isLIgnore:
                    isLIgnore=False
                if isHIgnore:
                    isHIgnore=False
            else:
                if not isHIgnore:
                    if islhUpdateReq:
                        lh,lhdate=float(sorted_list[i]['high']),sorted_list[i]['date']
                    else:
                        if lh <= float(sorted_list[i]['high']):
                            lh,lhdate=float(sorted_list[i]['high']),sorted_list[i]['date']
                        else:
                            isLIgnore=False
                            isHIgnore=False
                        isHIgnore=True
                    if not isLIgnore:
                        isLIgnore=True
                    else:
                        stock=file_path
                        trendChk=store.readFromFile(stock,'metaData')
                        metaDataConst=json.loads(trendChk[0])
                        mailType=email.constEmailDetails(metaDataConst['trend'],stock)
                        data=email.constructMail(mailType,'trade',str(ll),lldate)
                        email.sendMail(data)
                        metaDataConst['5']='stop'
                        metaDataConst['30']='start'
                        store.writeToFile(stock,'metaData',[metaDataConst])
                        break
    if Htrend=='up':
        hh=float(sorted_list[0]['high'])
        hhdate=sorted_list[0]['date']
        l=float(sorted_list[0]['low'])
        ldate=sorted_list[0]['date']
        hl=float(sorted_list[0]['low'])
        hldate=sorted_list[0]['date']
        ishlUpdateReq=True
        isHIgnore,isLIgnore=False,False
        for i in range(1,len(sorted_list)):
            if l<float(sorted_list[i]['low']):
                l,ldate=float(sorted_list[i]['low']),sorted_list[i]['date']
            if hh>=float(sorted_list[i]['high']):
                hh,hhdate=float(sorted_list[i]['high']),sorted_list[i]['date']
                if isHIgnore:
                    isHIgnore=False
                if isLIgnore:
                    isLIgnore=False
            else:
                if not isLIgnore:
                    if ishlUpdateReq:
                        hl,hldate=float(sorted_list[i]['low']),sorted_list[i]['date']
                    else:
                        if hl <= float(sorted_list[i]['low']):
                            hl,hldate=float(sorted_list[i]['low']),sorted_list[i]['date']
                        else:
                            isHIgnore=False
                            isLIgnore=False
                        isLIgnore=True
                    if not isHIgnore:
                        isHIgnore=True
                    else:
                        stock=file_path
                        trendChk=store.readFromFile(stock,'metaData')
                        metaDataConst=json.loads(trendChk[0])
                        mailType=email.constEmailDetails(metaDataConst['trend'],stock)
                        data=email.constructMail(mailType,'trade',str(hh),hhdate)
                        email.sendMail(data)
                        metaDataConst['5']='stop'
                        metaDataConst['30']='start'
                        store.writeToFile(stock,'metaData',[metaDataConst])
                        break


'''
first capture ll, this will be the starting point.. use this value to capture lh
'''
'''
if both max5 and max30 are same, lh will come later
if differs, max5 as lh
if both min5 and min30 are same, that is ll
if differs, update ll everytime new value comes untill 5min trend reverse occur
'''



