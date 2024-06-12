from io import BytesIO
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
from PIL import Image
import tempfile

# Changed Token to my Token
Token = "7339030817:AAFSKxPDo3Rayb0sZj6DA5brjJKRz4o45L8"
bot = telebot.TeleBot(Token)


class PDF(FPDF):
    def add_header_to_first_page(pdf, logo_path, heading, subheading):
        # Set font for header
        pdf.set_font("Arial", "B", 12)

        # Set header background color
        pdf.set_fill_color(0, 0, 128)  # Navy blue

        # Add header to first page
        pdf.set_y(10)  # Set Y position for header
        pdf.cell(0, 10, "", 0, 1, "C", 1)  # Empty cell for background color
        pdf.set_y(10)  # Reset Y position for content
        pdf.set_x(10)  # Set X position for logo
        pdf.image(logo_path, x=10, y=10, w=20)
        pdf.set_x(40)  # Set X position for heading
        pdf.cell(0, 10, heading, 0, 0, "R")
        pdf.set_x(40)  # Set X position for subheading
        pdf.cell(0, 10, subheading, 0, 1, "R")

    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Response Details", 0, 1, "C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(5)

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_table(self, data, level=0):
        self.set_font("Arial", "", 12)
        for key, value in data.items():
            if isinstance(value, list):
                self.cell(0, 10, f"{key}:", 0, 1, "L")
                for item in value:
                    self.ln(5)
                    if isinstance(item, dict):
                        self.add_sub_table(item, level + 1)
                    else:
                        self.add_key_value(key, item, level + 1)
            elif isinstance(value, dict):
                self.cell(0, 10, f"{key}:", 0, 1, "L")
                self.add_sub_table(value, level + 1)
            else:
                self.add_key_value(key, value, level)

    def add_sub_table(self, sub_data, level):
        self.set_font("Arial", "", 12)
        for sub_key, sub_value in sub_data.items():
            if isinstance(sub_value, dict):
                self.cell(0, 10, f"{sub_key}:", 0, 1, "L")
                self.add_sub_table(sub_value, level + 1)
            elif isinstance(sub_value, list):
                self.cell(0, 10, f"{sub_key}:", 0, 1, "L")
                for item in sub_value:
                    self.ln(5)
                    if isinstance(item, dict):
                        self.add_sub_table(item, level + 1)
                    else:
                        self.add_key_value(sub_key, item, level + 1)
            else:
                self.add_key_value(sub_key, sub_value, level)

    def add_key_value(self, key, value, level):
        indent = " " * (level * 4)
        self.cell(50, 10, f"{indent}{key}", 1)
        self.cell(140, 10, f"{value}", 1)
        self.ln()

    def add_image(self, url):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img_path = "temp_image.png"
            img.save(img_path)
            self.image(img_path, x=10, w=100)
        except Exception as e:
            self.cell(0, 10, f"Error loading image: {e}", 0, 1, "L")


def generate_pdf(data, filename="response.pdf"):
    pdf = PDF()
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


pdf = FPDF()
pdf.add_page()

heading = "Rudrastra OSINT REPORT"
subheading = """NOTE : This report is strictly confidential and only for police officers. Don't
share it with anyone else or post it on WhatsApp, Telegram, or anywhere
else public."""
add_header_to_first_page = (
    "/home/pallav/Documents/GitHub/telegram-bot/response.pdf",
    "/home/pallav/Documents/GitHub/telegram-bot/logo.png",
    heading,
    subheading,
)
pdf.output("output.pdf")


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
