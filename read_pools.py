import requests
import json
import urllib3
urllib3.disable_warnings()
url = "https://192.168.35.129/mgmt/tm/ltm/pool"
username = "admin"
password = "Tannu@123"
response = requests.get(
url,
auth=(username, password),
verify = False )

data = response.json()
print(json.dumps(data, indent=4))
