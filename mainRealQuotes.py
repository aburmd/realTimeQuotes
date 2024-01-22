from polygon import RESTClient as SQ
import realQuote
import getAuth as auth
import getFormatConvertor as formater
import getStored

api_val=auth.getAPIKey('poly')
sqClient=SQ(api_key=api_val)
'''
start_dt=formater.getCurDate()
end_dt=formater.getCurDate()
'''
start_dt='2024-01-16'
end_dt='2024-01-16'

data=realQuote.getQuote(start_dt,end_dt)
getStored.fileInput(data['results'])
quotes=realQuote.defaultQuoteGenerator({})
quotes=realQuote.storeQuotes(data['results'],quotes)
print(quotes)
