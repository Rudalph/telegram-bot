import requests

def leak_check(email):
    url = f"https://leakcheck.io/api/public?check={str(email)}"
    headers = {
    }

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {"status": response.status_code, "data": {}}
    except Exception as e:
        return {"data": {}, "status": 500, "error": str(e)}
