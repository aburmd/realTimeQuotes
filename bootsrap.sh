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
echo 'export trend=up' >> ~/.bashrc
source ~/.bash_profile
mkdir ~/DataStore
touch ~/DataStore/trend.txt
mkdir ~/workspace
cd ~/workspace
sudo dnf install git-all -y
git clone https://github.com/aburmd/realTimeQuotes.git
cd ~/