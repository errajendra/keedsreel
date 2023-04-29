from rest_framework import serializers
from talvido_app.models import Reel, ReelComment, ReelLike, ReelCommentLike, Talvidouser
from talvido_app.api.serializers.profile_serializers import UserModelSerializer


""" Reel List, Create, delete Serializer """
class GetReelModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user_profile")

    class Meta:
        model = Reel
        fields = ["id", "user", "reel", "description", "created_at", "updated_at"]
    
    def get_user_profile(self, data):
        user = Talvidouser.objects.get(firebase_uid=data.user.firebase_uid)
        user_serializer = UserModelSerializer(user).data
        user_serializer["image"] = (
            "https://"
            + self.context["request"].META["HTTP_HOST"]
            + user.profile.image.url
        )
        return user_serializer


class UploadUserReelsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reel
        fields = ["reel", "description"]
