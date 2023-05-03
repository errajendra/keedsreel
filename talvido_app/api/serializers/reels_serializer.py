from rest_framework import serializers, status
from talvido_app.models import (
    Reel,
    ReelComment,
    ReelLike,
    ReelCommentLike,
    Talvidouser,
)
from talvido_app.api.serializers.profile_serializers import UserModelSerializer
from datetime import datetime


class GetReelModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user_profile")
    reel_views = serializers.SerializerMethodField("get_reel_views")
    reel_liked_by = serializers.SerializerMethodField("get_liked_by_user_reel")
    comments = serializers.SerializerMethodField("get_reel_comments")
    total_likes = serializers.SerializerMethodField("get_total_likes")
    total_comments = serializers.SerializerMethodField("get_total_comments")
    duration = serializers.SerializerMethodField("get_reel_duration")

    class Meta:
        model = Reel
        fields = [
            "id",
            "user",
            "reel",
            "description",
            "reel_views",
            "reel_liked_by",
            "comments",
            "duration",
            "total_likes",
            "total_comments",
            "created_at",
            "updated_at",
        ]

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
        reel_liked_user = data.reel_like.all()
        self.total_reel_likes = reel_liked_user.count()
        return GetReelLikeModelSerializer(
            reel_liked_user, many=True, context=self.context
        ).data

    def get_reel_comments(self, data):
        reel_comment = data.reelcomment_set.all()
        self.total_comments = reel_comment.count()
        return GetReelCommentModelSerializer(
            reel_comment, many=True, context=self.context
        ).data

    def get_total_likes(self, data):
        return self.total_reel_likes

    def get_total_comments(self, data):
        return self.total_comments

    def get_reel_duration(self, data):
        difference = datetime.now() - data.created_at.replace(tzinfo=None)
        m, s = divmod(difference.total_seconds(), 60)
        hours = int(m // 60)
        if hours > 1:
            return f"{hours} hours ago"
        else:
            return f"{int(m%60)} minutes ago"


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
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {"reel_id": ["reel_id is invalid"]},
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
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {"reel_id": ["reel_id is invalid"]},
                }
            )

    def create(self, validate_data):
        reel_like = ReelLike.objects.get_or_create(
            user=self.context["request"].user, reel=self.get_queryset()
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
            reel_liked = ReelLike.objects.get(
                id=self.data.get("reel_liked_id"), user=self.context["request"].user
            )
            return reel_liked
        except ReelLike.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {
                        "reel_id": [
                            "reel_liked_id is invalid or not associate with current user"
                        ]
                    },
                }
            )

    def delete(self):
        self.get_queryset().delete()
        return None


class AddReelCommentSerializer(serializers.ModelSerializer):
    reel_id = serializers.CharField()

    class Meta:
        model = ReelComment
        fields = ["reel_id", "comment"]


class GetReelCommentModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user_profile")
    liked_by = serializers.SerializerMethodField("get_liked_comment")

    class Meta:
        model = ReelComment
        fields = ["id", "user", "reel", "comment", "created_at", "updated_at", "liked_by"]

    def get_user_profile(self, data):
        user = Talvidouser.objects.get(firebase_uid=data.user.firebase_uid)
        user_serializer = UserModelSerializer(user).data
        user_serializer["image"] = (
            "https://"
            + self.context["request"].META["HTTP_HOST"]
            + user.profile.image.url
        )
        return user_serializer

    def get_liked_comment(self, data):
        reel_comment_like = data.reel_comment.all()
        return GetReelCommentLikeModelSerializer(reel_comment_like, many=True, context=self.context).data


class RemoveReelCommentSerializer(serializers.Serializer):
    reel_comment_id = serializers.CharField()

    def get_queryset(self):
        try:
            reel_comment = ReelComment.objects.get(
                id=self.data.get("reel_comment_id"), user=self.context["request"].user
            )
            return reel_comment
        except ReelComment.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {
                        "reel_id": [
                            "reel_comment_id is invalid or not associate with current user"
                        ]
                    },
                }
            )

    def delete(self):
        self.get_queryset().delete()
        return None


class AddReelCommentLikeSerializer(serializers.Serializer):
    reel_comment_id = serializers.CharField()

    def get_queryset(self):
        try:
            reel_comment = ReelComment.objects.get(id=self.data.get("reel_comment_id"))
            return reel_comment
        except ReelComment.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {"reel_comment_id": ["reel_comment_id is invalid"]},
                }
            )

    def create(self, validate_data):
        reel_comment_like = ReelCommentLike.objects.get_or_create(
            user=self.context["request"].user, comment=self.get_queryset()
        )
        return reel_comment_like


class GetReelCommentLikeModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user_profile")
    
    class Meta:
        model = ReelComment
        fields = ["id", "user", "comment", "created_at", "updated_at"]

    def get_user_profile(self, data):
        user = Talvidouser.objects.get(firebase_uid=data.user.firebase_uid)
        user_serializer = UserModelSerializer(user).data
        user_serializer["image"] = (
            "https://"
            + self.context["request"].META["HTTP_HOST"]
            + user.profile.image.url
        )
        return user_serializer


class RemoveReelCommentLikeSerializer(serializers.Serializer):
    reel_comment_like_id = serializers.CharField()

    def get_queryset(self):
        try:
            reel_comment = ReelCommentLike.objects.get(
                id=self.data.get("reel_comment_like_id"), user=self.context["request"].user
            )
            return reel_comment
        except ReelCommentLike.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {
                        "reel_comment_like_id": [
                            "reel_comment_like_id is invalid or not associate with current user"
                        ]
                    },
                }
            )

    def delete(self):
        self.get_queryset().delete()
        return None
