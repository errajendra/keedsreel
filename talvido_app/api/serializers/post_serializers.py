from rest_framework import serializers, status
from talvido_app.models import Story, StoryViews, Profile, Follow
from talvido_app.api.serializers.profile_serializers import ProfileModelSerializer
from datetime import datetime


""" story model serializer"""

class StoryModelSerializer(serializers.ModelSerializer):
    hours = serializers.SerializerMethodField("get_hours")
    user = serializers.CharField(read_only=True)
    story = serializers.FileField()

    def get_hours(self, data):
        hours = data.ends_at - data.post_at
        return hours.days

    class Meta:
        model = Story
        fields = ["id", "user", "story", "post_at", "ends_at", "hours"]


"""delete story serializer"""

class DeleteStorySerializer(serializers.Serializer):
    story_id = serializers.CharField()

    """this method will delete the story"""

    def delete(self, id):
        Story.objects.get(id=id).delete()
        return None


"""story view model serializer"""

class StoryViewModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_profile")

    class Meta:
        model = StoryViews
        fields = ["user", "created_at"]

    def get_profile(self, data):
        return ProfileModelSerializer(
            Profile.objects.get(user=data.user), context=self.context
        ).data


"""add story views serializer"""

class AddStoryViewSerializer(serializers.Serializer):
    story_id = serializers.CharField()

    """override save method"""

    def save(self, **kwargs):
        story_id = self.validated_data.get("story_id")
        request = self.context["request"]
        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {"story_id": ["The story_id is invalid"]},
                }
            )

        """if user has own story then it will not add the story views"""
        if request.user.firebase_uid == story.user.firebase_uid:
            return None
        story_view = StoryViews.objects.get_or_create(user=request.user, story=story)
        return story_view


"""Get user followings stories model serializer"""

class GetUserFollowingsStoriesModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_profile")
    stories = serializers.SerializerMethodField("get_stories")

    class Meta:
        model = Follow
        fields = ["user", "stories"]

    def get_profile(self, data):
        return ProfileModelSerializer(
            Profile.objects.get(user=data.user_to), context=self.context
        ).data

    def get_stories(self, data):
        return StoryModelSerializer(
            Story.objects.filter(user=data.user_to, ends_at__gt=datetime.today()),
            many=True,
            context=self.context,
        ).data
