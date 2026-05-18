import requests 
requests.packages.urllib3.disable_warnings()
url = "https://192.168.35.129/mgmt/tm/sys/version"
username = "admin"
password = "Tannu@123"

response = requests.get(
url,
auth=(username, password),
verify=False
)
print(response.json())

