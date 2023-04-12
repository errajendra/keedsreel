from rest_framework.authentication import BaseAuthentication
from firebase_admin import credentials, auth
from .import (
    NoAuthToken,
    InvalidAuthToken,
    FirebaseError,
    NoFirebaseuidAvaliable
)
from talvido_app.models import Talvidouser


"""FIREBASE AUTHENTICATION"""

class FirebaseAuthentication(BaseAuthentication):
    """override authenticate method and write our custom firebase authentication."""
    def authenticate(self, request):
        """Get the authorization Token, It raise exception when no authorization Token is given"""
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header:
            raise NoAuthToken("No auth token provided")
        
        """Decoding the Token It rasie exception when decode failed."""
        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid auth token")
        
        """Return Nothing"""
        if not id_token or not decoded_token:
            return None
        
        """Get the uid of an user"""
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()
        
        try:
            user = Talvidouser.objects.get(username=uid)
        except Talvidouser.DoesNotExist:
            raise NoFirebaseuidAvaliable("token associate with firebase uid is not avaliable in database")

        return (user,None)
