# Send to user if user is not authenticated, on /Start
def welcome_message(username, user_id):
    return f"""
Welcome {username}

To get information about this bot, run the command /help.
To access the bot, you can use /mainmenu.
Consider joining our channel @Rudrastra for updates and queries.

your Telegram username: {username}.
If you are new to the bot, fill up this form https://www.rudrastra.in/register to activate yourself with your telegram user id: {user_id}

Demo Video: https://youtu.be/4DGvX4P_tQg?si=kKth08qFtCJb1HGW

Note: Sharing this video to another user who is not part of law enforcement is not allowed.
Note: All sales and payments are final. Any kind of refund is not applicable for any downtime, maintenance, service failure!
Feedback Link: 
        """


def help_message(username):
    return f"""
Welcome {username} to the Rudrastra OSINT bot.
This is made strictly for law enforcement officers only.
This bot provide various tools which can be used in investigation to solve cases.For the accessing the bot your account needs to be activated.For more info about bot join our channel @Rudrastra.
Note: All sales and payments are final. Any kind of refund is not applicable for any downtime, maintenance, service failure!

Feedback Link:-
        """


def purchase_not_activated(username, user_id):
    return f"""
You are not activated please fill up the form https://www.rudrastra.in/login.
Your telegram Username is {username}.
Your telegram userid is {user_id}.
If you are facing any problem Contact +91 84320 03083 on Whatsapp
"""
