import sqlite3
import getTypeConvertor as conv
conn = sqlite3.connect('stdb2.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS indx')
cur.execute('DROP TABLE IF EXISTS uptrend')


cur.execute('''
CREATE TABLE indx (stk TEXT,qdate TEXT,open decimal,high decimal,low decimal,close decimal,curH decimal,curHdt TEXT,curL decimal,curLdt TEXT,cCnt decimal,cSumB decimal,cSum decimal,cTrend TEXT,cAdjTrend TEXT)''')


fname = input('Enter file name: ')
curTrend = input('Enter the trend (up or down):')
if (len(fname) < 1): fname = '/Users/abuhura/Desktop/DataStore/data/qqq_5min.txt'
if (len(curTrend) < 1): curTrend = 'up'
fh = open(fname)


for line in fh:
    elementHashMap=conv.convStrToHashMap(line)
    if not elementHashMap:
        continue  
    cur.execute('SELECT stk FROM indx WHERE qdate = ? ', (elementHashMap['date'],))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO indx (stk, qdate,open,high,low,close,cTrend)
                VALUES (?, ?, ?, ?, ?, ?,?)''', ('qqq',elementHashMap['date'],float(elementHashMap['open']),float(elementHashMap['high']),float(elementHashMap['low']),float(elementHashMap['close']),curTrend))
    else:
        continue
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'select qdate,high,low,close,open from indx order by julianday(strftime(qdate));'

sortVal=[]
for row in cur.execute(sqlstr):
    sortVal.append([str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4])])
preH,maxH,maxHDt=float('-infinity'),float('-infinity'),''
preL,minL,minLDt=float('infinity'),float('infinity'),''
cumSumB=0
cumSum=0
cumCnt=0
for x in sortVal:
    if preH<float(x[1]):
        maxH=float(x[1])
        maxHDt=x[0]
    if preL>float(x[2]):
        minL=float(x[2])
        minLDt=x[0]
    cumCnt+=1
    cumSumB+=abs(float(x[3])-float(x[4]))
    cumSum+=abs(float(x[1])-float(x[2]))  
    cur.execute('UPDATE indx SET curH = ?,curHdt=?,curL=?,curLdt=?,cCnt=?,cSumB=?,cSum=? WHERE qdate = ?',(maxH,maxHDt,minL,minLDt,cumCnt,cumSumB,cumSum,x[0]))
    conn.commit()
    preH,preL=float(x[1]),float(x[2])

def epudi():
    res=[]
    cur.execute('drop table if exists temp')
    ln='create table temp as select *,csumB/cCnt as cAvgB,csum/cCnt as cAvg, cTrend CurTrend  from indx order by julianday(strftime(qdate))'
    cur.execute(ln)
    cur.execute('drop table if exists temp1')
    ln3='''
    create table temp1 as 
    select  quDT,qu,Ttype,CurTrend from
    (select quDT,qu,Ttype,CurTrend from 
    (select curHDt as quDT, curH as qu, 'H' as  Ttype,CurTrend,
    row_number() over(PARTITION by curLDT order by qdate desc) as HHrnk from temp) where HHrnk=1
    UNION
    select quDT,qu,Ttype,CurTrend from 
    (select curLDt as quDT, curL as qu, 'L' as  Ttype,CurTrend,
    row_number() over(PARTITION by curHDt order by qdate) as LLrnk from temp) where LLrnk=1)
    order by 1,2,3 '''
    cur.execute(ln3)
    cur.execute('drop table if exists tempDe11')
    ln4='''
    create table tempDe11 
    as 
    select a.quDT,a.Ttype,b.quDT as quDT_1,b.Ttype as Ttype_1 from 
    (select quDT,datetime(quDT, '+5 minutes') as quDTC,Ttype from temp1) a,
    (select quDT,datetime(quDT, '+0 minutes') as quDTC, Ttype from temp1) b
    where a.quDTC=b.quDTC and b.Ttype='L'  and a.Ttype='H' 
    order by a.quDT,a.Ttype,b.quDT,b.Ttype;
    '''
    cur.execute(ln4)
    cur.execute('delete from temp1 where (quDT,Ttype) in (select  quDT,Ttype from tempDe11)')
    cur.execute('delete from temp1 where (quDT,Ttype) in (select  quDT_1,Ttype_1 from tempDe11)')
    cur.execute('drop table if exists trendReversal')
    ln5='''
    create table trendReversal as 
    with vw_dataset as
    (select quDT,qu,Ttype, CurTrend, row_number() over(PARTITION by ttype order by quDT) as rnk
    from temp1 order by quDT, (case when Ttype='L' then 1 else 2 end))
    select b.rnk as preRank,b.quDT as prequDT,b.qu as prequ,b.CurTrend as preTrend,
    a.quDT, a.qu,a.Ttype,
    a.CurTrend,
    case when b.CurTrend='down' and a.qu > b.qu and a.Ttype=b.Ttype and a.Ttype='H' then 'up'
    else (
    case when b.CurTrend='up' and a.qu < b.qu and a.Ttype=b.Ttype and a.Ttype='L' then 'down'
    else b.CurTrend
    end
    ) end as upComingCurTrend
    from vw_dataset a, vw_dataset b
    where a.rnk=b.rnk+1 and a.Ttype=b.Ttype 
    order by a.quDT,a.qu,a.Ttype
    '''
    cur.execute(ln5)
    ln1='select count(1) as cnt from trendReversal'
    lastUpdt='select min(b.cCnt) as cCNT from trendReversal a, indx b where a.CurTrend= b.cTrend and a.quDT=b.qdate and b.cAdjTrend is null'
    cTrendUpdate='''update indx set cTrend= 
    (select upComingCurTrend from trendReversal a, indx b where b.qdate=a.quDT
    and b.cAdjTrend is null and b.cCNT=?) 
    where indx.cCNT >= ? and indx.cAdjTrend is null'''
    cAdjTrendUpdate='''update indx set cAdjTrend= 
    (select upComingCurTrend from trendReversal a, indx b where b.qdate=a.quDT
    and b.cAdjTrend is null and b.cCNT=?) 
    where indx.cCNT <= ? and indx.cAdjTrend is null
    '''
    conn.commit()
    for r in cur.execute(lastUpdt):
        cur.execute(cTrendUpdate,[str(r[0]),str(r[0])])
        if r[0]:
            res.append([str(r[0])])
            conn.commit()
        print(res)
    for r in cur.execute(lastUpdt):
        cur.execute(cAdjTrendUpdate,[str(r[0]),str(r[0])])
        if r[0]:
            res.append([str(r[0])])
            conn.commit()
        print(res)
    return res

res=epudi()
conn.commit()
while res and res[0] and res[0][0]:
    res=epudi()
    conn.commit()
cur.close()