import os
import telebot
import requests
from fpdf import FPDF
from alltrials import (
    whatapp_lookup,
    social_media_accounts,
    eyecon_detail_fetcher,
    truecaller_detail_fetcher,
    upi_detail_fetcher,
)
from pdf_formatting import PDF
from PIL import Image
import tempfile
import firebase_admin
from firebase_admin import db, credentials

# Initialize Firebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://pallav-b64b6-default-rtdb.asia-southeast1.firebasedatabase.app/"
    },
)

# Changed Token to my Token
Token = "7339030817:AAFSKxPDo3Rayb0sZj6DA5brjJKRz4o45L8"
bot = telebot.TeleBot(Token)


def clean_text(text):
    if isinstance(text, (bool, int, float)):
        return str(text)
    # Replace problematic characters with a space
    return "".join(
        [char if len(char) == 1 and ord(char) < 128 else " " for char in text]
    )


def generate_pdf(data, filename="response.pdf"):
    pdf = PDF()
    pdf.header()
    pdf.add_page()

    # Truecaller Section
    pdf.chapter_title("Truecaller Details:")
    truecaller_data = data.get("truecaller", {})
    if isinstance(truecaller_data, dict):
        for key, value in truecaller_data.items():
            if key == "data" and isinstance(value, list):
                for entry in value:
                    cleaned_entry = {
                        clean_text(k): clean_text(v) for k, v in entry.items()
                    }
                    pdf.add_table(cleaned_entry)
            else:
                pdf.add_table({clean_text(key): clean_text(value)})

    # Eyecon Section
    pdf.chapter_title("Eyecon Details:")
    eyecon_data = data.get("eyecon", {})
    if isinstance(eyecon_data, dict):
        cleaned_eyecon_data = {
            clean_text(k): clean_text(v) for k, v in eyecon_data.items()
        }
        pdf.add_table(cleaned_eyecon_data)

    # WhatsApp Section


def generate_pdf(data, filename="response.pdf"):
    pdf = PDF()

    pdf.header()
    pdf.add_page()

    # Truecaller Section
    pdf.chapter_title("Truecaller Details:")
    truecaller_data = data.get("truecaller", {})
    if isinstance(truecaller_data, dict):
        for key, value in truecaller_data.items():
            if key == "data" and isinstance(value, list):
                for entry in value:
                    cleaned_entry = {
                        clean_text(k): clean_text(v) for k, v in entry.items()
                    }
                    pdf.add_table(cleaned_entry)
            else:
                pdf.add_table({clean_text(key): clean_text(value)})

    # Eyecon Section
    pdf.chapter_title("Eyecon Details:")
    eyecon_data = data.get("eyecon", {})
    if isinstance(eyecon_data, dict):
        cleaned_eyecon_data = {
            clean_text(k): clean_text(v) for k, v in eyecon_data.items()
        }
        pdf.add_table(cleaned_eyecon_data)

    # WhatsApp Section
    pdf.chapter_title("WhatsApp Details:")
    whatsapp_data = data.get("Whatsapp_data", {})
    if isinstance(whatsapp_data, dict):
        cleaned_whatsapp_data = {
            clean_text(k): clean_text(v) for k, v in whatsapp_data.items()
        }
        pdf.add_table(cleaned_whatsapp_data)

        # Render profilePic in WhatsApp section
        if (
            "data" in whatsapp_data
            and isinstance(whatsapp_data["data"], dict)
            and "profilePic" in whatsapp_data["data"]
        ):
            profile_pic_url = whatsapp_data["data"]["profilePic"]
            response = requests.get(profile_pic_url)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(response.content)
                    temp_file_path = temp_file.name

                # Convert image to PNG format
                image = Image.open(temp_file_path)
                png_file_path = "/tmp/temp.png"
                image.save(png_file_path, "PNG")

                # Get image dimensions
                img_width, img_height = image.size

                # Add PNG image to PDF
                pdf.image(png_file_path, x=10, y=pdf.y + 10, w=50)
                pdf.y += img_height + 10  # Adjust the y-coordinate for next content

                # Delete temporary files
                os.unlink(temp_file_path)
                os.unlink(png_file_path)

    # Social Media Section
    pdf.chapter_title("Social Media Details:")
    social_media_data = data.get("social_media_data", {})
    if isinstance(social_media_data, dict):
        for key, value in social_media_data.items():
            if key == "data" and isinstance(value, list):
                for entry in value:
                    cleaned_entry = {
                        clean_text(k): clean_text(v) for k, v in entry.items()
                    }
                    pdf.add_table(cleaned_entry)
            else:
                pdf.add_table({clean_text(key): clean_text(value)})

    # Output PDF content to memory
    pdf_content = pdf.output(dest="S").encode("latin-1")

    # Write PDF content to file
    with open(filename, "wb") as f:
        f.write(pdf_content)


def check_user_auth(user_id, username):
    ref = db.reference("users")
    users = ref.get()
    for user in users.values():
        if user.get("telegram_id") == user_id or user.get("username") == username:
            return True
    return False


@bot.message_handler(
    func=lambda message: message.text.isdigit() and len(message.text) == 10
)
def handle_phone_number(message):
    user_id = message.from_user.id
    username = message.from_user.username

    if check_user_auth(user_id, username):
        number = message.text
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        truecaller_data = truecaller_detail_fetcher(number)
        eyecon_data = eyecon_detail_fetcher("91", number)
        whatsapp_data = whatapp_lookup(number)
        social_media_data = social_media_accounts(number)
        upi_data = upi_detail_fetcher(number)

        response_data = {
            "truecaller": truecaller_data,
            "eyecon": eyecon_data,
            "Whatsapp_data": whatsapp_data,
            "social_media_data": social_media_data,
            "Upi_Data": upi_data,
        }

        generate_pdf(response_data)
        with open("response.pdf", "rb") as f:
            bot.send_document(message.chat.id, f)

        bot.reply_to(
            message, "Here is the PDF response with Truecaller and Eyecon details."
        )
    else:
        bot.reply_to(message, "User not authenticated.")


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.reply_to(message, "Please enter a 10-digit mobile number.")


bot.polling()
