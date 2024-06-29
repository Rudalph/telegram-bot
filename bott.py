import telebot
from alltrials import *
import firebase_admin
from firebase_admin import credentials
from telebot import types
from pdf_template import create_phone_pdf, generate_pdf_gmail
from auth import check_user_auth, decrement_credits
from constants import welcome_message, help_message, purchase_not_activated
from firebase_admin import credentials, firestore
from Api_Endpoints.ip_lookup import *
from Api_Endpoints.imei_lookup import imei_lookup
from Api_Endpoints.domain_lookup import dns_lookup
from Api_Endpoints.leak_check import leak_check
from Api_Endpoints.ifsc_code import ifsc_lookup
from Api_Endpoints.crypto_inves import crypto_inves
from Api_Endpoints.upi_lookup import upi_lookup
from Api_Endpoints.whois_lookup import whois_lookup

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
    msg = welcome_message(username, user_id)
    bot.send_message(message.chat.id, msg)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    comming_soon = ["cell_id", "nodal_search", "image_lookup", "vehicle_details","subdomain_lookup"]
    if call.data == "phone_osint":
        phone_osint_subitems(call)
    elif call.data == "email_osint":
        email_osint_subitems(call)
    elif call.data == "ip_lookup":
        ip_lookup_subitems(call)
    elif call.data == "vpn_proxy":
        msg = bot.send_message(
            call.message.chat.id, "Please enter a Valid Ip Address: "
        )
        bot.register_next_step_handler(msg, handle_vpn_proxy)
    elif call.data == "ip_investigation":
        msg = bot.send_message(
            call.message.chat.id, "Please enter a Valid Ip Address: "
        )
        bot.register_next_step_handler(msg, handle_ip_address_investigation)

    elif call.data == "imei_lookup":
        msg = bot.send_message(
            call.message.chat.id, "Please enter a Valid 15 digit IMEI number: "
        )
        bot.register_next_step_handler(msg, handle_imei_number)
    elif call.data == "full_osint":
        msg = bot.send_message(
            call.message.chat.id, "Please enter a 10-digit mobile number:"
        )
        bot.register_next_step_handler(msg, handle_complete_phone_number)
    elif call.data == "dns_lookup":
        msg = bot.send_message(call.message.chat.id, "Please enter a Domain Name :")
        bot.register_next_step_handler(msg, handle_dns_lookup)
    elif call.data == "gmail_data":
        msg = bot.send_message(call.message.chat.id, "Please enter a Valid Email ID :")
        bot.register_next_step_handler(msg, handle_email_data)
    elif call.data == "breached_email":
        msg = bot.send_message(call.message.chat.id, "Please enter a Valis Email ID: :")
        bot.register_next_step_handler(msg, handle_leak_check)
    elif call.data == "complete_email":
        msg = bot.send_message(call.message.chat.id, "Please enter a Valid Email ID: ")
        bot.register_next_step_handler(msg, handle_complete_email)
    elif call.data=="upi_accounts" or "upi_lookup":
        msg = bot.send_message(call.message.chat.id, "Please enter a Valid UPI ID / Phone Number: ")
        bot.register_next_step_handler(msg, handle_upi_lookup)         
    elif call.data == "domain_lookup":
        domain_lookup_subitems(call)
    elif call.data == "ifsc_search":
        msg = bot.send_message(call.message.chat.id, "Please enter a Valid IFSC Code: ")
        bot.register_next_step_handler(msg, handle_ifsc)
    elif call.data == "cryptocurrency":
        msg = bot.send_message(call.message.chat.id, "Please enter a Valid Hash: ")
        bot.register_next_step_handler(msg, hadle_crypto_inves)
    elif call.data == "whois_lookup":
        msg = bot.send_message(call.message.chat.id, "Please enter a Valid Domain : ")
        bot.register_next_step_handler(msg, handle_whois_lookup)
    elif call.data in comming_soon:
        bot.send_message(call.message.chat.id, "Comming Soon")
    elif call.data == "next_page":
        send_second_page(call)
    elif call.data == "previous_page":
        send_first_page(call.message)
    else:
        bot.answer_callback_query(call.id, f"Button {call.data} clicked!")


# def callback_inline(call):


def handle_complete_phone_number(message):
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
                upi_data = upi_lookup(number)

                bot.send_message(
                    message.chat.id,
                    "Generating Response....",
                )

                response_data = {
                    "Truecaller_data": truecaller_data,
                    "eyecon_data": eyecon_data,
                    "whatsapp_data": whatsapp_data,
                    "social_media_accounts": social_media_data,
                    "Upi_Data": upi_data,
                }

                create_phone_pdf(response_data)
                with open("user_data.pdf", "rb") as f:
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
        # msg = bot.send_message(
        # message.chat.id, "Invalid number. Please enter a 10-digit mobile number:"
        # )
        # phone_num_retries+=1
        # bot.register_next_step_handler(msg, handle_phone_number)
        handle_start(message)


