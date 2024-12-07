# from PDF.pdf_formatting import PDF
from fpdf import FPDF
data = {
    "Truecaller_data": {
        "status": True,
        "data": [
            {
                "name": "Pallav Vaniya",
                "phones": [
                    {
                        "e164Format": "+919408974741",
                        "numberType": "MOBILE",
                        "nationalFormat": "094089 74741",
                        "dialingCode": 91,
                        "countryCode": "IN",
                        "carrier": "BSNL",
                        "type": "openPhone",
                    }
                ],
                "addresses": [
                    {
                        "address": "IN",
                        "city": "Gujarat",
                        "countryCode": "IN",
                        "timeZone": "+05:30",
                        "type": "address",
                    }
                ],
            }
        ],
    },
    "eyecon_data": {
        "status": True,
        "message": "Success",
        "timestamp": 1719654603126,
        "data": {
            "fullName": "Dhirajlal Vaniya Ten Chemical",
            "otherNames": [
                {"name": "Dhiru Bombay", "type": ""},
                {"name": "Ridhi Shah", "type": ""},
                {"name": "Dhiraj Vania", "type": ""},
            ],
        },
    },
    "whatsapp_data": {
        "id": {
            "server": "c.us",
            "user": "919408974741",
            "_serialized": "919408974741@c.us",
        },
        "number": "919408974741",
        "isBusiness": False,
        "labels": [],
        "type": "in",
        "isMe": False,
        "isUser": True,
        "isGroup": False,
        "isWAContact": True,
        "isMyContact": False,
        "isBlocked": False,
        "profilePic": "https://pps.whatsapp.net/v/t61.24694-24/367555120_210530571776920_4035442803451311132_n.jpg?ccb=11-4&oh=01_Q5AaINyRbt9-vnj489fJLv7gKqZGSAATgWS32B_BZeVC9hik&oe=668CDFE3&_nc_sid=e6ed6c&_nc_cat=106",
        "about": "There is no place like 127.0.0.1",
        "countryCode": "IN",
        "phone": "+91 94089 74741",
    },
    "social_media_accounts": {
        "success": True,
        "data": {
            "number": 36200130525,
            "valid": True,
            "disposable": False,
            "type": "mobile",
            "country": "HU",
            "carrier": "Yettel Hungary",
            "score": 4,
            "account_details": {
                "facebook": {"registered": False},
                "google": {"registered": False, "account_id": None, "full_name": None},
                "twitter": {"registered": False},
                "instagram": {"registered": False},
                "yahoo": {"registered": None},
                "microsoft": {"registered": False},
                "snapchat": {"registered": False},
                "skype": {
                    "registered": False,
                    "age": None,
                    "city": None,
                    "bio": None,
                    "country": None,
                    "gender": None,
                    "language": None,
                    "name": None,
                    "handle": None,
                    "id": None,
                    "photo": None,
                    "state": None,
                },
                "whatsapp": {
                    "registered": False,
                    "photo": None,
                    "last_seen": None,
                    "about": None,
                    "last_active": None,
                },
                "telegram": {"registered": None, "photo": None, "last_seen": None},
                "viber": {"registered": None, "photo": None, "last_seen": None, "name": None},
                "kakao": {"registered": None},
                "ok": {"registered": False, "age": None},
                "zalo": {"registered": False, "date_of_birth": None, "name": None, "uid": None},
                "line": {"registered": None, "name": None, "photo": None},
                "flipkart": {"registered": False},
                "bukalapak": {"registered": False},
                "jdid": {"registered": None},
                "altbalaji": {"registered": False},
                "shopclues": {"registered": False},
                "snapdeal": {"registered": None},
                "tiki": {"registered": False},
                "vkontakte": {"registered": False},
                "weibo": {"registered": False},
            },
        },
    },
}

main_heading = "Rudrastra OSINT REPORT"
sub_heading = """NOTE: This report is strictly confidential and only for police officers.  
    Don't share it with anyone else or post it on WhatsApp, Telegram, or anywhere else public."""


