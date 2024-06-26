from rest_framework import serializers
from talvido_app.models import Talvidouser, ReferralUser
from django.conf import settings
from talvido_app.firebase.helpers import (
    verify_firebase_uid,
    generate_firebase_token,
    send_reset_password_email,
    # generate_firebase_token_with_email,
)
from talvido_app.firebase.exceptions import InvalidFirebaseUID, FirebaseUIDExists
from django.contrib.auth.hashers import make_password
import requests
import re
from firebase_admin import auth
from rest_framework import status
from firebase_admin.exceptions import AlreadyExistsError


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

    password = serializers.CharField()
    email = serializers.EmailField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    profileUrl = serializers.URLField()

    """overriding the create method"""

    def create(self, validated_data):
        email = validated_data.get("email")
        users = Talvidouser.objects.filter(email=email)
        if users.exists():
            password = users.first().password_value
        else:
            password = validated_data.get("password")
        try:
            auth.create_user(email=email, password=password)
        except AlreadyExistsError:
            # user = generate_firebase_token(email=email, password=password)
            pass
        user = generate_firebase_token(email=email, password=password).json()
        try:
            talvido_user = Talvidouser.objects.create(
                first_name=validated_data.get("firstName"),
                last_name=validated_data.get("lastName"),
                email=email,
                password=make_password(password),
                firebase_uid=user["localId"],
                password_value=password,
            )
        except AlreadyExistsError:
            talvido_user = Talvidouser.objects.get(
                email=email,
                firebase_uid=user["localId"],
            )
        # profile = Profile.objects.get(user=talvido_user)
        # profile.image = validated_data['profileUrl']
        # profile.save()
        user["first_name"] = talvido_user.first_name
        user["last_name"] = talvido_user.last_name
        return user



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
                "expiresIn": res["expires_in"],
            },
        }
        return response, response_data


"""Email register model serializer"""

class TalvidoEmailRegisterSerializer(serializers.Serializer):

    """serializers fields"""

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    referral = serializers.CharField(required=False, allow_blank=True)

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
        try:
            auth.create_user(email=email, password=password)
        except AlreadyExistsError:
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": [
                        "The email address you are trying to login with is already exists in firebase database but not in our database",
                        "please use the email address and same password if you remember when you signup",
                        "otherwise reset password and set new password",
                        "and then come to signup again with the same credentals"
                    ]
                }
            )
        user = generate_firebase_token(email=email, password=password).json()
        talvido_user = Talvidouser.objects.create(
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            email=email,
            password=make_password(password),
            password_value=password,
            firebase_uid=user["localId"],
        )
        user["first_name"] = talvido_user.first_name
        user["last_name"] = talvido_user.last_name

        referral_code = validated_data.get("referral", None)
        referral_user = Talvidouser.objects.filter(referral_code=referral_code)
        if referral_user.exists():
            ref_user = referral_user.first()
            ReferralUser.objects.get_or_create(
                user=talvido_user, referral_user=ref_user
            )
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
        firebase_uid = user.json()["localId"]
        check_user = Talvidouser.objects.filter(firebase_uid=firebase_uid)
        if check_user.exists() and check_user.first().is_active:
            u = check_user.first()
            u.password_value = password
            u.save()
            return user.json()
        elif not check_user.exists():
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                    "message": "unauthorized",
                    "data": "The email your are trying to login with is not longer avaliable in database"
                }
            )
        else:
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                    "message": "unauthorized",
                    "data": "Your account is temporary inactive"
                }
            )


"""Reset password serializer"""

class ResetEmailPasswordSerializer(serializers.Serializer):
    requestType = serializers.CharField()
    email = serializers.EmailField()

    def send_reset_password_email(self):
        reset_email = send_reset_password_email(
            self.validated_data.get("email"), self.validated_data.get("requestType")
        )
        if reset_email.status_code == 400:
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": reset_email.json()["error"]["errors"],
                }
            )
        return reset_email


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

    """This method validating the password"""

    def validate_password(self, value):
        if len(value) <= 6:
            raise serializers.ValidationError(
                "Password should atleast contain more than 6 characters"
            )
        return value

    def update_password(self):
        firebase_uid = self.context["request"].user
        password = self.data.get("password")
        update_pwd = auth.update_user(uid=str(firebase_uid), password=password)
        try:
            user = Talvidouser.objects.get(firebase_uid=firebase_uid)
            user.password_value = password
            user.save()
        except:
            pass
        return update_pwd



