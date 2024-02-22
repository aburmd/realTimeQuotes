EC2 Machine Prerequistics:
1) https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-linux.html
2) https://github.com/git-guides/install-git#install-git-on-linux
sudo dnf install git-all
3)https://github.com/polygon-io/client-python
4) clone Git hub repo:
https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

Install Pacakage:
1) polygon
2) mailjet

pip3 install -U polygon-api-client

"HTMLPart": "<h3> Hello Abu, 30mins Candle Red </h3> <p> Hello Abu, here's a quick overview of today's market trends. Based on the current movement, the market is predominantly trending upward. This analysis is derived from the 4-hour timeframe, indicating an UpTrend. Both the 30-minute and 4-hour trends are currently aligned in the same direction. However, the most recent 30-minute candle suggests a potential reversal. This possibility becomes more pronounced if the 5-minute candle confirms the trend reversal after the observed 30-minute candle. Stay calm, relax, and make well-informed decisions! Best of luck!</p>"

4hrs Up, 30mins up:
Hello Abu, here's a quick overview of today's market trends. Based on the current movement, the market is predominantly trending upward. This analysis is derived from the 4-hour timeframe, indicating an UpTrend. Both the 30-minute and 4-hour trends are currently aligned in the same direction. However, the most recent 30-minute candle suggests a potential reversal. This possibility becomes more pronounced if the 5-minute candle confirms the trend reversal after the observed 30-minute candle. Stay calm, relax, and make well-informed decisions! Best of luck!

4hrs Up, 30mins down:
<h3> Hello Abu, 30mins Candle Green </h3>
Hi Abu, I wanted to share a quick summary of today's market trends with you. Currently, the market is showing a predominant downward trend, but there are indications of a possible reversal to an upward trend. This analysis is based on the 4-hour timeframe, which suggests an UpTrend. However, it's important to note that the 30-minute timeframe is currently showing a downward trend, and the alignment with the 4-hour trend is not consistent. The most recent 30-minute candle hints at a potential reversal, and this possibility becomes more significant if the 5-minute candle confirms the trend reversal after the observed 30-minute candle. Stay composed, take a deep breath, and make informed decisions! Best wishes for successful trading!

bootsrtap.sh 

curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
pip3 install awsebcli --upgrade --user
pip3 install -U polygon-api-client
pip3 install schedule
pip3 install mailjet-rest 
echo 'export en=EC2' >> ~/.bashrc
echo 'export test=bbfdea59aa1c732b37f66d5c7fd3fe08' >> ~/.bashrc
echo 'export tmz=pst' >> ~/.bashrc
echo 'export trend=up' >> ~/.bashrc
source ~/.bash_profile
mkdir ~/DataStore
touch ~/DataStore/trend.txt
mkdir ~/workspace
cd ~/workspace
sudo dnf install git-all
git clone https://github.com/aburmd/realTimeQuotes.git
cd ~/
nohup python3 ~/workspace/realTimeQuotes/marketWatcher.py &



Here's a simplified overview of our process:

1) Initial Setup: The script initialFileCreate.py prepares necessary files in the specified path.
2) Every 30 Minutes:
   a) query30.py runs to publish the quote precisely every 30 minutes.
   b) main.py checks if the last candle has reversed its trend. If it has, it updates the metadata to indicate a 'start' signal for 5-minute tracking.
3) Every 5 Minutes:
   a) query5.py is scheduled to run, but it first checks if the 'start' signal for 5-minute tracking is active. If it is, it publishes a 5-minute quote.
   b) Alongside, main5.py tracks the lowest value in the last 30 minutes and updates it as needed until a reversal trend is identified. Upon finding a reversal, it updates the metadata with specific value indicators and signals a 'start' for reversal tracking.
4) Reversal Tracking:
   a) main5R.py activates upon the 'start' reversal signal, comparing current 5-minute highs/lows against previous markers. Depending on the outcome, it categorizes the result as 'False' or 'Execute' and updates the metadata to stop 5-minute tracking.
5) Completion:
   a)Once the 'stop' signal is issued for 5-minute tracking, query5.py pauses its publishing task, and both main5.py and main5R.py conclude their operations until the next 'start' signal.

This sequence ensures our system dynamically updates and responds based on specific trend reversals and predefined intervals.


