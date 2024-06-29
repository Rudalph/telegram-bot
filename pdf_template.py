from io import BytesIO
import json
import os
import tempfile
from PIL import Image
from fpdf import FPDF
import requests
from pdf_formatting import PDF

def clean_text(text):
    if isinstance(text, (bool, int, float)):
        return str(text)
    return "".join(
        [char if len(char) == 1 and ord(char) < 128 else " " for char in text]
    )


# def generate_pdf(data, filename="response.pdf"):
#     pdf = PDF()

#     pdf.header()
#     pdf.add_page()

#     # Truecaller Section
#     pdf.chapter_title("Truecaller Details:")
#     truecaller_data = data.get("truecaller", {})
#     if isinstance(truecaller_data, dict):
#         for key, value in truecaller_data.items():
#             if key == "data" and isinstance(value, list):
#                 for entry in value:
#                     cleaned_entry = {
#                         clean_text(k): clean_text(v) for k, v in entry.items()
#                     }
#                     pdf.add_table(cleaned_entry)
#             else:
#                 pdf.add_table({clean_text(key): clean_text(value)})

#     # Eyecon Section
#     pdf.chapter_title("Eyecon Details:")
#     eyecon_data = data.get("eyecon", {})
#     if isinstance(eyecon_data, dict):
#         cleaned_eyecon_data = {
#             clean_text(k): clean_text(v) for k, v in eyecon_data.items()
#         }
#         pdf.add_table(cleaned_eyecon_data)

#     # Social Media Section
#     pdf.chapter_title("Social Media Details:")
#     social_media_data = data.get("social_media_data", {})
#     if isinstance(social_media_data, dict):
#         for key, value in social_media_data.items():
#             if key == "data" and isinstance(value, list):
#                 for entry in value:
#                     cleaned_entry = {
#                         clean_text(k): clean_text(v) for k, v in entry.items()
#                     }
#                     pdf.add_table(cleaned_entry)
#             else:
#                 pdf.add_table({clean_text(key): clean_text(value)})
                
#     # WhatsApp Section
#     pdf.chapter_title("WhatsApp Details:")
#     whatsapp_data = data.get("Whatsapp_data", {})
#     if isinstance(whatsapp_data, dict):
#         cleaned_whatsapp_data = {
#             clean_text(k): clean_text(v) for k, v in whatsapp_data.items()
#         }
#         pdf.add_table(cleaned_whatsapp_data)

#         # Render profilePic in WhatsApp section
#         if (
#             "data" in whatsapp_data
#             and isinstance(whatsapp_data["data"], dict)
#             and "profilePic" in whatsapp_data["data"]
#         ):
#             profile_pic_url = whatsapp_data["data"]["profilePic"]
#             response = requests.get(profile_pic_url)
#             if response.status_code == 200:
#                 with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#                     temp_file.write(response.content)
#                     temp_file_path = temp_file.name

#                 # Convert image to PNG format
#                 image = Image.open(temp_file_path)
#                 png_file_path = "/tmp/temp.png"
#                 image.save(png_file_path, "PNG")

#                 # Get image dimensions
#                 img_width, img_height = image.size

#                 # Add PNG image to PDF
#                 pdf.image(png_file_path, x=10, y=pdf.y + 10, w=50)
#                 pdf.y += img_height + 10  # Adjust the y-coordinate for next content

#                 # Delete temporary files
#                 os.unlink(temp_file_path)
#                 os.unlink(png_file_path)

#     # Output PDF content to memory
#     pdf_content = pdf.output(dest="S").encode("latin-1")

#     # Write PDF content to file
#     with open(filename, "wb") as f:
#         f.write(pdf_content)

main_heading = "Rudrastra OSINT REPORT"
sub_heading = """NOTE: This report is strictly confidential and only for police officers.  
    Don't share it with anyone else or post it on WhatsApp, Telegram, or anywhere else public."""

