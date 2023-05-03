from rest_framework import serializers, status
from talvido_app.models import Talvidouser, Profile, Follow, Post


"""user model serializer"""

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talvidouser
        fields = "__all__"


"""profile model serializer"""

class ProfileModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    followers = serializers.SerializerMethodField("get_user_followers")
    followings = serializers.SerializerMethodField("get_user_followings")
    total_post = serializers.SerializerMethodField("get_user_total_posts")
    posts = serializers.SerializerMethodField("get_user_posts")


    class Meta:
        model = Profile
        fields = ["user", "image", "gender","location", "description", "posts", "followers","followings","total_post"]

    def get_user_followers(self,data):
        return Talvidouser.objects.get(firebase_uid=data.user).user_to.all().count()

    def get_user_followings(self,data):
        return Talvidouser.objects.get(firebase_uid=data.user).user_from.all().count()

    def get_user_total_posts(self,data):
        return Talvidouser.objects.get(firebase_uid=data.user).post_user.all().count()
    
    def get_user_posts(self, data):
        from talvido_app.api.serializers.post_serializers import GetPostModelSerializer
        user = Talvidouser.objects.get(firebase_uid=data.user.firebase_uid)
        user_posts = user.post_user.all()
        # return []
        return GetPostModelSerializer(user_posts, many=True, context=self.context).data


"""update profile model serializer"""

class UpdateProfileModelSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    mobile_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "username", "mobile_number", "gender", "description", "location"]

    """override update method and update the talvido user information"""

    def update(self, instance, validated_data):
        username = validated_data.get("username")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        mobile_number = validated_data.get("mobile_number")

        user = Talvidouser.objects.get(firebase_uid=instance)

        if username is not None and username:
            user.username = username
        if first_name is not None and first_name:
            user.first_name = first_name
        if last_name is not None and last_name:
            user.last_name = last_name
        if mobile_number is not None and mobile_number:
            user.mobile_number = mobile_number
        user.save()
        return super().update(instance, validated_data)


"""upadate user profile picture model serializer"""

class UpdateuserProfilePictureModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["image"]


"""Followers model serializer"""

class FollowersModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_profile")

    class Meta:
        model = Follow
        fields = ["user", "created_at"]

    def get_profile(self, data):
        return ProfileModelSerializer(
            Profile.objects.get(user=data.user_from), context=self.context
        ).data


"""Following model serializer"""

class FollowingModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_profile")
    posts = serializers.SerializerMethodField("get_user_post")

    class Meta:
        model = Follow
        fields = ["user", "posts", "created_at"]

    def get_profile(self, data):
        return ProfileModelSerializer(
            Profile.objects.get(user=data.user_to), context=self.context
        ).data

    def get_user_post(self,data):
        from talvido_app.api.serializers.post_serializers import GetPostModelSerializer
        posts = Post.objects.filter(user=data.user_to)
        return GetPostModelSerializer(posts,many=True,context=self.context).data


class UserFollowSerializer(serializers.Serializer):
    user_firebase_uid = serializers.CharField()

    def create(self, validated_data):
        try:
            user = Talvidouser.objects.get(firebase_uid=validated_data.get("user_firebase_uid"))
        except Talvidouser.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {
                        "user_firebase_uid" : [
                            "firebase uid is invalid"
                        ]
                    }
                }
            )
        
        follow  = Follow.objects.get_or_create(
            user_to = user,
            user_from = self.context["request"].user
        )
        return follow
