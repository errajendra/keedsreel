from rest_framework import status
from rest_framework.exceptions import APIException


class NoAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "error": {"token": "No authentication token provided"},
    }
    default_code = "no_auth_token"


class InvalidAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "error": {"token": "Invalid authentication token provided"},
    }
    default_code = "invalid_token"


class FirebaseError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "error": {
            "firebase_uid": "The user provided with the auth token is not a valid Firebase user, it has no Firebase UID"
        },
    }
    default_code = "no_firebase_uid"


class NoFirebaseuidAvaliable(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "error": {
            "firebase_uid": "The token associate with firebase uid is not avaliable in database"
        },
    }
    default_code = "no_firebase_uid_avaliable_in_database"


class InvalidFirebaseUID(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "error": {"firebase_uid": "This firebase uid is invalid"},
    }
    default_code = "invalid firebase uid"


class FirebaseUIDExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": "bad request",
        "error": {"firebase_uid": "Firebase uid is already exist"},
    }
    default_code = "Firebase uid is already exist"
