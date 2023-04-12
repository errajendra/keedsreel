from rest_framework import status
from rest_framework.exceptions import APIException


class NoAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "No authentication token provided"
    default_code = "no_auth_token"


class InvalidAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid authentication token provided"
    default_code = "invalid_token"


class FirebaseError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "The user provided with the auth token is not a valid Firebase user, it has no Firebase UID"
    default_code = "no_firebase_uid"


class NoFirebaseuidAvaliable(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "The token associate with firebase uid is not avaliable in database"
    default_code = "no_firebase_uid_avaliable_in_database"


class InvalidFirebaseUID(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "This firebase uid is invalid"
    default_code = "invalid firebase uid"
