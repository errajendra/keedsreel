from firebase_admin import auth


"""this method verify firebase uid"""
def verify_firebase_uid(firebase_uid):
    user = auth.get_user(firebase_uid)
    return user.uid
