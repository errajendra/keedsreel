from rest_framework import serializers
from talvido_app.models import Talvidouser
import re


"""mobile login serialzier"""

class TalvidoMobileLoginSerializer(serializers.Serializer):

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

        user = Talvidouser.objects.get_or_create(
            mobile_number=mobile_number,
            username=firebase_uid,
            login_with="Mobile Number",
        )
        return user
