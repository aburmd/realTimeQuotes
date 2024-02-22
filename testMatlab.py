'''
Need to explore more on this
'''

import coreLogic as core
import getTypeConvertor as conv
import getStored as store
import json
import constructEmail as email
import matplotlib.pyplot as plt
import numpy as np
# Example usage
def fileToDict(file_path,file5):
    file5=file_path+'_'+file5+'min'
    resT5=store.readFromFile(file5,'store')
    res5=[]
    for e in resT5:
        if e=='':
            continue
        elementHashMap=conv.convStrToHashMap(e)
        res5.append(elementHashMap)
    sorted_list = sorted(res5, key=lambda x: x['date'])
    return sorted_list
res=fileToDict('ndx','1')
xarr,yarr=[],[]
for i,n in enumerate(res):
    xarr.append(i)
    yarr.append(float(n['low']))
    
#print(xarr[:10],yarr[:10])

# Sample data points
x = np.array(xarr)
y = np.array(yarr)

# Plotting the data points
#plt.scatter(x, y)
plt.plot(xarr,yarr)

'''
# Fitting a linear trend line
m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b, color='red') # Trend line
'''
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Trend Line Example')
plt.show()

