import requests
import urllib3
import json

urllib3.disable_warnings()

#############################################################################
############################ F5 CONNECTION ##################################
#############################################################################

F5_IP = "192.168.35.129"
USERNAME = "admin"
PASSWORD = "Tannu@123"

#############################################################################
############################ APPLICATION VARIABLES ###########################
#############################################################################

APP_NAME = "inventory_app"

POOL_NAME = f"{APP_NAME}_pool"

VIP_NAME = f"{APP_NAME}_vip"
VIP_IP = "192.169.106.201"
VIP_PORT = 80

POOL_MEMBERS = [
    "192.169.106.128",
    "192.169.106.129"
]

MONITOR_NAME = f"{APP_NAME}_monitor"

#############################################################################
############################ COMMON VARIABLES ################################
#############################################################################

HEADERS = {
    "Content-Type": "application/json"
}

AUTH = (USERNAME, PASSWORD)

BASE_URL = f"https://{F5_IP}"

#############################################################################
############################ CREATE MONITOR ##################################
#############################################################################

monitor_url = f"{BASE_URL}/mgmt/tm/ltm/monitor/http"

monitor_payload = {
    "name": MONITOR_NAME
}

monitor_response = requests.post(
    monitor_url,
    auth=AUTH,
    headers=HEADERS,
    json=monitor_payload,
    verify=False
)

print("\n========== MONITOR RESPONSE ==========")
print("Status:", monitor_response.status_code)
print(monitor_response.text)

#############################################################################
############################ CREATE POOL #####################################
#############################################################################

pool_url = f"{BASE_URL}/mgmt/tm/ltm/pool"

pool_payload = {
    "name": POOL_NAME,
    "monitor": MONITOR_NAME
}

pool_response = requests.post(
    pool_url,
    auth=AUTH,
    headers=HEADERS,
    json=pool_payload,
    verify=False
)

print("\n========== POOL RESPONSE ==========")
print("Status:", pool_response.status_code)
print(pool_response.text)

#############################################################################
############################ ADD POOL MEMBERS ################################
#############################################################################

for member_ip in POOL_MEMBERS:

    member_url = f"{BASE_URL}/mgmt/tm/ltm/pool/~Common~{POOL_NAME}/members"

    member_payload = {
        "name": f"{member_ip}:{VIP_PORT}",
        "address": member_ip
    }

    member_response = requests.post(
        member_url,
        auth=AUTH,
        headers=HEADERS,
        json=member_payload,
        verify=False
    )

    print(f"\n========== MEMBER {member_ip} RESPONSE ==========")
    print("Status:", member_response.status_code)
    print(member_response.text)

#############################################################################
############################ CREATE VIRTUAL SERVER ###########################
#############################################################################

vip_url = f"{BASE_URL}/mgmt/tm/ltm/virtual"

vip_payload = {
    "name": VIP_NAME,
    "partition": "Common",
    "destination": f"{VIP_IP}:{VIP_PORT}",
    "ipProtocol": "tcp",
    "sourceAddressTranslation": {
        "type": "automap"
    },
    "pool": f"/Common/{POOL_NAME}"
}

vip_response = requests.post(
    vip_url,
    auth=AUTH,
    headers=HEADERS,
    json=vip_payload,
    verify=False
)

print("\n========== VIP RESPONSE ==========")
print("Status:", vip_response.status_code)
print(vip_response.text)

#############################################################################
############################ FINAL STATUS ####################################
#############################################################################

print("\n========== DEPLOYMENT COMPLETE ==========")
print(f"Application Name : {APP_NAME}")
print(f"VIP              : {VIP_IP}:{VIP_PORT}")
print(f"Pool             : {POOL_NAME}")
print(f"Members          : {POOL_MEMBERS}")