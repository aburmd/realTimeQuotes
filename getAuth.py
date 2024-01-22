import os

def getAPIKey(source):
    if source=='poly':
        res='vubKg43HwaEXAfS6tDyrYlegAewlaJJM'
    elif source=='jet':
        res='7a6ab0e0362db8618aef78fdb9179fb6'
    return res

def getSecret(source):
    if source=='jet':
        res=os.environ['test']
    return res
            
file_path='/Users/abuhura/Desktop/QQQ.txt'  
'''
API_KEY = os.environ['ussr']
API_SECRET = os.environ['test']
'''