def handle_complete_email(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    is_auth, user_data = check_user_auth(user_id, username)
    if is_auth:
        if user_data["credits"] > 0:
            email = message.text
            email_data = email_detail_fetcher(email)

            response_data = {
                "email": email_data,
            }

            generate_pdf_gmail(response_data)
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
    status, data = check_user_auth(user_id, username)

    if status:
        bot.send_message(
            message.chat.id,
            "Welcome To Rudrastra OSINT Bot \n For More Featrues Checkout: rudrastra.in",
        )
        send_first_page(message)
    else:
        msg = welcome_message(username, user_id)
        bot.send_message(message.chat.id, msg)


def send_first_page(message):
    options = [
        ("Phone Number OSINT", "phone_osint"),
        ("Email OSINT", "email_osint"),
        ("UPI/VPA Address Lookup", "upi_lookup"),
        ("IP Address LookUp", "ip_lookup"),
        ("Domain LookUp", "domain_lookup"),
        ("Crypto Investigation", "cryptocurrency"),
        ("Next Page", "next_page"),
    ]

    markup = types.InlineKeyboardMarkup(row_width=1)
    for text, callback in options:
        button = types.InlineKeyboardButton(text, callback_data=callback)
        markup.add(button)

    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)


def send_second_page(call):
    options = [
        ("IMEI Lookup", "imei_lookup"),
        ("Cell ID Decoder", "cell_id"),
        ("Nodal Officier Search", "nodal_search"),
        ("Image Location LookUp", "image_lookup"),
        ("Vehicle Details", "vehicle_details"),
        ("IFSC Code Search", "ifsc_search"),
        # (""),
        ("Previous Page", "previous_page"),
    ]

    markup = types.InlineKeyboardMarkup(row_width=1)
    for text, callback in options:
        button = types.InlineKeyboardButton(text, callback_data=callback)
        markup.add(button)

    bot.edit_message_text(
        "Second Page:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


def phone_osint_subitems(call):
    options = [
        ("Caller ID Search", "caller_id"),
        # ("LPG Data", "lpg_data"),
        ("UPI Accounts", "upi_accounts"),
        # ("Connected Dish TV providers", "dish_tv"),
        # ("Public Utility Lookup", "public_utility"),
        # ("MNP Lookup", "mnp_lookup"),
        ("Connected Social Accounts", "other_websites"),
        ("International Number Validator", "international_num"),
        ("Full OSINT Report/Deep Search", "full_osint"),
        ("Previous Page", "previous_page"),
    ]

    markup = types.InlineKeyboardMarkup(row_width=1)
    for text, callback in options:
        button = types.InlineKeyboardButton(text, callback_data=callback)
        markup.add(button)

    bot.edit_message_text(
        "Second Page:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


def ip_lookup_subitems(call):
    options = [
        ("VPN Proxy Detection", "vpn_proxy"),
        ("IP Address Investigation", "ip_investigation"),
        ("Previous Page", "previous_page"),
    ]

    markup = types.InlineKeyboardMarkup(row_width=1)
    for text, callback in options:
        button = types.InlineKeyboardButton(text, callback_data=callback)
        markup.add(button)

    bot.edit_message_text(
        "IP Lookup",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


def domain_lookup_subitems(call):
    options = [
        ("DNS Lookup", "dns_lookup"),
        ("Whois Lookup", "whois_lookup"),
        ("Subdomain Lookup", "subdomain_lookup"),
        ("Previous Page", "previous_page"),
    ]

    markup = types.InlineKeyboardMarkup(row_width=1)
    for text, callback in options:
        button = types.InlineKeyboardButton(text, callback_data=callback)
        markup.add(button)

    bot.edit_message_text(
        "Domain Lookup",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


def email_osint_subitems(call):
    options = [
        ("Gmail Data", "gmail_data"),
        ("Connected Social Accounts", "connected_social"),
        ("Breached Email Check", "breached_email"),
        ("Full OSINT Report / Deep Search", "complete_email"),
        ("Previous Page", "previous_page"),
    ]

    markup = types.InlineKeyboardMarkup(row_width=1)
    for text, callback in options:
        button = types.InlineKeyboardButton(text, callback_data=callback)
        markup.add(button)

    bot.edit_message_text(
        "Gmail OSINT:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


@bot.message_handler(commands=["checkcredits"])
def handle_check_credits(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    status, data = check_user_auth(user_id, username)
    if status:
        msg = bot.send_message(
            message.chat.id, f"""Your account have {data["credits"]} Credit Points."""
        )
        msg
        if data["credits"] == 0:
            bot.reply_to(msg, "You have low account balance please recharge")
    else:
        msg = welcome_message(username, user_id)
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["help"])
def reply_on_help(message):
    username = message.from_user.username
    msg = help_message(username)
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["purchase"])
def reply_on_purchase(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    status, data = check_user_auth(user_id, username)
    if status:
        msg = bot.send_message(
            message.chat.id,
            f"""Your account have {data["credits"]} Credit Points. \n 
            To Recharge your account go to https://www.rudrastra.in/register""",
        )
        msg
    else:
        msg = purchase_not_activated(username, user_id)
        bot.send_message(message.chat.id, msg)


def handle_vpn_proxy(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    is_auth, user_data = check_user_auth(user_id, username)

    if is_auth:
        if user_data["credits"] > 0:
            ipaddress = message.text
            ip_data = vpn_proxy_detection(ipaddress)

            data = format_dict(ip_data)

            bot.send_message(message.chat.id, data)
            bot.reply_to(
                message,
                "Here is the response with.",
            )

            # Decrement user credits
            decrement_credits(user_data)
        else:
            bot.reply_to(
                message, "You have no credits left. Please recharge your account."
            )
    else:
        bot.reply_to(message, "User not authenticated.")


def handle_ip_address_investigation(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    is_auth, user_data = check_user_auth(user_id, username)

    if is_auth:
        if user_data["credits"] > 0:
            ipaddress = message.text
            ip_data = ip_address_investigation(ipaddress)

            data = format_dict(ip_data)

            bot.send_message(message.chat.id, data)
            bot.reply_to(
                message,
                "Here is the response with.",
            )

            # Decrement user credits
            decrement_credits(user_data)
        else:
            bot.reply_to(
                message, "You have no credits left. Please recharge your account."
            )
    else:
        bot.reply_to(message, "User not authenticated.")


def handle_imei_number(message):
    if message.text.isdigit() and len(message.text) == 15:

        user_id = str(message.from_user.id)
        username = message.from_user.username
        is_auth, user_data = check_user_auth(user_id, username)

        if is_auth:
            if user_data["credits"] > 0:
                imei = message.text
                imei_data = imei_lookup(imei)

                # data =

                bot.send_message(message.chat.id, format_dict(imei_data))
                bot.reply_to(
                    message,
                    "Here is the response with IMEI Information.",
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
        handle_start(message)


# Function to Handle DNS LOOKUP SubItem Button.
def handle_dns_lookup(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    is_auth, user_data = check_user_auth(user_id, username)

    if is_auth:
        if user_data["credits"] > 0:
            domain = message.text
            domain_data = dns_lookup(domain)

            # data =
            # Seprate Dict Formatter for DNS LOOKUP.
            def format_dict_dns(d, indent=0):
                formatted = ""
                for key, value in d.items():
                    if isinstance(value, dict):
                        formatted += " " * indent + f"{key}:\n"
                        formatted += format_dict(value, indent + 4)
                    elif isinstance(value, list):
                        formatted += " " * indent + f"{key}:\n"
                        for item in value:
                            formatted += format_dict(item, indent + 4)
                    else:
                        formatted += " " * indent + f"{key}: {value}\n"
                return formatted

            bot.send_message(message.chat.id, format_dict_dns(domain_data))
            bot.reply_to(
                message,
                "Here is the response with Domain Information.",
            )

            # Decrement user credits
            decrement_credits(user_data)
        else:
            bot.reply_to(
                message, "You have no credits left. Please recharge your account."
            )
    else:
        bot.reply_to(message, "User not authenticated.")


def handle_leak_check(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    is_auth, user_data = check_user_auth(user_id, username)

    if is_auth:
        if user_data["credits"] > 0:
            email = message.text
            email_data = leak_check(email)

            # data =

            # bot.send_message(message.chat.id, format_dict(email_data))

            if email_data["success"]:
                source_details = "\n ".join(
                    [
                        f'{source.get("name",{})} ({source.get("date",{})})'
                        for source in email_data.get("sources", {})
                    ]
                )
                message_text = (
                    f"Email valid: {email_data['success']}\n"
                    f"Found: {email_data['found']}\n"
                    f"Fields: {', '.join(email_data['fields'])}\n"
                    f"Sources: {source_details}"
                )
                bot.send_message(message.chat.id, message_text)

                bot.reply_to(
                    message,
                    "Here is the response with Breach Information.",
                )
            else:
                bot.send_message(message.chat.id, "Your Mail is not Breached Anywhere")

            # Decrement user credits
            decrement_credits(user_data)
        else:
            bot.reply_to(
                message, "You have no credits left. Please recharge your account."
            )
    else:
        bot.reply_to(message, "User not authenticated.")


def handle_ifsc(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    is_auth, user_data = check_user_auth(user_id, username)

    if is_auth:
        if user_data["credits"] > 0:
            ifsc = message.text
            ifsc_data = ifsc_lookup(ifsc)

            # data =

            # source_details = "\n ".join([f'{source["name"]} ({source["date"]})' for source in email_data['sources']])

            # message_text = (
            #     f"Email valid: {email_data['success']}\n"
            #     f"Found: {email_data['found']}\n"
            #     f"Fields: {', '.join(email_data['fields'])}\n"
            #     f"Sources: {source_details}"
            # )
            # bot.send_message(message.chat.id, message_text)

            bot.send_message(message.chat.id, format_dict(ifsc_data))
            bot.reply_to(
                message,
                "Here is the response with Bank Information.",
            )

            # Decrement user credits
            decrement_credits(user_data)
        else:
            bot.reply_to(
                message, "You have no credits left. Please recharge your account."
            )
    else:
        bot.reply_to(message, "User not authenticated")


def hadle_crypto_inves(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    is_auth, user_data = check_user_auth(user_id, username)

    if is_auth:
        if user_data["credits"] > 0:
            hash = message.text
            hash_data = crypto_inves(hash)

            # data =

            # source_details = "\n ".join([f'{source["name"]} ({source["date"]})' for source in email_data['sources']])

            # message_text = (
            #     f"Email valid: {email_data['success']}\n"
            #     f"Found: {email_data['found']}\n"
            #     f"Fields: {', '.join(email_data['fields'])}\n"
            #     f"Sources: {source_details}"
            # )
            # bot.send_message(message.chat.id, message_text)

            bot.send_message(message.chat.id, format_dict(hash_data))
            bot.reply_to(
                message,
                "Here is the response with Transaction Information.",
            )

            # Decrement user credits
            decrement_credits(user_data)
        else:
            bot.reply_to(
                message, "You have no credits left. Please recharge your account."
            )
    else:
        bot.reply_to(message, "User not authenticated")


def handle_email_data(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    is_auth, user_data = check_user_auth(user_id, username)

    if is_auth:
        if user_data["credits"] > 0:
            email = message.text
            email_data = email_detail_fetcher(email)

            # data =
            bot.send_message(message.chat.id, format_dict(email_data))
            bot.reply_to(
                message,
                "Here is the response with Email Information.",
            )

            # Decrement user credits
            decrement_credits(user_data)
        else:
            bot.reply_to(
                message, "You have no credits left. Please recharge your account."
            )
    else:
        bot.reply_to(message, "User not authenticated")


def handle_whois_lookup(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    is_auth, user_data = check_user_auth(user_id, username)

    if is_auth:
        if user_data["credits"] > 0:
            domain = message.text
            domain_data = whois_lookup(domain)

            # data =
            bot.send_message(message.chat.id, format_dict(domain_data))
            bot.reply_to(
                message,
                "Here is the response with Domain Information.",
            )

            # Decrement user credits
            decrement_credits(user_data)
        else:
            bot.reply_to(
                message, "You have no credits left. Please recharge your account."
            )
    else:
        bot.reply_to(message, "User not authenticated")

def handle_upi_lookup(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    is_auth, user_data = check_user_auth(user_id, username)

    if is_auth:
        if user_data["credits"] > 0:
            vpa = message.text
            vpa_data = upi_lookup(vpa)

            # data =
            bot.send_message(message.chat.id, format_dict(vpa_data))
            bot.reply_to(
                message,
                "Here is the response with UPI Information.",
            )

            # Decrement user credits
            decrement_credits(user_data)
        else:
            bot.reply_to(
                message, "You have no credits left. Please recharge your account."
            )
    else:
        bot.reply_to(message, "User not authenticated")
        
def format_dict(d, indent=0):
    formatted = ""
    for key, value in d.items():
        if isinstance(value, dict):
            formatted += " " * indent + f"{key}:\n\n"
            formatted += format_dict(value, indent + 4)
        else:
            formatted += " " * indent + f"{key}: {value}\n\n"
    return formatted


bot.polling()
