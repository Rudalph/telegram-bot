import telebot
from alltrials import *
import firebase_admin
from firebase_admin import credentials
from telebot import types
from pdf_template import generate_pdf
from auth import check_user_auth, decrement_credits
from constants import welcome_message
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("cred_prod.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Change Token to your Token
Token = "6809147064:AAHJJ9WMPhcEmoF5JLSgksyxPZfkV-IZfQI"
bot = telebot.TeleBot(Token)


@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    status,data  = check_user_auth(user_id, username)
    if status:
        bot.send_message(message.chat.id, "Welcome")

        markup = types.InlineKeyboardMarkup(row_width=1)
        phone_osint_button = types.InlineKeyboardButton(
            "Phone Osint", callback_data="phone_osint"
        )
        email_osint_button = types.InlineKeyboardButton(
            "Email Osint", callback_data="email_osint"
        )

        markup.add(phone_osint_button, email_osint_button)
        bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)
    else:
        msg = welcome_message(username, user_id)
        bot.send_message(message.chat.id, msg)


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
        user_id = str(message.from_user.id)
        username = message.from_user.username
        is_auth, user_data = check_user_auth(user_id, username)

        if is_auth:
            if user_data["credits"] > 0:
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
                    message,
                    "Here is the PDF response with Truecaller and Eyecon details.",
                )

                # Decrement user credits
                decrement_credits(user_data)
            else:
                bot.reply_to(
                    message, "You have no credits left. Please recharge your account."
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
    is_auth, user_data = check_user_auth(user_id, username)

    if is_auth:
        if user_data["credits"] > 0:
            email = message.text
            email_data = email_detail_fetcher(email)

            response_data = {
                "email": email_data,
            }

            generate_pdf(response_data)
            with open("response.pdf", "rb") as f:
                bot.send_document(message.chat.id, f)

            bot.reply_to(message, "Here is the PDF response with email details.")

            # Decrement user credits
            decrement_credits(user_data)
        else:
            bot.reply_to(
                message, "You have no credits left. Please recharge your account."
            )
    else:
        bot.reply_to(message, "User not authenticated.")


@bot.message_handler(commands=["mainmenu"])
def handle_other_messages(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    status,data  = check_user_auth(user_id, username)
    if status:
        bot.send_message(message.chat.id, "Welcome")

        markup = types.InlineKeyboardMarkup(row_width=1)
        phone_osint_button = types.InlineKeyboardButton(
            "Phone Osint", callback_data="phone_osint"
        )
        email_osint_button = types.InlineKeyboardButton(
            "Email Osint", callback_data="email_osint"
        )

        markup.add(phone_osint_button, email_osint_button)
        bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)
    else:
        msg = welcome_message(username, user_id)
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["checkcredits"])
def handle_other_messages(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    status,data  = check_user_auth(user_id, username)
    if status:
        msg = bot.send_message(message.chat.id, f"""Your account have {data["credits"]} Credit Points.""")
        msg
        if data["credits"] == 0:
            bot.reply_to(msg, "You have low account balance please recharge")
    else:
        msg = welcome_message(username, user_id)
        bot.send_message(message.chat.id, msg)
bot.polling()
