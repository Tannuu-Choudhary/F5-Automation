import requests
requests.packages.urllib3.disable_warnings()
url = "https://192.168.35.129/mgmt/tm/ltm/pool"
username = "admin"
password = "Tannu@123"

payload = {
"name" : "automation_pool",
"loadBalancingMode" : "round-robin",
"partition" : "Common",
"monitor" : "tcp"
}

response = requests.post(
url,
auth=(username, password),
json=payload,
verify=False
)

print(response.status_code)
print(response.text)