""" Google ID Token register serializer"""

# class GoogleTokenSignAuthSerializer(serializers.Serializer):
#     id_token = serializers.CharField()

#     """This method validating the email is exists or not"""
#     def validate_id_token(self, value):
#         url = "https://oauth2.googleapis.com/tokeninfo"
#         params = {'id_token': f'{value}'}
#         r = requests.get(url, params=params)
#         result = r.json()
#         # userid = result['sub']
#         if not 'email' in result:
#             raise serializers.ValidationError("Invalid token")
#         self.email = result['email']
#         self.profile_picture = result['picture']
#         self.f_name = result['given_name']
#         self.l_name = result['family_name']
#         if not self.email:
#             raise serializers.ValidationError("Invalid token")
#         if Talvidouser.objects.filter(email=self.email).exists():
#             raise serializers.ValidationError("This email is already exists")
#         return value


#     """overriding the create method"""
#     def create(self, validated_data):
#         email = self.email
#         users = Talvidouser.objects.filter(email=self.email)
#         if Talvidouser.objects.filter(email=self.email).exists():
#             talvido_user = users[0]
#             user = generate_firebase_token_with_email(email=email).json()
#         else:
#             try:
#                 auth.create_user(email=email)
#             except AlreadyExistsError:
#                 raise serializers.ValidationError(
#                     {
#                         "status_code": status.HTTP_400_BAD_REQUEST,
#                         "message": "bad request",
#                         "data": [
#                             "The email address you are trying to login with is already exists in firebase database but not in our database",
#                             "please use the email address and same password if you remember when you signup",
#                             "otherwise reset password and set new password",
#                             "and then come to signup again with the same credentals"
#                         ]
#                     }
#                 )
#             user = generate_firebase_token_with_email(email=email).json()
#             talvido_user = Talvidouser.objects.create(
#                 first_name=self.f_name,
#                 last_name=self.l_name,
#                 email=email,
#                 firebase_uid=user["localId"],
#             )
#         user["first_name"] = talvido_user.first_name
#         user["last_name"] = talvido_user.last_name
#         return user
class GoogleTokenSignAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()

    """This method validating the email is exists or not"""
    def validate_id_token(self, value):
        url = "https://oauth2.googleapis.com/tokeninfo"
        params = {'id_token': f'{value}'}
        r = requests.get(url, params=params)
        result = r.json()
        self.userid = result['sub']
        if not 'email' in result:
            raise serializers.ValidationError("Invalid token")
        self.email = result['email']
        self.profile_picture = result['picture']
        self.f_name = result['given_name']
        self.l_name = result['family_name']
        if not self.email:
            raise serializers.ValidationError("Invalid token")
        if Talvidouser.objects.filter(email=self.email).exists():
            raise serializers.ValidationError("This email is already exists")
        return value


    """overriding the create method"""
    def create(self, validated_data):
        email = self.email
        users = Talvidouser.objects.filter(email=self.email)
        if Talvidouser.objects.filter(email=self.email).exists():
            talvido_user = users[0]
            user = generate_firebase_token(email=email, password=self.userid).json()
        else:
            try:
                auth.create_user(email=email)
            except AlreadyExistsError:
                raise serializers.ValidationError(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "message": "bad request",
                        "data": [
                            "The email address you are trying to login with is already exists in firebase database but not in our database",
                            "please use the email address and same password if you remember when you signup",
                            "otherwise reset password and set new password",
                            "and then come to signup again with the same credentals"
                        ]
                    }
                )
            user = generate_firebase_token(email=email, password=self.userid).json()
            talvido_user = Talvidouser.objects.create(
                first_name=self.f_name,
                last_name=self.l_name,
                email=email,
                firebase_uid=user["localId"],
            )
        user["first_name"] = talvido_user.first_name
        user["last_name"] = talvido_user.last_name
        return user
