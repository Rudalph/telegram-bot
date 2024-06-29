import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("VPNAPI_KEY")

# Check if the API key is available
if not api_key:
    raise ValueError(
        "API key not found. Make sure to set the VPNAPI_KEY environment variable in the .env file."
    )


def vpn_proxy_detection(ipAddress):
    url = f"https://vpnapi.io/api/{ipAddress}?key={api_key}"
    headers = {}

    try:
        response = requests.get(url, headers=headers)
        print(f"Response Status Code: {response.status_code}")
        print(
            f"Response Content: {response.content.decode()}"
        )  # Print full response content for debugging

        if response.status_code == 200:
            return {"status": 200, "data": response.json()}
        return {"status": response.status_code, "data": {}}
    except Exception as e:
        return {"data": {}, "status": 500, "error": str(e)}
    

def ip_address_investigation(ipAddress):
    url = f"https://ipinfo.io/widget/demo/{ipAddress}"
    headers = {}

    try:
        response = requests.get(url, headers=headers)
        print(f"Response Status Code: {response.status_code}")
        print(
            f"Response Content: {response.content.decode()}"
        )  # Print full response content for debugging

        if response.status_code == 200:
            return {"status": 200, "data": response.json()}
        return {"status": response.status_code, "data": {}}
    except Exception as e:
        return {"data": {}, "status": 500, "error": str(e)}
    
# data = ip_address_investigation("152.58.60.76")
# print(vpn_proxy_detection("152.58.60.76"))

def print_dict(d, indent=0):
        for key, value in d.items():
            if isinstance(value, dict):
                print(' ' * indent + f"{key}:")
                print_dict(value, indent + 4)
            else:
                print(' ' * indent + f"{key}: {value}")
        return d


#     # Print the data
# data1 = print_dict(data)
# print_dict(data1)