import requests

def upi_lookup(vpa):
    url = f"https://upi-details.onrender.com/upi-details?vpa={vpa}"

    headers = {
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return {"status": response.status_code, "data": {}}
    except Exception as e:
        return {"data": {}, "status": 500, "error": str(e)}

