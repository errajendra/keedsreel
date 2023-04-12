from .exceptions import *
from firebase_admin import credentials
import firebase_admin


"""intialize firebase credentials"""
cred = credentials.Certificate("talvido-4cf3f-firebase-adminsdk-u7p22-904989d192.json")
firebase_admin.initialize_app(cred)
