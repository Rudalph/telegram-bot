import os
from flask import Flask, request, send_file, jsonify
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

app = Flask(__name__)


def clean_text(text):
    if isinstance(text, (bool, int, float)):
        return str(text)
    # Replace problematic characters with a space
    return ''.join([char if len(char) == 1 and ord(char) < 128 else ' ' for char in text])


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
                    cleaned_entry = {clean_text(k): clean_text(v) for k, v in entry.items()}
                    pdf.add_table(cleaned_entry)
            else:
                pdf.add_table({clean_text(key): clean_text(value)})

    # Eyecon Section
    pdf.chapter_title("Eyecon Details:")
    eyecon_data = data.get("eyecon", {})
    if isinstance(eyecon_data, dict):
        cleaned_eyecon_data = {clean_text(k): clean_text(v) for k, v in eyecon_data.items()}
        pdf.add_table(cleaned_eyecon_data)

    # WhatsApp Section
    pdf.chapter_title("WhatsApp Details:")
    whatsapp_data = data.get("Whatsapp_data", {})
    if isinstance(whatsapp_data, dict):
        cleaned_whatsapp_data = {clean_text(k): clean_text(v) for k, v in whatsapp_data.items()}
        pdf.add_table(cleaned_whatsapp_data)

        # Render profilePic in WhatsApp section
        if "data" in whatsapp_data and isinstance(whatsapp_data["data"], dict) and "profilePic" in whatsapp_data["data"]:
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
                    cleaned_entry = {clean_text(k): clean_text(v) for k, v in entry.items()}
                    pdf.add_table(cleaned_entry)
            else:
                pdf.add_table({clean_text(key): clean_text(value)})

    # Output PDF content to memory
    pdf_content = pdf.output(dest='S').encode('latin-1')

    # Write PDF content to file
    with open(filename, "wb") as f:
        f.write(pdf_content)


@app.route('/fetch-details', methods=['POST'])
def fetch_details():
    number = request.form.get('number')
    if not number or not number.isdigit() or len(number) != 10:
        return jsonify({"error": "Invalid phone number"}), 400

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
    return send_file("response.pdf", as_attachment=True)


@app.route('/')
def index():
    return '''
    <form method="post" action="/fetch-details">
        <label for="number">Enter 10-digit mobile number:</label>
        <input type="text" id="number" name="number" required>
        <button type="submit">Submit</button>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)