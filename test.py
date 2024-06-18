import firebase_admin
from firebase_admin import db, credentials

# Initialize Firebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://pallav-b64b6-default-rtdb.asia-southeast1.firebasedatabase.app/"
    },
)

ref = db.reference("User")
users = ref.get()
print(users)

def check_user_auth(user_id, username):
    for user in users.values():
        if user.get("id") == user_id or user.get("username") == username:
            return True
    return False

