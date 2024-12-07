import firebase_admin
from firebase_admin import credentials, firestore

# Chatbot Collection Schema Important Fields

#   username: String
#   telegramId: number
#   credits: number


def check_user_auth(user_id, username):
    db_collection = "chatbot"
    db = firestore.client()
    users_ref = db.collection(db_collection)
    users = users_ref.stream()
    if not users:
        print("No users found in the database.")
        return False, None

    for user in users:
        user_data = user.to_dict()
        if (
            user_data["telegramId"] == user_id
            and user_data["telegramusername"] == username
        ):
            return True, user_data
    return False, None


def decrement_credits(user_data):
    db_collection = "chatbot"

    db = firestore.client()
    doc_ref = db.collection(db_collection).get()
    for doc in doc_ref:
        if (
            doc.to_dict()["telegramusername"] == user_data["telegramusername"]
            and doc.to_dict()["telegramId"] == user_data["telegramId"]
        ) and doc.to_dict()["credits"] > 0:
            key = doc.id
            db.collection(db_collection).document(key).update(
                {"credits": firestore.Increment(-1)}
            )
            return True
    return False
