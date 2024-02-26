---Important---
-- sorted by julianday, to keep all entries in the right order 
drop table if exists temp;
create temporary table temp as 
select *,csumB/cCnt as cAvgB,csum/cCnt as cAvg, (case when cAdjTrend is null then cTrend else  cAdjTrend end) CurTrend  from indx order by julianday(strftime(qdate));

-- curL is not changing means, high gets update on every candle, capture the highest point in that journey for H
-- curH is not changing means, low gets update on every candle, capture the lowest point in that journey for L

drop table if exists temp1;
create temporary table temp1 as 
 select  quDT,qu,Ttype,CurTrend from
(select quDT,qu,Ttype,CurTrend from 
(select curHDt as quDT, curH as qu, 'H' as  Ttype,CurTrend,
row_number() over(PARTITION by curLDT order by qdate desc) as HHrnk from temp) where HHrnk=1
UNION
select quDT,qu,Ttype,CurTrend from 
(select curLDt as quDT, curL as qu, 'L' as  Ttype,CurTrend,
row_number() over(PARTITION by curHDt order by qdate) as LLrnk from temp) where LLrnk=1)
order by 1,2,3;

-- remove the entry which is moving up and then down in the upcoming candle
drop table if exists tempDe11;
create temporary table tempDe11 
as 
select a.quDT,a.Ttype,b.quDT as quDT_1,b.Ttype as Ttype_1 from 
(select quDT,datetime(quDT, '+5 minutes') as quDTC,Ttype from temp1) a,
(select quDT,datetime(quDT, '+0 minutes') as quDTC, Ttype from temp1) b
where a.quDTC=b.quDTC and b.Ttype='L'  and a.Ttype='H' 
order by a.quDT,a.Ttype,b.quDT,b.Ttype;

delete from temp1 where (quDT,Ttype) in (select  quDT,Ttype from tempDe11);

delete from temp1 where (quDT,Ttype) in (select  quDT_1,Ttype_1 from tempDe11);

drop table if exists trendReversal;
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
 order by a.quDT,a.qu,a.Ttype;
 
update indx set cAdjTrend= 
(select upComingCurTrend from trendReversal a, indx b where b.qdate=a.quDT
    and b.cAdjTrend is null and b.cCNT=(select min(b.cCnt) as cCNT from trendReversal a, indx b where a.CurTrend= b.cTrend and a.quDT=b.qdate and b.cAdjTrend is null)) 
    where indx.cCNT <= (select min(b.cCnt) as cCNT from trendReversal a, indx b where a.CurTrend= b.cTrend and a.quDT=b.qdate and b.cAdjTrend is null
    ) and  indx.cAdjTrend is null;

----end ----



def epudi():
    res=[]
    cur.execute('drop table if exists temp')
    cur.execute('create table temp as select *,csumB/cCnt as cAvgB,csum/cCnt as cAvg, (case when cAdjTrend is null then cTrend else  cAdjTrend end) CurTrend  from indx order by julianday(strftime(qdate))')
    cur.execute('drop table if exists temp1')
    ln3='''
    create temporary table temp1 as 
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
    create temporary table tempDe11 
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
    lastUpdt='select min(b.qdate) from trendReversal a, indx b where a.CurTrend= b.cTrend and a.quDT=b.qdate and b.cAdjTrend is null'
    for r in cur.execute(lastUpdt):
        res.append(r)
    conn.commit()
    return res