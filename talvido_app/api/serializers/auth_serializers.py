from rest_framework import serializers
from talvido_app.models import Talvidouser
from django.conf import settings
from talvido_app.firebase.helpers import (
    verify_firebase_uid,
    generate_firebase_token,
    send_reset_password_email,
)
from talvido_app.firebase.exceptions import InvalidFirebaseUID, FirebaseUIDExists
from django.contrib.auth.hashers import make_password
import requests
import re
from firebase_admin import auth
from rest_framework import status


"""Mobile registration serializer"""

class TalvidoMobileRegisterSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField()

    class Meta:
        model = Talvidouser
        fields = ["mobile_number", "firebase_uid", "referral_code", "login_with"]

    """validate the mobile number"""

    def validate_mobile_number(self, value):
        validate_phone_number_pattern = "^\\+?[1-9][0-9]{9,14}$"
        if not re.match(validate_phone_number_pattern, value):
            raise serializers.ValidationError(
                """Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."""
            )
        return value

    """override the create method and verfying the valid firebase uid"""

    def create(self, validated_data):
        try:
            """verifying the firebase uid"""
            verify_firebase_uid(firebase_uid=validated_data.get("firebase_uid"))
        except:
            raise InvalidFirebaseUID()
        return super().create(validated_data)


"""mobile login serialzier"""

class TalvidoMobileLoginSerializer(serializers.Serializer):

    """Required fields"""

    firebase_uid = serializers.CharField()
    mobile_number = serializers.CharField()

    """validate the mobile number"""

    def validate_mobile_number(self, value):
        validate_phone_number_pattern = "^\\+?[1-9][0-9]{9,14}$"
        if not re.match(validate_phone_number_pattern, value):
            raise serializers.ValidationError(
                """Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."""
            )
        return value

    """validate firebase uid"""

    def validate_firebase_uid(self, value):
        try:
            """verifying the firebase uid"""
            verify_firebase_uid(firebase_uid=value)
        except:
            raise InvalidFirebaseUID()
        return value

    """checking credentails"""

    def check_credentials(self, firebase_uid, mobile_number):
        user = Talvidouser.objects.filter(
            firebase_uid=firebase_uid, mobile_number=mobile_number
        )
        if user.exists():
            return user
        return None


"""check mobile number exist serializer"""

class CheckMobileNumberExistSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()

    """validate the mobile number"""

    def validate_mobile_number(self, value):
        validate_phone_number_pattern = "^\\+?[1-9][0-9]{9,14}$"
        if not re.match(validate_phone_number_pattern, value):
            raise serializers.ValidationError(
                """Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."""
            )
        return value

    """checking mobile no. exists or not"""

    def check_mobile_number_exists(self, mobile_number):
        if Talvidouser.objects.filter(mobile_number=mobile_number).exists():
            return True
        return False


"""Google login serializer"""

class TavlidoGoogleLoginSerializer(serializers.Serializer):

    """Required fields"""

    firebase_uid = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    profile_pic = serializers.URLField()

    """override the save method"""

    def save(self):
        email = self.validated_data.get("email")
        firebase_uid = self.validated_data.get("firebase_uid")
        full_name = self.validated_data.get("full_name")

        """verifying the firebase uid"""
        try:
            verify_firebase_uid(firebase_uid=firebase_uid)
        except:
            raise InvalidFirebaseUID()

        try:
            user = Talvidouser.objects.get_or_create(
                username=firebase_uid,
                email=email,
                login_with="Google",
                full_name=full_name,
            )
            return user
        except:
            raise FirebaseUIDExists()


"""Facebok login serializer"""

class TavlidoFacebokLoginSerializer(serializers.Serializer):

    """Required fields"""

    firebase_uid = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    profile_pic = serializers.URLField()

    """override the save method"""

    def save(self):
        email = self.validated_data.get("email")
        firebase_uid = self.validated_data.get("firebase_uid")
        full_name = self.validated_data.get("full_name")

        """verifying the firebase uid"""
        try:
            verify_firebase_uid(firebase_uid=firebase_uid)
        except:
            raise InvalidFirebaseUID()

        try:
            user = Talvidouser.objects.get_or_create(
                username=firebase_uid,
                email=email,
                login_with="Facebook",
                full_name=full_name,
            )
            return user
        except:
            raise FirebaseUIDExists()


"""Regenerate access token serializer"""

class RegenerateAccessTokenSerializer(serializers.Serializer):

    """Required fields"""

    grant_type = serializers.CharField()
    refresh_token = serializers.CharField()

    """method that generate new token on the base of refresh token"""

    def get_access_token(self, grant_type, refresh_token):
        url = f"https://securetoken.googleapis.com/v1/token?key={settings.FIREBASE_API_KEY}"
        data = {"grant_type": grant_type, "refresh_token": refresh_token}
        response_data = requests.post(url=url, data=data)
        res = response_data.json()
        response = {
            "status_code": 200,
            "message": "ok",
            "data": {
                "localId": res["user_id"],  
                "displayName": "",
                "idToken": res["access_token"],
                "refreshToken": res["refresh_token"],
                "expiresIn": res["expires_in"]
            }
        }
        return response, response_data


"""Email register model serializer"""

class TalvidoEmailRegisterSerializer(serializers.Serializer):
    
    """serializers fields"""
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    referral_code = serializers.CharField(required=False)

    """This method validating the email is exists or not"""

    def validate_email(self, value):
        if Talvidouser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already exists")
        return value

    """This method validating the password should atleast 
        contain more than 6 characters"""

    def validate_password(self, value):
        if len(value) <= 6:
            raise serializers.ValidationError(
                "Password should atleast contain more than 6 characters"
            )
        return value

    """overriding the create method"""

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        auth.create_user(email=email, password=password)
        user = generate_firebase_token(email=email, password=password).json()
        talvido_user = Talvidouser.objects.create(
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            email=email,
            password=make_password(password),
            referral_code=validated_data.get("referral_code", ""),
            firebase_uid=user["localId"],
        )
        user["first_name"] = talvido_user.first_name
        user["last_name"] = talvido_user.last_name
        return user


"""Email login serializer"""


class TalvidoEmailLoginSerializer(serializers.Serializer):
    
    """serializers fields"""
    email = serializers.EmailField()
    password = serializers.CharField()

    """This method validating the email is exists or not"""

    def validate_password(self, value):
        if len(value) <= 6:
            raise serializers.ValidationError(
                "Password should atleast contain more than 6 characters"
            )
        return value

    """This method will check login credentials"""

    def check_credentials(self):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")

        """it will generate the firebase tokens"""
        user = generate_firebase_token(email=email, password=password)

        """if status code is 400 then it will raise validation error"""
        if user.status_code == 400:
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                    "message": "unauthorized",
                    "data": user.json()["error"]["message"],
                }
            )
        return user.json()


class ResetEmailPasswordSerializer(serializers.Serializer):
    requestType = serializers.CharField()
    email = serializers.EmailField()

    def send_reset_password_email(self):
        reset_email = send_reset_password_email(
            self.validated_data.get("email"),self.validated_data.get("requestType")
        )
        if reset_email.status_code == 400:
            raise serializers.ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "bad request",
                    "data" : reset_email.json()["error"]["errors"]
                }
            )
        return reset_email
