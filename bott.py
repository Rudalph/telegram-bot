import os
from tkinter import Image
import telebot
import requests
from fpdf import FPDF
from alltrials import (
    whatapp_lookup,
    social_media_accounts,
    eyecon_detail_fetcher,
    truecaller_detail_fetcher,
)
from pdf_formatting import PDF
from PIL import Image
import tempfile

# Changed Token to my Token
Token = "7339030817:AAFSKxPDo3Rayb0sZj6DA5brjJKRz4o45L8"
bot = telebot.TeleBot(Token)


def generate_pdf(data, filename="response.pdf"):
    pdf = PDF()

    pdf = PDF()
    # pdf.set_header_info(
    #     "/home/pallav/Documents/GitHub/telegram-bot/logo.png",
    #     "Rudrastra OSINT REPORT",
    #     """NOTE: This report is strictly confidential and only for police officers. 
    #     Don't share it with anyone else or post it on WhatsApp, Telegram, or anywhere else public.""",
    # )
    # pdf.add_page()

    pdf.add_page()
    # Truecaller Section
    pdf.chapter_title("Truecaller Details:")
    truecaller_data = data["truecaller"]
    for key, value in truecaller_data.items():
        if key == "data":
            for entry in value:
                pdf.add_table(entry)
        else:
            pdf.add_table({key: value})

    # Eyecon Section
    pdf.chapter_title("Eyecon Details:")
    eyecon_data = data["eyecon"]
    pdf.add_table(eyecon_data)

    # WhatsApp Section
    pdf.chapter_title("WhatsApp Details:")
    whatsapp_data = data["Whatsapp_data"]
    pdf.add_table(whatsapp_data)

    # Render profilePic in WhatsApp section
    if "data" in whatsapp_data and "profilePic" in whatsapp_data["data"]:
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

        pdf.output(filename)


@bot.message_handler(
    func=lambda message: message.text.isdigit() and len(message.text) == 10
)
def handle_phone_number(message):
    number = message.text
    truecaller_data = truecaller_detail_fetcher(number)
    eyecon_data = eyecon_detail_fetcher("91", number)
    whatsapp_data = whatapp_lookup(number)
    social_media_data = social_media_accounts(number)

    response_data = {
        "truecaller": truecaller_data,
        "eyecon": eyecon_data,
        "Whatsapp_data": whatsapp_data,
        "social_media_data": social_media_data,
    }

    generate_pdf(response_data)
    with open("response.pdf", "rb") as f:
        bot.send_document(message.chat.id, f)

    bot.reply_to(
        message, "Here is the PDF response with Truecaller and Eyecon details."
    )


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.reply_to(message, "Please enter a 10-digit mobile number.")


bot.polling()
