from rest_framework import serializers
from talvido_app.models import (
    Talvidouser,
    Profile,
    Follow
)


"""user model serializer"""

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Talvidouser
        fields = '__all__'


"""profile model serializer"""

class ProfileModelSerializer(serializers.ModelSerializer):

    user = UserModelSerializer()

    class Meta:
        model = Profile
        fields = ['user','image','gender']


"""update profile model serializer"""

class UpdateProfileModelSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Profile
        fields = ['full_name','username','gender']
    
    """override update method and update the talvido user information"""
    def update(self, instance, validated_data):
        username = validated_data.get("username")
        full_name = validated_data.get("full_name")

        user = Talvidouser.objects.get(firebase_uid=instance)

        if username is not None and username:
            user.username = username
        if full_name is not None and full_name:
            user.full_name = full_name
        user.save()
        return super().update(instance, validated_data)


"""upadate user profile picture model serializer"""

class UpdateuserProfilePictureModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['image']


"""Followers model serializer"""

class FollowersModelSerializer(serializers.ModelSerializer):

    user_from = UserModelSerializer()

    class Meta:
        model = Follow
        fields = ['user_from','created_at']


"""Following model serializer"""

class FollowingModelSerializer(serializers.ModelSerializer):

    user_to = UserModelSerializer()

    class Meta:
        model = Follow
        fields = ['user_to','created_at']