from PIL import Image
def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.save(filename)


def create_phone_pdf(data):
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
    pdf.set_fill_color(173, 216, 230)  # Light blue color
    # pdf.rect(10, 10, 190, 20, 'F')  # Blue box for title background

    # Set font for title (bold, white)
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(190, 20, "Caller ID Search", 0, 1, "C", fill=True)
    pdf.set_font("Times", "B", 16)
    pdf.set_text_color(0, 0, 0)

    # First Name section
    pdf.cell(200, 10, txt="Names:", ln=True, align="L")
    first_names = set()
    if data.get("Truecaller_data", {}).get("status", False):
        for entry in data["Truecaller_data"].get("data", []):
            if "name" in entry:
                first_names.add(entry["name"])
    if data.get("eyecon_data", {}).get("status", False):
        if "fullName" in data["eyecon_data"].get("data", {}):
            first_names.add(data["eyecon_data"]["data"]["fullName"])
        for other_name in data["eyecon_data"].get("data", {}).get("otherNames", []):
            if "name" in other_name:
                first_names.add(other_name["name"])
    pdf.set_font("Times", "", 16)
    pdf.multi_cell(
        200, 10, txt=", \n".join(first_names) if first_names else "None", align="L"
    )
    pdf.ln(5)

    # Email section
    pdf.cell(200, 10, txt="Email:", ln=True, align="L")
    pdf.cell(200, 10, txt="None", ln=True, align="L")
    pdf.ln(5)

    # Address Section
    if data.get("Truecaller_data", {}).get("status", False):
        addresses = data.get("Truecaller_data", {}).get("data", [])[0].get("addresses", [])
        for i, address in enumerate(addresses, start=1):
            pdf.set_font("Times", "B", 16)
            pdf.multi_cell(300,10, f'Address {i}:', 0, "L")
            pdf.set_font("Times", "", 16)
            pdf.multi_cell(300,10, f'Address:   {address.get("address", "N/A")}', 0, "L")
            pdf.multi_cell(300,10, f'City:  {address.get("city", "N/A")}', 0, "L")
            pdf.multi_cell(300,10, f'Country Code:  {address.get("countryCode", "N/A")}', 0, "L")
            pdf.multi_cell(300,10, f'Time Zone: {address.get("timeZone", "N/A")}', 0, "L")
            pdf.multi_cell(300,10, f'Type:  {address.get("type", "N/A")}', 0, "L")
    pdf.ln(5)
    #UPI Section
    pdf.set_font("Times", "B", 22)
    pdf.set_text_color(255, 255, 255)

    pdf.cell(190, 20, "Linked UPI Accounts", 0, 1, "C", fill=True)
    pdf.set_font("Times", "", 16)
    pdf.set_text_color(0, 0, 0)

    upi_response = data.get("Upi_Data",{}).get('response2',{})
    for key, value in upi_response.items():
        pdf.multi_cell(300,10, f'{key}:   {value}', 0, "L")

    if data.get("Truecaller_data", {}).get("status", False):
        addresses = data.get("Truecaller_data", {}).get("data", [])[0].get("addresses", [])
        for i, address in enumerate(addresses, start=1):
            pdf.set_font("Times", "B", 16)
            pdf.multi_cell(300,10, f'Address {i}:', 0, "L")
            pdf.set_font("Times", "", 16)
            pdf.multi_cell(300,10, f'Address:   {address.get("address", "N/A")}', 0, "L")
            pdf.multi_cell(300,10, f'City:  {address.get("city", "N/A")}', 0, "L")
            pdf.multi_cell(300,10, f'Country Code:  {address.get("countryCode", "N/A")}', 0, "L")
            pdf.multi_cell(300,10, f'Time Zone: {address.get("timeZone", "N/A")}', 0, "L")
            pdf.multi_cell(300,10, f'Type:  {address.get("type", "N/A")}', 0, "L")
    pdf.ln(5)

    # Connected Social Media Apps section
    pdf.cell(190, 20, "Connected Social Media Apps", 0, 1, "C", fill=True)
    # pdf.cell(200, 10, txt="Connected Social Media Apps:", ln=True, align="L")
    pdf.set_fill_color(0, 0, 230)  # blue color
    pdf.cell(190, 10, "", 0, 1)
    #Whatsapp Details
    if data.get("whatsapp_data", {}).get("isWAContact", False):
        pdf.set_font("Times", "B", 22)
        pdf.set_text_color(255, 255, 255)

        pdf.cell(190, 20, "WhatsApp Details", 0, 1, "C", fill=True)
        pdf.image("whatsapp_logo.png", x=65, y=pdf.get_y()-15 , w=10)  # WhatsApp logo
        pdf.ln(5)
        # Stting Heading
        pdf.set_font("Times", "B", 16)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, txt="WhatsApp Details:", ln=True, align="L")
        pdf.ln(5)
        pdf.set_font("Times", "", 16)
        whatsapp_data = data.get("whatsapp_data", {})
        profile_pic_url = whatsapp_data.get("profilePic", "")

        if profile_pic_url:
            download_image(profile_pic_url, "profile_pic.jpg")
            pdf.image("profile_pic.jpg", x=150, y=pdf.get_y(), w=40)

        pdf.multi_cell(200, 10, f"Number: {whatsapp_data.get('number', 'N/A')}", 0, "L")
        pdf.multi_cell(200, 10, f"Phone: {whatsapp_data.get('phone', 'N/A')}", 0, "L")
        pdf.multi_cell(200, 10, f"Is Business: {whatsapp_data.get('isBusiness', 'N/A')}", 0, "L")
        pdf.multi_cell(200, 10, f"About: {whatsapp_data.get('about', 'N/A')}", 0, "L")
        pdf.ln(5)
    pdf.set_font("Times", "", 16)
    pdf.set_text_color(0, 0, 0)

    # Stting Heading
    pdf.set_font("Times", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(190, 20, "Other Social Media Apps", 0, 1, "C", fill=True)
    pdf.ln(5)
    pdf.set_font("Times", "", 16)
    pdf.set_text_color(0, 0, 0)
    #Other Social Media Details
    accounts = data["social_media_accounts"].get("data",{}).get("account_details",{})
    print(accounts)
    def convert_value(value):
        if value is False:
            return 'No'
        elif value is None:
            return 'None'
        else:
            return value
    for key, value in accounts.items():
        # Convert each value before adding to PDF
        if(key != "whatsapp"):
            formatted_value = {k: convert_value(v) for k, v in value.items()}
            formatted_value_str = json.dumps(formatted_value, indent=2, separators=(', ', ': '))[1:-1]

            # Add key and formatted value to PDF
            pdf.multi_cell(200, 10, txt=f"{key} : {formatted_value_str}")
            pdf.ln(10)



    pdf.ln(5)

    # Save the PDF with name 'user_data.pdf'
    pdf.output("user_data.pdf")


def generate_pdf_gmail(data_dict, filename="response.pdf"):
    pdf = PDF()
    pdf.header()
    pdf.add_page()
    pdf.chapter_title("Complete Email OSINT Report")

    # Add PROFILE_CONTAINER data
    pdf.add_table(data_dict["email"])
    pdf.ln()

    # Add Gmail Details section
    pdf.chapter_title("Gmail Details:")
    gmail_data = data_dict.get("gmail", {}).get("emails", {}).get("PROFILE", {})
    if gmail_data:
        pdf.add_table(gmail_data)
    else:
        pdf.multi_cell(0, 10, "No Gmail details found.")
    pdf.ln()

    # Output the PDF to a file
    # pdf.output("osint_report.pdf")

    pdf_content = pdf.output(dest="S").encode("latin-1")
    with open(filename, "wb") as f:
        f.write(pdf_content)