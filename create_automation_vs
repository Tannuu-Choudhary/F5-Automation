import requests
import json
import urllib3

urllib3.disable_warnings()

headers = {
	"Content-Type": "application/json"
}

vs_url = "https://192.168.35.129/mgmt/tm/ltm/virtual"

username = "admin"
password = "Tannu@123"

vs_payload = {
    "name": "automation_vs",
    "destination": "192.168.106.201:80",
    "ipProtocol": "tcp",
    "mask": "255.255.255.255",
    "pool": "automation_pool",
    "sourceAddressTranslation": {
        "type": "automap"
    },
    "profiles": [
        {
            "name": "tcp"
        }
    ]
}

vs_response = requests.post(
    vs_url,
    auth=(username, password),
    headers=headers,
    json=vs_payload,
    verify=False
)

print("\nVS status code:", vs_response.status_code)
print("Response:")
print(vs_response.text)