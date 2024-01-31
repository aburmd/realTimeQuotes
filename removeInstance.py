import boto3
ec2 = boto3.client('ec2')
response = ec2.describe_instances()
res=[]
def listInstances():
    listInstance=[]
    for l in response['Reservations']:
        listInstance.append([l['Instances'][0]['InstanceId'],l['Instances'][0]['State']])
    for n in listInstance:
        if n[1]['Name']=='running':
            res.append(n[0])
    return res

def getTerminateInstance(instance):
    return ec2.terminate_instances(InstanceIds=[instance])

def job():
    instancesList=listInstances()
    responseList=[]
    for i in instancesList:
        responseList.append(getTerminateInstance(i))
        print("Running EC2 Intance:{} is terminated".format(i))

job()