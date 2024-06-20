import os
import tempfile
from PIL import Image
import requests
from pdf_formatting import PDF

def clean_text(text):
    if isinstance(text, (bool, int, float)):
        return str(text)
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

    # Output PDF content to memory
    pdf_content = pdf.output(dest="S").encode("latin-1")

    # Write PDF content to file
    with open(filename, "wb") as f:
        f.write(pdf_content)
