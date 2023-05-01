from rest_framework import serializers, status
from talvido_app.models import Reel, ReelComment, ReelLike, ReelCommentLike, Talvidouser, ReelView
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


class AddReelViewsSerializer(serializers.Serializer):
    reel_id = serializers.CharField()

    def create(self, validate_data):
        try:
            reel = Reel.objects.get(id=validate_data.get("reel_id"))
        except Reel.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "bad request",
                    "data" : {
                        "post_id" : [
                            "post_id is invalid"
                        ]
                    }
                }
            )
        import pdb;pdb.set_trace()
        reel_view = reel.reelview.views + 1
        reel = reel_view.save()
        return reel
