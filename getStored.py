'''
Input list of elements to be added as a file
https://www.geeksforgeeks.org/writing-to-file-in-python/
'''
import json
import getAuth as auth

def fileInput(list):
    file = open(auth.getFilePath(),'w')
    for d in list:
        s=json.dumps(d)+'\n'
        file.write(s)
    file.close()

    