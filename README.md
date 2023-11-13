# Ubiquity_extreme_signal_checker
The simple tool which main goal is find the Ubiquity devices which Tx signal is below singal which we expected(CUT OFF parameter).
This tool, login to all available Ubiquity devices in network. To login this devices is used ssh session. When The needed information is found and
is added to the list. Tool generate two .txt files which include:
* The first one contains infomration from all Ubiquity devices
* The second one contains only information, when CUTOFF parameter is not expected as we want.

### Create Virtual Env(Is Optional)
pip3 install virtualenv

source UbiScanner/bin/activate

### Install required packages
pip3 install -r requirements.txt

### Run Script
python3 ubiquity_extreme_signal_checker.py

### Comments
The file with list of output was generated in the same directory as the python script.
