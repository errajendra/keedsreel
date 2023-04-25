from rest_framework import serializers
from talvido_app.models import Talvidouser
from django.conf import settings
from talvido_app.firebase.helpers import verify_firebase_uid, generate_firebase_token
from talvido_app.firebase.exceptions import InvalidFirebaseUID, FirebaseUIDExists
from django.contrib.auth.hashers import make_password
import requests
import re
from firebase_admin import auth


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
        response = requests.post(url=url, data=data)
        return response


"""Email register model serializer"""

class TalvidoEmailRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    referral_code = serializers.CharField(required=False)

    def validate_email(self, value):
        if Talvidouser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already exists")
        return value
    
    def validate_password(self, value):
        if len(value) <= 6:
            raise serializers.ValidationError("Password should atleast contain more than 6 characters")
        return value

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        auth.create_user(
            email = email,
            password = password
        )
        user = generate_firebase_token(email=email, password=password)
        Talvidouser.objects.create(
            first_name = validated_data.get("first_name"),
            last_name = validated_data.get("last_name"),
            email = email,
            password = make_password(password),
            referral_code = validated_data.get("referral_code",""),
            firebase_uid = user["localId"]
        )
        return user
