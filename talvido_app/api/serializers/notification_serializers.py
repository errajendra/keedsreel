from rest_framework import serializers
from talvido_app.models import Notification, Talvidouser
from talvido_app.utils import get_duration


class NotificationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "notification_type", "seen"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = self.get_user_info(instance)
        if instance.notification_type == "POST_LIKE":
            data["post"] = self.get_post_like_data(instance)
        elif instance.notification_type == "POST_COMMENT":
            data["post"] = self.get_post_comment_data(instance)
        elif instance.notification_type == "FOLLOW":
            data["is_follow"] = self.get_follow_data(instance)
        data["duration"] = get_duration(instance)
        return data

    def get_user_info(self, data):
        return {
            "firebase_uid": data.user_from.firebase_uid,
            "full_name": data.user_from.first_name + " " + data.user_from.last_name,
            "username": data.user_from.username,
            "image": "https://"
            + self.context["request"].META["HTTP_HOST"]
            + data.user_from.profile.image.url,
        }

    def get_post_like_data(self, data):
        post_data = data.post_like.post
        return {
            "id": post_data.id,
            "image": ( post_data.post.name if "https://ik.imagekit.io/" in post_data.post.name else "https://"
            + self.context["request"].META["HTTP_HOST"]
            + post_data.post.url,
            )
        }

    def get_post_comment_data(self, data):
        post_data = data.post_comment
        return {
            "id": post_data.post.id,
            "image": ( post_data.post.post.name if "https://ik.imagekit.io/" in post_data.post.post.name else "https://"
            + self.context["request"].META["HTTP_HOST"]
            + post_data.post.post.url,
            ),
            "comment": post_data.comment,
        }

    def get_follow_data(self, data):
        return (
            1
            if Talvidouser.objects.get(firebase_uid=self.context["request"].user)
            .user_from.all()
            .filter(user_to=data.user_from, user_from=self.context["request"].user)
            .exists()
            else 0
        )
