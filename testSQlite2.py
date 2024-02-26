import sqlite3
import getTypeConvertor as conv
conn = sqlite3.connect('stdb2.sqlite')
cur = conn.cursor()

sqlstr = 'select qdate,open,high,low,close,cCNT,HH,HL,LL,LH,Trend from tempIndx order by cCNT;'


sortVal=[]
for row in cur.execute(sqlstr):
    sortVal.append([str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5]),str(row[6]),str(row[7]),str(row[8]),str(row[9]),str(row[10])])
print(sortVal[0])
HH,HL,LL,LH= 427.35,427.35,425.40,425.40
preH,preL= float('infinity'),float('-infinity')
trend=''
LLHigh, HHLow = 427.35,427.35
upDTQ='update tempIndx set HH=?,LL=?,LH=?,HL=?,Trend=? where cCNT=?'
for x in sortVal:
    trend=max(str(x[10]),trend)
    CNT=str(x[5])
    if HH < float(x[2]) and LL > float(x[3]):
        cur.execute(upDTQ,(str(HH),str(LL),str(LH),str(HL),trend,CNT))
        conn.commit()
        continue
    if HH<float(x[2]):
        if HL > HHLow:
            LL=HL
            LH=HL
        HH=float(x[2])
        HL=float(x[2])
        HHLow=float(x[3])
        trend='up'
        preH,preL=float(x[2]),float(x[3])
        cur.execute(upDTQ,(str(HH),str(LL),str(LH),str(HL),trend,CNT))
        conn.commit()
        continue
    if LL>float(x[3]):
        if LH > LLHigh:
            HH=LH
            HL=LH
        LL=float(x[3])
        LH=float(x[3])
        LLHigh=float(x[2])
        trend='down'
        preH,preL=float(x[2]),float(x[3])
        cur.execute(upDTQ,(str(HH),str(LL),str(LH),str(HL),trend,CNT))
        conn.commit()
        continue
    if trend=='up':
        if preL==HHLow:
            HL=min(HL,float(x[3]))
        else:
            HL=min(preL,HL)
            HL=min(HL,float(x[3]))
    if trend=='down':
        if preH==LLHigh:
            LH=max(LH,float(x[2]))
        else:
            LH=max(preH,LH)
            LH=max(LH,float(x[2]))
    preH,preL=float(x[2]),float(x[3])
    cur.execute(upDTQ,(str(HH),str(LL),str(LH),str(HL),trend,CNT))
    conn.commit()

#validate data QQQ 21Feb2024 9:30 to 11.35
cur.close()