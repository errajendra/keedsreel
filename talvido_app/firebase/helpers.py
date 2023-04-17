from firebase_admin import auth
from talvido_app.models import Talvidouser


"""this method verify firebase uid"""
def verify_firebase_uid(firebase_uid):
    user = auth.get_user(firebase_uid)
    return user.uid


"""this method get user from token"""
def get_user_from_token(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    id_token = auth_header.split(" ").pop()
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token.get("uid")
    user = Talvidouser.objects.get(firebase_uid=uid)
    return user
