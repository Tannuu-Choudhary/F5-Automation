import requests
import urllib3
import os
import sys

#############################################################################
######################## DISABLE SSL WARNINGS ###############################
#############################################################################

urllib3.disable_warnings()

#############################################################################
######################## F5 CONNECTION DETAILS ##############################
#############################################################################

F5_IP = os.environ['TARGET_F5']

USERNAME = os.environ['F5_CREDS_USR']

PASSWORD = os.environ['F5_CREDS_PSW']

#############################################################################
######################## JENKINS PARAMETERS #################################
#############################################################################

APP_NAME = os.environ['APP_NAME']

ENVIRONMENT = os.environ['ENVIRONMENT']

VIP_IP = os.environ['VIP_IP']

VIP_PORT = int(os.environ['VIP_PORT'])

POOL_MEMBERS = [
    member.strip()
    for member in os.environ['POOL_MEMBERS'].split(',')
]

#############################################################################
######################## DYNAMIC OBJECT NAMES ###############################
#############################################################################

POOL_NAME = f"{ENVIRONMENT}_{APP_NAME}_Pool"

VIP_NAME = f"{ENVIRONMENT}_{APP_NAME}_VS"

MONITOR_NAME = f"{ENVIRONMENT}_{APP_NAME}_Monitor"

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

try:

    MONITOR_RESPONSE = requests.post(
        MONITOR_URL,
        auth=AUTH,
        headers=HEADERS,
        json=MONITOR_PAYLOAD,
        verify=False,
        timeout=15
    )

    print("Status:", MONITOR_RESPONSE.status_code)
    print(MONITOR_RESPONSE.text)

    if MONITOR_RESPONSE.status_code not in [200, 201]:
        print("Monitor Creation Failed")
        sys.exit(1)

except Exception as e:

    print("Error During Monitor Creation")
    print(e)

    sys.exit(1)

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

try:

    POOL_RESPONSE = requests.post(
        POOL_URL,
        auth=AUTH,
        headers=HEADERS,
        json=POOL_PAYLOAD,
        verify=False,
        timeout=15
    )

    print("Status:", POOL_RESPONSE.status_code)
    print(POOL_RESPONSE.text)

    if POOL_RESPONSE.status_code not in [200, 201]:
        print("Pool Creation Failed")
        sys.exit(1)

except Exception as e:

    print("Error During Pool Creation")
    print(e)

    sys.exit(1)

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

    try:

        MEMBER_RESPONSE = requests.post(
            MEMBER_URL,
            auth=AUTH,
            headers=HEADERS,
            json=MEMBER_PAYLOAD,
            verify=False,
            timeout=15
        )

        print(f"\nAdding Member: {member}")

        print("Status:", MEMBER_RESPONSE.status_code)

        print(MEMBER_RESPONSE.text)

        if MEMBER_RESPONSE.status_code not in [200, 201]:
            print(f"Failed To Add Member: {member}")
            sys.exit(1)

    except Exception as e:

        print(f"Error Adding Member: {member}")

        print(e)

        sys.exit(1)

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

try:

    VIP_RESPONSE = requests.post(
        VIP_URL,
        auth=AUTH,
        headers=HEADERS,
        json=VIP_PAYLOAD,
        verify=False,
        timeout=15
    )

    print("Status:", VIP_RESPONSE.status_code)

    print(VIP_RESPONSE.text)

    if VIP_RESPONSE.status_code not in [200, 201]:
        print("VIP Creation Failed")
        sys.exit(1)

except Exception as e:

    print("Error During VIP Creation")

    print(e)

    sys.exit(1)

#############################################################################
######################## SAVE CONFIGURATION #################################
#############################################################################

print("\n========== Saving Configuration ==========")

SAVE_URL = f"https://{F5_IP}/mgmt/tm/sys/config"

SAVE_PAYLOAD = {
    "command": "save"
}

try:

    SAVE_RESPONSE = requests.post(
        SAVE_URL,
        auth=AUTH,
        headers=HEADERS,
        json=SAVE_PAYLOAD,
        verify=False,
        timeout=15
    )

    print("Status:", SAVE_RESPONSE.status_code)

    print(SAVE_RESPONSE.text)

except Exception as e:

    print("Error Saving Configuration")

    print(e)

    Print ("successfull")

#############################################################################
######################## FINAL DEPLOYMENT STATUS ############################
#############################################################################

print("\n========== DEPLOYMENT COMPLETE ==========")

print(f"Environment      : {ENVIRONMENT}")

print(f"Application Name : {APP_NAME}")

print(f"VIP Name         : {VIP_NAME}")

print(f"VIP Address      : {VIP_IP}:{VIP_PORT}")

print(f"Pool Name        : {POOL_NAME}")

print(f"Monitor Name     : {MONITOR_NAME}")

print(f"Pool Members     : {POOL_MEMBERS}")