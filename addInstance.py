import boto3

# Your bootstrap script
user_data_script = """
#!/bin/bash
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
pip3 install awsebcli --upgrade --user
pip3 install -U polygon-api-client
pip3 install schedule
pip3 install mailjet-rest
pip3 install boto3
echo 'export en=EC2' >> ~/.bashrc
echo 'export test=bbfdea59aa1c732b37f66d5c7fd3fe08' >> ~/.bashrc
echo 'export tmz=pst' >> ~/.bashrc
echo 'export Trend=up' >> ~/.bashrc
source ~/.bash_profile
source ~/.bashrc
mkdir ~/DataStore
touch ~/DataStore/trend.txt
mkdir ~/workspace
sudo dnf install git-all -y
cd ~/workspace
git clone https://github.com/aburmd/realTimeQuotes.git
cd ~
nohup python3 ~/workspace/realTimeQuotes/test.py &
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