def generate_pdf(data, filename="truecaller_data.pdf"):
    pdf = FPDF()
    pdf.add_page()
    # pdf.page_no() == 1:
    pdf.set_fill_color(0, 150, 255)  # Navy blue
    pdf.rect(0, 0, 210, 20, "F")
    # pdf.set_y(10)
    pdf.set_font("Arial", "B", 12)
    pdf.image("logo.png", 10, 5, 20)
    pdf.set_text_color(255, 255, 255)  # White
    pdf.cell(0, 10, main_heading, 0, 1, "C", fill=False)
    pdf.set_text_color(0, 0, 0)  # White
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 10, sub_heading, 0, "C", fill=False)
    pdf.ln(10)
    # padding = 20
    # pdf.set_xy(padding, 40)
    # Add a page
    # pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Set background color for the "Truecaller Details" section
    pdf.set_fill_color(173, 216, 230)  # Light blue color
    # pdf.rect(10, 10, 190, 20, 'F')  # Blue box for title background

    # Set font for title (bold, white)
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(190, 20, "Truecaller Details", 0, 1, "C", fill=True)

    # Reset fill color for the rest of the content
    pdf.set_fill_color(255, 255, 255)  # White color

    # Set padding
    # Set font for key-value pairs (regular, black)
    pdf.set_font("Times", "", 12)
    pdf.set_text_color(255, 0, 0)
    pdf.set_text_color(0, 0, 255)
    pdf.set_font("Times", "B", 18)
    pdf.cell(300,10,f"Basic Information: ")
    # Set font for key-value pairs (regular, black)
    pdf.set_font("Times", "B", 16)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(100, 10, f'Timestamp: {data.get("timestamp", "N/A")}', 0, "L")
        # Accessing the first element of "data" list and then using .get() method
    pdf.multi_cell(300,10, f'Telegram Id: {(data["data"][0].get("id", "N/A") if data["data"] else "N/A")}', 0, "L")
    pdf.multi_cell(300,10, f'Name: {(data["data"][0].get("name", "N/A") if data["data"] else "N/A")}', 0, "L")
    pdf.multi_cell(300,10, f'Gender: {(data["data"][0].get("gender", "N/A") if data["data"] else "N/A")}', 0, "L")
    pdf.multi_cell(300,10, f'Score: {(data["data"][0].get("score", "N/A") if data["data"] else "N/A")}', 0, "L")
    pdf.multi_cell(300,10, f'Access: {(data["data"][0].get("access", "N/A") if data["data"] else "N/A")}', 0, "L")
    pdf.multi_cell(300,10, f'Enhanced: {(data["data"][0].get("enhanced", "N/A") if data["data"] else "N/A")}', 0, "L")
    pdf.multi_cell(100,5)

    # Handle lists or nested structures if needed
    pdf.multi_cell(10,20)
    pdf.set_text_color(0, 0, 255)
    pdf.set_font("Times", "B", 22)
    pdf.cell(300,10,f"Phone Information ")
    # Set font for key-value pairs (regular, black)
    pdf.set_font("Times", "B", 16)
    pdf.set_text_color(0, 0, 0)


    phones = data["data"][0].get("phones", [])
    for i, phone in enumerate(phones, start=1):
        pdf.set_font("Times", "B", 16)
        pdf.set_text_color(255, 0, 0)
        pdf.multi_cell(300,10, f'Phone {i}:', 0, "L")
        pdf.set_font("Times", "", 16)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(300,10, f'e164-Format:    {phone.get("e164Format", "N/A")}', 0, "L")
        pdf.multi_cell(300,10, f'Number Type:    {phone.get("numberType", "N/A")}', 0, "L")
        pdf.multi_cell(300,10, f'National Format:    {phone.get("nationalFormat", "N/A")}', 0, "L")
        pdf.multi_cell(300,10, f'Dialing Code:   {phone.get("dialingCode", "N/A")}', 0, "L")
        pdf.multi_cell(300,10, f'Country Code:   {phone.get("countryCode", "N/A")}', 0, "L")
        pdf.multi_cell(300,10, f'Carrier:   {phone.get("carrier", "N/A")}', 0, "L")
        pdf.multi_cell(300,10, f'Type:  {phone.get("type", "N/A")}', 0, "L")

    pdf.multi_cell(100,5)


    pdf.multi_cell(10,20)
    pdf.set_text_color(0, 0, 255)
    pdf.set_font("Times", "B", 22)
    pdf.cell(300,10,f"Address Information ")
    # Set font for key-value pairs (regular, black)
    pdf.set_font("Times", "", 16)
    pdf.set_text_color(0, 0, 0)


    addresses = data["data"][0].get("addresses", [])
    for i, address in enumerate(addresses, start=1):
        pdf.multi_cell(300,10, f'Address {i}:', 0, "L")
        pdf.multi_cell(300,10, f'Address:   {address.get("address", "N/A")}', 0, "L")
        pdf.multi_cell(300,10, f'City:  {address.get("city", "N/A")}', 0, "L")
        pdf.multi_cell(300,10, f'Country Code:  {address.get("countryCode", "N/A")}', 0, "L")
        pdf.multi_cell(300,10, f'Time Zone: {address.get("timeZone", "N/A")}', 0, "L")
        pdf.multi_cell(300,10, f'Type:  {address.get("type", "N/A")}', 0, "L")


        # Output key-value pairs
    # if data.get("status", False):
    #     for key, value in data.items():
    #         if isinstance(value, list):
    #             for item in value:
    #                 for k, v in item.items():
    #                     pdf.cell(100, 10, f"{k}:", 0, 0)
    #                     pdf.set_text_color(255, 0, 0)
    #                     pdf.multi_cell(100, 10, str(v), 0, "L")
    #         else:
    #             pdf.cell(100, 10, f"{key}:", 0, 0, "L")
    #             pdf.set_text_color(0, 0, 0)
    #             pdf.multi_cell(100, 10, str(value), 0, "L")

    # Save the pdf with name "Truecaller_Details.pdf"
    pdf.output("Truecaller_Details.pdf")


generate_pdf(data)
