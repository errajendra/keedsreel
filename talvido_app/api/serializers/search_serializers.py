from rest_framework import serializers
from talvido_app.models import Talvidouser, Profile


"""search by username model serializer"""

class SearchAccountModelSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image")

    class Meta:
        model = Talvidouser
        fields = ["firebase_uid", "username", "first_name", "last_name", "image"]
    
    """this method will return the user profile image url"""

    def get_image(self, data):
        profile = Profile.objects.get(user=data.firebase_uid)
        return "https://" + self.context["request"].META["HTTP_HOST"] + profile.image.url
