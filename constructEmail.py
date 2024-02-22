from mailjet_rest import Client as mail
import getAuth as auth
api_val=auth.getAPIKey('jet')
api_token=auth.getSecret('jet')


def constEmailDetails(trend,stock):
    trendType='LH' if trend=='down' else 'HL'
    dirc='Low' if trend=='down' else 'High'
    rdirc='High' if trend=='down' else 'Low'
    cTrendType='LL' if trend=='down' else 'HH'
    subject1 = 'Alert: {} - 30min Candle Trend Reversal'.format(stock)
    content1 = '''Hello Abu, Possible Trend reversal on {} for 30mins Candle.
                    So, Initiated 30mins candle to capture {}. 
                    Next step, will possibly to capture the {} on 5mins Candle. 
                    Upon {} received, the next step is identify whether 30mins Low or 30mins high reached first, 
                    If 30mins {} reached, next mail will possibly to execute the trade.
                    If it reversed and crossed the 30mins {}, next mail will possibly to say - False Alarm
                '''.format(stock,trendType,trendType,trendType,dirc,rdirc)
    subject2 = 'Place StopLoss Trade: {} - 5mins Candle Trend - {} received after {}'.format(stock,cTrendType,trendType)
    content2 = '''Hello Abu, {} received for {} on 5mins Candle. 
              This is captured after 30 mins reversal occurs. 
              Hence, it is time, Place a stoploss order.'''.format(cTrendType,stock)
    subject3 = 'False Alarm: {} - 5mins Candle Trend - reversed and crossed the 30mins {}'.format(stock,rdirc)
    content3 = '''Hello Abu, Trend continued with 30mins 
              as 5mins candle crosses previous 30mins same trend.
              Hence, it considered to be false alarm.'''
    res={'alert':[subject1,content1],'trade':[subject2,content2],'falarm':[subject3,content3]}
    return res
    
def constructMail(res,conType,*arg):
    subject=res[conType][0]
    content=res[conType][1]
    ll,llDate=None,None
    if len(arg)>0:
      ll='- with LL '+arg[0]
    if len(arg)>1:
      llDate=' at '+arg[1]
    data = {'Messages': 
        [{"From": {"Email": "aburmd@gmail.com","Name": "TradeAssitant"},
          "To":[{"Email": "abudigitalworld@gmail.com","Name": "AbuDigital"},
            {"Email": "huraira86@gmail.com","Name": "Abu"}],
        "Subject": "{}{}{}".format(subject,ll,llDate),
      "HTMLPart": "<h3><p>{}</p></h3>".format(content)}]}
    return data

def sendMail(data):
    mailjet = mail(auth=(api_val, api_token), version='v3.1')
    result = mailjet.send.create(data=data)
    return result