from rest_framework import serializers, status
from talvido_app.models import Reel, ReelComment, ReelLike, ReelCommentLike, Talvidouser, ReelView
from talvido_app.api.serializers.profile_serializers import UserModelSerializer


""" Reel List, Create, delete Serializer """
class GetReelModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user_profile")
    reel_views = serializers.SerializerMethodField("get_reel_views")
    reel_liked_by = serializers.SerializerMethodField("get_liked_by_user_reel")

    class Meta:
        model = Reel
        fields = ["id", "user", "reel", "description", "reel_views", "reel_liked_by", "created_at", "updated_at"]
    
    def get_user_profile(self, data):
        user = Talvidouser.objects.get(firebase_uid=data.user.firebase_uid)
        user_serializer = UserModelSerializer(user).data
        user_serializer["image"] = (
            "https://"
            + self.context["request"].META["HTTP_HOST"]
            + user.profile.image.url
        )
        return user_serializer

    def get_reel_views(self, data):
        return Reel.objects.get(id=data.id).reel_view_reel.views

    def get_liked_by_user_reel(self, data):
        reel_like = data.user.reel_like_user.all()
        return GetReelLikeModelSerializer(reel_like, many=True, context=self.context).data


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
                        "reel_id" : [
                            "reel_id is invalid"
                        ]
                    }
                }
            )
        reel_view = reel.reel_view_reel
        reel_view.views += 1
        reel_view.save()
        return reel


class AddReelLikeSerializer(serializers.Serializer):
    reel_id = serializers.CharField()

    def get_queryset(self):
        try:
            reel = Reel.objects.get(id=self.data.get("reel_id"))
            return reel
        except Reel.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "bad request",
                    "data" : {
                        "reel_id" : [
                            "reel_id is invalid"
                        ]
                    }
                }
            )

    def create(self, validate_data):
        reel_like = ReelLike.objects.get_or_create(
            user = self.context["request"].user,
            reel = self.get_queryset()
        )
        return reel_like


class GetReelLikeModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user_profile")

    class Meta:
        model = ReelLike
        fields = ["id", "user", "reel", "created_at", "updated_at"]

    def get_user_profile(self, data):
        user = Talvidouser.objects.get(firebase_uid=data.user.firebase_uid)
        user_serializer = UserModelSerializer(user).data
        user_serializer["image"] = (
            "https://"
            + self.context["request"].META["HTTP_HOST"]
            + user.profile.image.url
        )
        return user_serializer


class DeleteReelLikeSerializer(serializers.Serializer):
    reel_liked_id = serializers.CharField()

    def get_queryset(self):
        try:
            reel_liked = ReelLike.objects.get(id=self.data.get("reel_liked_id"),user=self.context["request"].user)
            return reel_liked
        except ReelLike.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "bad request",
                    "data" : {
                        "reel_id" : [
                            "reel_liked_id is invalid or not associate with current user"
                        ]
                    }
                }
            )

    def delete(self):
        self.get_queryset().delete()
        return None
