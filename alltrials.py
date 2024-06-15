# ==================================================================================================================================================================
import requests


def social_media_accounts(number):
    url = f"https://api.us-east-1-main.seon.io/SeonRestService/phone-api/v1/+91{number}"
    headers = {"X-API-KEY": "3b98a3b4-6945-402b-9c5f-01d4bf7f7383"}

    try:
        response = requests.get(url, headers=headers)
        print(f"Response Status Code: {response.status_code}")
        print(
            f"Response Content: {response.content.decode()}"
        )  # Print full response content for debugging

        if response.status_code == 200:
            data = response.json()
            print(f"Response JSON: {data}")  # Print JSON content

            if data.get("success"):
                account_details = data.get("data", {}).get("account_details", {})
                accounts = [
                    k for k, v in account_details.items() if v.get("registered")
                ]
                return {"status": 200, "data": accounts}

        return {"status": 200, "data": {}}
    except Exception as e:
        print(f"Error: {e}")
        return {"data": {}, "status": 500, "error": str(e)}

# ==================================================================================================================================================================


# ==================================================================================================================================================================

# import requests

def upi_detail_fetcher(upi_id):
    url = f"https://upi-details-fetcher.p.rapidapi.com/find_upi_details/{upi_id}"
    headers = {
        'X-RapidAPI-Key': 'b95fd8411bmsh0848506b3e8609bp11583cjsnc7dd84f5f6ec',
        'X-RapidAPI-Host': 'upi-details-fetcher.p.rapidapi.com'
    }

    try:
        response = requests.get(url, headers=headers)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.content.decode()}")  # Print full response content for debugging

        if response.status_code == 200:
            return {'status': 200, 'data': response.json()}
        return {'status': response.status_code, 'data': {}}
    except Exception as e:
        return {'data': {}, 'status': 500, 'error': str(e)}

# # Example usage
# result = upi_detail_fetcher("rudalphgonsalves2003@oksbi")
# print(result)
# ==================================================================================================================================================================


# ==================================================================================================================================================================

import requests


