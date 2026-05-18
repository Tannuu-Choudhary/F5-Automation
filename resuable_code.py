import requests
import urllib3

#############################################################################
######################## DISABLE SSL WARNINGS ###############################
#############################################################################

urllib3.disable_warnings()

#############################################################################
######################## F5 CONNECTION DETAILS ##############################
#############################################################################

F5_IP = "192.168.35.129"

USERNAME = "admin"

PASSWORD = "Tannu@123"

#############################################################################
######################## APPLICATION DETAILS ################################
#############################################################################

APP_NAME = "Jenkin_Automation"

POOL_NAME = f"{APP_NAME}_Pool"

VIP_NAME = f"{APP_NAME}_VS"

MONITOR_NAME = f"{APP_NAME}_Monitor"

VIP_IP = "192.168.106.203"

VIP_PORT = 80

#############################################################################
######################## BACKEND POOL MEMBERS ###############################
#############################################################################

POOL_MEMBERS = [
    "192.168.106.139",
    "192.168.106.140"
]

#############################################################################
######################## COMMON VARIABLES ###################################
#############################################################################

HEADERS = {
    "Content-Type": "application/json"
}

AUTH = (USERNAME, PASSWORD)

BASE_URL = f"https://{F5_IP}/mgmt/tm/ltm"

#############################################################################
######################## CREATE MONITOR #####################################
#############################################################################

print("\n========== Creating Monitor ==========")

MONITOR_URL = f"{BASE_URL}/monitor/http"

MONITOR_PAYLOAD = {
    "name": MONITOR_NAME
}

MONITOR_RESPONSE = requests.post(
    MONITOR_URL,
    auth=AUTH,
    headers=HEADERS,
    json=MONITOR_PAYLOAD,
    verify=False
)

print("Status:", MONITOR_RESPONSE.status_code)

print(MONITOR_RESPONSE.text)

#############################################################################
######################## CREATE POOL ########################################
#############################################################################

print("\n========== Creating Pool ==========")

POOL_URL = f"{BASE_URL}/pool"

POOL_PAYLOAD = {
    "name": POOL_NAME,
    "loadBalancingMode": "round-robin",
    "monitor": f"/Common/{MONITOR_NAME}"
}

POOL_RESPONSE = requests.post(
    POOL_URL,
    auth=AUTH,
    headers=HEADERS,
    json=POOL_PAYLOAD,
    verify=False
)

print("Status:", POOL_RESPONSE.status_code)

print(POOL_RESPONSE.text)

#############################################################################
######################## ADD POOL MEMBERS ###################################
#############################################################################

print("\n========== Adding Pool Members ==========")

MEMBER_URL = f"{BASE_URL}/pool/~Common~{POOL_NAME}/members"

for member in POOL_MEMBERS:

    MEMBER_PAYLOAD = {
        "name": f"{member}:{VIP_PORT}",
        "address": member
    }

    MEMBER_RESPONSE = requests.post(
        MEMBER_URL,
        auth=AUTH,
        headers=HEADERS,
        json=MEMBER_PAYLOAD,
        verify=False
    )

    print(f"\nAdding Member: {member}")

    print("Status:", MEMBER_RESPONSE.status_code)

    print(MEMBER_RESPONSE.text)

#############################################################################
######################## CREATE VIRTUAL SERVER ##############################
#############################################################################

print("\n========== Creating Virtual Server ==========")

VIP_URL = f"{BASE_URL}/virtual"

VIP_PAYLOAD = {
    "name": VIP_NAME,

    "destination": f"/Common/{VIP_IP}:{VIP_PORT}",

    "mask": "255.255.255.255",

    "ipProtocol": "tcp",

    "translateAddress": "enabled",

    "translatePort": "enabled",

    "sourceAddressTranslation": {
        "type": "automap"
    },

    "pool": f"/Common/{POOL_NAME}"
}

VIP_RESPONSE = requests.post(
    VIP_URL,
    auth=AUTH,
    headers=HEADERS,
    json=VIP_PAYLOAD,
    verify=False
)

print("Status:", VIP_RESPONSE.status_code)

print(VIP_RESPONSE.text)

#############################################################################
######################## SAVE F5 CONFIG #####################################
#############################################################################

print("\n========== Saving Configuration ==========")

SAVE_URL = f"https://{F5_IP}/mgmt/tm/sys/config"

SAVE_PAYLOAD = {
    "command": "save"
}

SAVE_RESPONSE = requests.post(
    SAVE_URL,
    auth=AUTH,
    headers=HEADERS,
    json=SAVE_PAYLOAD,
    verify=False
)

print("Status:", SAVE_RESPONSE.status_code)

print(SAVE_RESPONSE.text)

#############################################################################
######################## FINAL DEPLOYMENT STATUS ############################
#############################################################################

print("\n========== DEPLOYMENT COMPLETE ==========")

print(f"Application Name : {APP_NAME}")

print(f"VIP Name         : {VIP_NAME}")

print(f"VIP Address      : {VIP_IP}:{VIP_PORT}")

print(f"Pool Name        : {POOL_NAME}")

print(f"Monitor Name     : {MONITOR_NAME}")

print(f"Pool Members     : {POOL_MEMBERS}")