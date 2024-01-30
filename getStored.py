'''
Input list of elements to be added as a file
https://www.geeksforgeeks.org/writing-to-file-in-python/
'''
import json
import getAuth as auth

def fileInput(list):
    file = open(auth.getFilePath,'w')
    i=0
    for d in list:
        s=json.dumps(d)+'\n'
        file.write(s)
        i+=1
    file.close()
    print("File saved successfully with {} no of lines stored".format(i))
    
def fileWriter(list,filetype):
    file=''
    if filetype=='store':
        file = open(auth.getFilePath(),'w')
    else:
        file = open(auth.getTrendPath(),'w')
    i=0
    for d in list:
        s=json.dumps(d)+'\n'
        file.write(s)
        i+=1
    file.close()
    print("File saved successfully with {} no of lines stored".format(i))
    
def fileReader(filetype):
    if filetype=='store':
        file = open(auth.getFilePath(),'r')
    else:
        file = open(auth.getTrendPath(),'r')
    res=file.read()
    data=res.split("\n")
    print("File Available with {} of entries,the function reads from file and stored with type as {}.".format(len(data),type(data)))
    return data