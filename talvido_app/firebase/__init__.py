from .exceptions import *
from firebase_admin import credentials
import firebase_admin


"""intialize firebase credentials"""
cred = credentials.Certificate("kidsreel-c7df8-firebase-adminsdk-9yb5t-9aaeea5cff.json")
firebase_admin.initialize_app(cred)
