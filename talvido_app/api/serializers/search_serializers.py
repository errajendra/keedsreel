from rest_framework import serializers
from talvido_app.models import Talvidouser, Profile


class SearchByUsernameModelSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image")

    class Meta:
        model = Talvidouser
        fields = ["firebase_uid", "username", "first_name", "last_name", "image"]

    def get_image(self, data):
        profile = Profile.objects.get(user=data.firebase_uid)
        return "https://" + self.context["request"].META["HTTP_HOST"] + profile.image.url
