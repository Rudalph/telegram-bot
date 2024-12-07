import requests
import os
from dotenv import load_dotenv

load_dotenv()
rapid_api_key = os.getenv("RAPID_API_KEY")


def whois_lookup(domain):
    url = f"https://domaination.p.rapidapi.com/domains/{domain}"

    headers = {
        "x-rapidapi-key": rapid_api_key,
        "x-rapidapi-host": "domaination.p.rapidapi.com",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {"status": 200, "data": response.json()}
        return {"status": response.status_code, "data": {}}
    except Exception as e:
        return {"data": {}, "status": 500, "error": str(e)}
