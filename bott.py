import telebot
from alltrials import (
    whatapp_lookup,
    social_media_accounts,
    eyecon_detail_fetcher,
    truecaller_detail_fetcher,
    upi_detail_fetcher,
    email_detail_fetcher,
)
import firebase_admin
from firebase_admin import db, credentials
from telebot import types
from pdf_template import generate_pdf

# Initialize Firebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://pallav-b64b6-default-rtdb.asia-southeast1.firebasedatabase.app/"
    },
)

# Changed Token to my Token
Token = "6809147064:AAHJJ9WMPhcEmoF5JLSgksyxPZfkV-IZfQI"
bot = telebot.TeleBot(Token)




def check_user_auth(user_id, username):
    ref = db.reference("User")
    users = ref.get()
    if users is None:
        print("No users found in the database.")
        return False
    for user in users:
        if user.get("id") == user_id or user.get("username") == username:
            return True
    return False


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "phone_osint":
        msg = bot.send_message(
            call.message.chat.id, "Please enter a 10-digit mobile number:"
        )
        bot.register_next_step_handler(msg, handle_phone_number)

    elif call.data == "email_osint":
        msg = bot.send_message(call.message.chat.id, "Please enter a valid Email Id:")
        bot.register_next_step_handler(msg, handle_email)


def handle_phone_number(message):
    if message.text.isdigit() and len(message.text) == 10:
        user_id = message.from_user.id
        username = message.from_user.username
        if check_user_auth(user_id, username):
            number = message.text
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
    else:
        msg = bot.send_message(
            message.chat.id, "Invalid number. Please enter a 10-digit mobile number:"
        )
        bot.register_next_step_handler(msg, handle_phone_number)


def handle_email(message):
    user_id = message.from_user.id
    username = message.from_user.username
    if check_user_auth(user_id, username):
        email = message.text
        email_data = email_detail_fetcher(email)

        response_data = {
            "email": email_data,
        }

        generate_pdf(response_data)
        with open("response.pdf", "rb") as f:
            bot.send_document(message.chat.id, f)

        bot.reply_to(message, "Here is the PDF response with email details.")
    else:
        bot.reply_to(message, "User not authenticated.")


@bot.message_handler()
def handle_other_messages(message):
    bot.send_message(message.chat.id, 'Welcome')

    markup = types.InlineKeyboardMarkup(row_width=1)
    iron = types.InlineKeyboardButton('Phone Osint', callback_data='phone_osint')

    cotton = types.InlineKeyboardButton('Email Osint', callback_data="email_osint")
    
    markup.add(iron, cotton)
    # Send the message with the inline keyboard
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)


bot.polling()
