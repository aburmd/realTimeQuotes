import boto3

# Your bootstrap script
user_data_script = """
#!/bin/bash
su - ec2-user -c 'curl -O https://bootstrap.pypa.io/get-pip.py'
su - ec2-user -c 'python3 get-pip.py --user'
su - ec2-user -c 'pip3 install awsebcli --upgrade --user'
su - ec2-user -c 'pip3 install -U polygon-api-client'
su - ec2-user -c 'pip3 install schedule'
su - ec2-user -c 'pip3 install mailjet-rest'
su - ec2-user -c 'pip3 install boto3' 
su - ec2-user -c 'echo 'export en=EC2' >> ~/.bashrc'
su - ec2-user -c 'echo 'export test=bbfdea59aa1c732b37f66d5c7fd3fe08' >> ~/.bashrc'
su - ec2-user -c 'echo 'export tmz=pst' >> ~/.bashrc'
su - ec2-user -c 'echo 'export Trend=up' >> ~/.bashrc'
su - ec2-user -c 'source ~/.bash_profile'
su - ec2-user -c 'source ~/.bashrc'
su - ec2-user -c 'mkdir ~/DataStore'
su - ec2-user -c 'touch ~/DataStore/trend.txt'
su - ec2-user -c 'mkdir ~/workspace'
su - ec2-user -c 'sudo dnf install git-all -y'
su - ec2-user -c 'git clone https://github.com/aburmd/realTimeQuotes.git ~/workspace'
"""

# Create an EC2 resource
ec2 = boto3.resource('ec2')

# Create a new EC2 instance
def create():
    instances = ec2.create_instances(
        ImageId='ami-0a3c3a20c09d6f377',  # Replace with the AMI ID of your choice
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',  # Modify as needed
        KeyName='abu_personal',  # Replace with your key pair name
        UserData=user_data_script 
    )
    return instances[0].id

res=create()

print("New instance created:", res)