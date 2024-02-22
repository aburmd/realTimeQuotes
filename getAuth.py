import os

def getAPIKey(source):
    if source=='poly':
        res='vubKg43HwaEXAfS6tDyrYlegAewlaJJM'
    elif source=='jet':
        res='7a6ab0e0362db8618aef78fdb9179fb6'
    elif source=='tiingo':
        res='4fbd748b05ea85b5d9cf97c69aabbcd31d58bdf9'
    elif source=='twData':
        res='9fd84a3b6d2341be95c894c4842faae1'
    return res

def getSecret(source):
    if source=='jet':
        res=os.environ['test']
    return res

env=os.environ['en']
def getFilePath():
    if env=='local':
        dataPath='/Users/abuhura/Desktop/DataStore/'
    else:
        dataPath='/home/ec2-user/DataStore/'
    return dataPath

def getTrendPath():
    if env=='local':
        trendPath='/Users/abuhura/Desktop/DataStore/trend/'
    else:
        trendPath='/home/ec2-user/DataStore/trend/'
    return trendPath

def getFilePathNew():
    if env=='local':
        dataPath='/Users/abuhura/Desktop/DataStore/data/'
    else:
        dataPath='/home/ec2-user/DataStore/data/'
    return dataPath

def getTrendPathNew():
    if env=='local':
        trendPath='/Users/abuhura/Desktop/DataStore/metadata/'
    else:
        trendPath='/home/ec2-user/DataStore/metadata/'
    return trendPath
             
'''
API_KEY = os.environ['ussr']
API_SECRET = os.environ['test']
'''
