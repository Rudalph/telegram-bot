import telebot
import requests
from fpdf import FPDF

Token = "7434349510:AAG-vbjmpdsy5Hp4MPuVbxfyMrqxiPPhyMI"
bot = telebot.TeleBot(Token)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Demo PDF', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def truecaller_detail_fetcher(number):
    url = 'https://truecaller4.p.rapidapi.com/api/v1/getDetails'
    params = {
        'phone': number,
        'countryCode': 'IN'
    }
    headers = {
        'X-RapidAPI-Key': 'b95fd8411bmsh0848506b3e8609bp11583cjsnc7dd84f5f6ec',
        'X-RapidAPI-Host': 'truecaller4.p.rapidapi.com'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        return {'error': str(e)}

def eyecon_detail_fetcher(country_code, number):
    url = 'https://eyecon.p.rapidapi.com/api/v1/search'
    params = {
        'code': country_code,
        'number': number
    }
    headers = {
        'X-RapidAPI-Key': 'b95fd8411bmsh0848506b3e8609bp11583cjsnc7dd84f5f6ec',
        'X-RapidAPI-Host': 'eyecon.p.rapidapi.com'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        return {'error': str(e)}

def generate_pdf(data, filename='response.pdf'):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title('Response Details')
    pdf.chapter_body(f'Truecaller Details: {data["truecaller"]}')
    pdf.chapter_body(f'Eyecon Details: {data["eyecon"]}')
    pdf.output(filename)

@bot.message_handler(func=lambda message: message.text.isdigit() and len(message.text) == 10)
def handle_phone_number(message):
    number = message.text
    truecaller_data = truecaller_detail_fetcher(number)
    eyecon_data = eyecon_detail_fetcher('91', number)

    response_data = {
        'truecaller': truecaller_data,
        'eyecon': eyecon_data
    }

    generate_pdf(response_data)
    with open('response.pdf', 'rb') as f:
        bot.send_document(message.chat.id, f)

    bot.reply_to(message, "Here is the PDF response with Truecaller and Eyecon details.")

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.reply_to(message, "Please enter a 10-digit mobile number.")

bot.polling()
