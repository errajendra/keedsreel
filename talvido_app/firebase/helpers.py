from firebase_admin import auth
import requests


"""this method verify firebase uid"""
def verify_firebase_uid(firebase_uid):
    user = auth.get_user(firebase_uid)
    return user.uid


"""generate firebase token for user"""
def generate_firebase_token(email,password):
    url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyAAFVJZkY2c_5RXCUoqrcuLacXFvsjEshk"
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(data=data, url=url)
    return response