def whatapp_lookup(number):
    url = f"https://whatsapp-data1.p.rapidapi.com/number/91{number}"
    headers = {
        "X-RapidAPI-Key": "90decbbf63mshb133bb71ebec1b1p11e2a8jsnaa7b6a355591",
        "X-RapidAPI-Host": "whatsapp-data1.p.rapidapi.com",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {"status": 200, "data": response.json()}
        return {"status": 200, "data": {}}
    except Exception as error:
        return {"data": {}, "status": 500, "error": str(error)}


# ==================================================================================================================================================================


# ==================================================================================================================================================================

# import requests

# def truecaller_detail_fetcher(number):
#     url = 'https://truecaller4.p.rapidapi.com/api/v1/getDetailsBulk'
#     params = {
#         'phone': number,
#         'countryCode': 'IN'
#     }
#     headers = {
#         'X-RapidAPI-Key': 'b95fd8411bmsh0848506b3e8609bp11583cjsnc7dd84f5f6ec',
#         'X-RapidAPI-Host': 'truecaller4.p.rapidapi.com'
#     }

#     try:
#         response = requests.get(url, params=params, headers=headers)
#         if response.status_code == 200:
#             return response.json()
#         return {}
#     except Exception as e:
#         return {'error': str(e)}

# def print_formatted_output(data_list):
#     if not data_list:
#         print("No data available")
#         return

#     for data in data_list:
#         print_entry(data)

# def print_entry(entry):
#     print("Name:", entry.get("name", ""))
#     print("Gender:", entry.get("gender", ""))
#     print("Image:", entry.get("image", ""))
#     print("Score:", entry.get("score", ""))
#     print("Access:", entry.get("access", ""))
#     print("Enhanced:", entry.get("enhanced", ""))
#     print("Phones:")
#     for phone in entry.get("phones", []):
#         print("\tE164 Format:", phone.get("e164Format", ""))
#         print("\tNumber Type:", phone.get("numberType", ""))
#         print("\tNational Format:", phone.get("nationalFormat", ""))
#         print("\tDialing Code:", phone.get("dialingCode", ""))
#         print("\tCountry Code:", phone.get("countryCode", ""))
#         print("\tCarrier:", phone.get("carrier", ""))
#         print("\tType:", phone.get("type", ""))
#     print("Addresses:")
#     for address in entry.get("addresses", []):
#         print("\tAddress:", address.get("address", ""))
#         print("\tCity:", address.get("city", ""))
#         print("\tCountry Code:", address.get("countryCode", ""))
#         print("\tTime Zone:", address.get("timeZone", ""))
#         print("\tType:", address.get("type", ""))
#     print("Internet Addresses:")
#     for internet_address in entry.get("internetAddresses", []):
#         print("\tID:", internet_address.get("id", ""))
#         print("\tService:", internet_address.get("service", ""))
#         print("\tCaption:", internet_address.get("caption", ""))
#         print("\tType:", internet_address.get("type", ""))
#     print("Badges:", entry.get("badges", []))
#     print("Tags:", entry.get("tags", []))
#     print("Sources:", entry.get("sources", []))
#     print("Search Warnings:", entry.get("searchWarnings", []))
#     print("Comments Stats:", entry.get("commentsStats", ""))
#     print("Manual Caller ID Prompt:", entry.get("manualCallerIdPrompt", ""))
#     print()

# # Example usage
# result = truecaller_detail_fetcher("9408974741")
# print_formatted_output(result.get("data", []))
# ==================================================================================================================================================================


def eyecon_detail_fetcher(country_code, number):
    url = "https://eyecon.p.rapidapi.com/api/v1/search"
    params = {"code": country_code, "number": number}
    headers = {
        "X-RapidAPI-Key": "b95fd8411bmsh0848506b3e8609bp11583cjsnc7dd84f5f6ec",
        "X-RapidAPI-Host": "eyecon.p.rapidapi.com",
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        return {"error": str(e)}


# ==================================================================================================================================================================

# import requests

# def eyecon_detail_fetcher(country_code, number):
#     url = 'https://eyecon.p.rapidapi.com/api/v1/search'
#     params = {
#         'code': country_code,
#         'number': number
#     }
#     headers = {
#         'X-RapidAPI-Key': 'b95fd8411bmsh0848506b3e8609bp11583cjsnc7dd84f5f6ec',
#         'X-RapidAPI-Host': 'eyecon.p.rapidapi.com'
#     }

#     try:
#         response = requests.get(url, params=params, headers=headers)
#         print(f"Response Status Code: {response.status_code}")
#         print(f"Response Content: {response.content.decode()}")  # Print full response content for debugging

#         if response.status_code == 200:
#             return response.json()
#         return {}
#     except Exception as e:
#         return {'error': str(e)}

# def print_formatted_output(data):
#     print("Eyecon Details:")
#     if data:
#         print("Status:", data.get("status", ""))
#         print("Message:", data.get("message", ""))
#         print("Timestamp:", data.get("timestamp", ""))
#         inner_data = data.get("data", {})
#         if inner_data:
#             print("Full Name:", inner_data.get("fullName", ""))
#             print("Other Names:", inner_data.get("otherNames", []))
#         else:
#             print("No inner data available")
#     else:
#         print("No data available")

# # Example usage
# result = eyecon_detail_fetcher('91', '7249735828')
# print_formatted_output(result)
# ==================================================================================================================================================================


def truecaller_detail_fetcher(number):
    url = "https://truecaller4.p.rapidapi.com/api/v1/getDetails"
    params = {"phone": number, "countryCode": "IN"}
    headers = {
        "X-RapidAPI-Key": "b95fd8411bmsh0848506b3e8609bp11583cjsnc7dd84f5f6ec",
        "X-RapidAPI-Host": "truecaller4.p.rapidapi.com",
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        return {"error": str(e)}
