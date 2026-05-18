import requests
import json
import urllib3
urllib3.disable_warnings()
url = "https://192.168.35.129/mgmt/tm/ltm/pool/automation_pool/members"
headers = { "Content-Type": "application/json" }
username = "admin"
password = "Tannu@123"

members_payload = [
{"name": "192.168.106.132:80"},
{"name": "192.168.106.133:80"}
]
for member in members_payload:
 member_response = requests.post(
  url,
  auth = (username, password),
  headers = headers,
  json = member,
  verify = False
)

print("\nPool Members status:")
print(member_response.status_code)
print(member_response.text)




