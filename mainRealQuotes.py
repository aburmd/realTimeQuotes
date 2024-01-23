from polygon import RESTClient as SQ
import realQuote
import getAuth as auth
import getFormatConvertor as formater
import getStored
'''
start_dt=formater.getDate()
end_dt=formater.getDate()
print(start_dt)
'''
start_dt='2024-01-16'
end_dt='2024-01-16'


data=realQuote.getQuote(start_dt,end_dt,'tiingo')
print(data)
print(type(data))
getStored.fileInput(data)

