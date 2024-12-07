import requests

def crypto_inves(hash):
    url = f"https://api-crypto-u33s.onrender.com/get-transactions?hash={hash}"
    headers = {
        # "Authorization":api_key,
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        return {"error": str(e)}

