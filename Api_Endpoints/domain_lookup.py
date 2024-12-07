import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MOJODNS_API_KEY")

# Check if the API key is available
if not api_key:
    raise ValueError(
        "API key not found. Make sure to set the VPNAPI_KEY environment variable in the .env file."
    )

def dns_lookup(domain):
    url = f"https://api.mojodns.com/api/dns/{domain}/a"
    headers = {
        "Authorization":api_key,
    }

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

