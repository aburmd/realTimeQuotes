import coreLogic as core
import getTypeConvertor as conv
import getStored as store

# Example usage
def main5(file_path,bigV,smallV):
    file_path = file_path  # Change this to your text file's path
    file5=file_path+'_'+smallV+'min'
    file30=file_path+'_'+bigV+'min'
    resT30=store.readFromFile(file30,'store')
    res30=[]
    for e in resT30:
        if e=='':
            continue
        elementHashMap=conv.convStrToHashMap(e)
        res30.append(elementHashMap)

    startQtime=res30[-1]
    resT5=store.readFromFile(file5,'store')
    res5=[]
    for e in resT5:
        if e=='':
            continue
        elementHashMap=conv.convStrToHashMap(e)
        if elementHashMap['date'] <= startQtime['date']:
            continue
        res5.append(elementHashMap)
        
    sorted_list = sorted(res5, key=lambda x: x['date'])
    ll=float(sorted_list[1]['low'])
    lldate=sorted_list[1]['date']
    isIgnore=False
    for i in range(2,len(sorted_list)):
        if ll>=float(sorted_list[i]['low']):
            ll,lldate=float(sorted_list[i]['low']),sorted_list[i]['date']
            if isIgnore:
                isIgnore=False
        else:
            if not isIgnore:
                isIgnore=True
            else:
                break

    maxVal,minVal=0,-1
    for r in res5:
        maxVal=max(maxVal,r['high']) 
        minVal=min(minVal,r['low'])
    print(maxVal,startQtime['high'])
'''
first capture ll, this will be the starting point.. use this value to capture lh
'''
'''
if both max5 and max30 are same, lh will come later
if differs, max5 as lh
if both min5 and min30 are same, that is ll
if differs, update ll everytime new value comes untill 5min trend reverse occur
'''




    