import requests

def crypto_inves(hash):
    url = f"https://api-crypto-u33s.onrender.com/get-transactions?hash={hash}"
    headers = {
        # "Authorization":api_key,
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

