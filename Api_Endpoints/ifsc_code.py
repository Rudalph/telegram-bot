import requests

def ifsc_lookup(ifsc):
    url = f"https://ifsc.razorpay.com/{ifsc}"
    headers = {
    }

    try:
        response = requests.get(url)
        print(f"Response Status Code: {response.status_code}")
        print(
            f"Response Content: {response.content.decode()}"
        )  # Print full response content for debugging

        if response.status_code == 200:
            return {"status": response.status_code, "data": response.json()}
        return {"status": response.status_code, "data": {}}
    except Exception as e:
        return {"data": {}, "status": 500, "error": str(e)}

