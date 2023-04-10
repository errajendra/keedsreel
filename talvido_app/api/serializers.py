from rest_framework import serializers
from talvido_app.models import Talvidouser
from rest_framework import status
import re


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

    """override the save method"""
    def save(self):
        mobile_number = self.validated_data.get("mobile_number")
        firebase_uid = self.validated_data.get("firebase_uid")

        try:
            user = Talvidouser.objects.get_or_create(
            mobile_number=mobile_number,
            username=firebase_uid,
            login_with="Mobile Number",
        )
            return user
        except:
            raise serializers.ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "bad request",
                    "firebase_uid" : "Firebase uid is already exist."
                }
            )


"""Google login serializer"""

class TavlidoGoogleLoginSerializer(serializers.Serializer):

    firebase_uid = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    profile_pic = serializers.URLField()

    """override the save method"""
    def save(self):
        email = self.validated_data.get("email")
        firebase_uid = self.validated_data.get("firebase_uid")
        full_name = self.validated_data.get("full_name")

        try:
            user = Talvidouser.objects.get_or_create(
            username=firebase_uid,
            email=email,
            login_with="Google",
            full_name=full_name
        )
            return user
        except:
            raise serializers.ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "bad request",
                    "firebase_uid" : "Firebase uid is already exist."
                }
            )


"""Facebok login serializer"""

class TavlidoFacebokLoginSerializer(serializers.Serializer):

    firebase_uid = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    profile_pic = serializers.URLField()

    """override the save method"""
    def save(self):
        email = self.validated_data.get("email")
        firebase_uid = self.validated_data.get("firebase_uid")
        full_name = self.validated_data.get("full_name")

        try:
            user = Talvidouser.objects.get_or_create(
            username=firebase_uid,
            email=email,
            login_with="Facebook",
            full_name=full_name
        )
            return user
        except:
            raise serializers.ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "bad request",
                    "firebase_uid" : "Firebase uid is already exist."
                }
            )