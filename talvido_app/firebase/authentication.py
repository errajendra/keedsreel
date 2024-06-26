from rest_framework.authentication import BaseAuthentication
from firebase_admin import auth
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
            auth_header = request.META.get("HTTP_AUTH")
            if not auth_header:
                raise NoAuthToken()
        
        """Decoding the Token It rasie exception when decode failed."""
        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken()
        
        """Return Nothing"""
        if not id_token or not decoded_token:
            return None
        
        """Get the uid of an user"""
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()

        """checking firebase uid is avalible in database"""
        try:
            user = Talvidouser.objects.get(firebase_uid=uid)
        except Talvidouser.DoesNotExist:
            raise NoFirebaseuidAvaliable()

        return (user,None)
