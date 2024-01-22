'''
This library helps to convert a rare object type to commonly used type such such string,list,hashmap etc.
In this module, polyAPI return aggregate stock quotes in HTTPResponse which is then cast to return as bytes
'''
import json
from urllib3 import HTTPResponse
from typing import cast

def convByteToDict(bytes):
    input=bytes
    #convert bytes to str
    bytesToStr=input.decode('utf8').replace("'", '"')
    #convert str into hashmap
    res=json.loads(bytesToStr)
    return res

def convHTTPResponseToByte(args):
    return cast(HTTPResponse,args,)

def convStrToHashMap(s):
    return json.loads(s)