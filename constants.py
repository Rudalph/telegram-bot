
# Send to user if user is not authenticated, on /Start
def welcome_message(username, user_id):
    return f"""
    Welcome {username}

    To get information about this bot, run the command /help.
    To access the bot, you can use /mainmenu.
    Consider joining our channel @Rudrastra for updates and queries.
    If you are new to the bot, fill up this form https://forms.gle/i4KVXYQzLRgL5SQh6 to activate yourself with your telegram user id: {user_id}

    Demo Video: https://www.youtube.com/watch?v=6lIysJOqF2E

    Note: Sharing this video to another user who is not part of law enforcement is not allowed.
    Note: All sales and payments are final. Any kind of refund is not applicable for any downtime, maintenance, service failure!
    Feedback Link: https://forms.gle/ivLzYr64sgDKorx67
        """

