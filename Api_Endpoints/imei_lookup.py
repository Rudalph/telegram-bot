import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("IMEI_API_KEY")

# Check if the API key is available
if not api_key:
    raise ValueError(
        "API key not found. Make sure to set the VPNAPI_KEY environment variable in the .env file."
    )


def imei_lookup(imei):
    url = f"https://dash.imei.info/api/check/0/?API_KEY={api_key}&imei={imei}"
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


# def email_detail_fetcher(email):
#     url = "https://google-data.p.rapidapi.com/email/"+str(email)
#     # params = {"email": email}
#     headers = {
#         "X-RapidAPI-Key": "b95fd8411bmsh0848506b3e8609bp11583cjsnc7dd84f5f6ec",
#         "X-RapidAPI-Host":  "google-data.p.rapidapi.com",
#     }

#     try:
#         response = requests.get(url,headers=headers)
#         if response.status_code == 200:
#             return response.json()
#         return {}
#     except Exception as e:
#         return {"error": str(e)}

def format_dict(d, indent=0):
    formatted = ""
    for key, value in d.items():
        if isinstance(value, dict):
            formatted += " " * indent + f"{key}:\n"
            formatted += format_dict(value, indent + 4)
        elif isinstance(value, list):
            formatted += " " * indent + f"{key}:\n"
            for item in value:
                if isinstance(item, dict):
                    formatted += format_dict(item, indent + 4)
                else:
                    formatted += " " * (indent + 4) + f"- {item}\n"
        else:
            formatted += " " * indent + f"{key}: {value}\n"
    return formatted


# data=email_detail_fetcher("pallav.2905@gmail.com")
# print(format_dict(data))
    