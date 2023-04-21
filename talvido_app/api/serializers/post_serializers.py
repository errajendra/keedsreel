from rest_framework import serializers, status
from talvido_app.models import (
    Story,
    StoryViews,
    Profile,
    Follow,
    Post
)
from talvido_app.api.serializers.profile_serializers import ProfileModelSerializer
from datetime import datetime


""" story model serializer"""

class StoryModelSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField("get_story_duration")
    user = serializers.CharField(read_only=True)
    story = serializers.FileField()

    def get_story_duration(self, data):
        difference = data.ends_at.replace(tzinfo=None) - datetime.now()
        m, s = divmod(difference.total_seconds(), 60)
        hours  = int(24 - m//60)
        return f"{hours}h ago" if hours > 1 else f"{int(60 - m%60)}m ago"

    class Meta:
        model = Story
        fields = ["id", "user", "story", "post_at", "ends_at", "duration"]


"""delete story serializer"""

class DeleteStorySerializer(serializers.Serializer):
    story_id = serializers.CharField()

    """this method will delete the story"""

    def delete(self):
        Story.objects.get(id=self.validated_data.get("story_id")).delete()
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
            Story.objects.select_related().filter(user=data.user_to, ends_at__gt=datetime.today()),
            many=True,
            context=self.context,
        ).data


"""Get Post model serializer"""

class GetPostModelSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField("get_profile")
    duration = serializers.SerializerMethodField("get_post_duration")

    class Meta:
        model = Post
        fields = ["id","user","description","post","duration","created_at","updated_at"]

    def get_profile(self, data):
        return ProfileModelSerializer(
            Profile.objects.get(user=data.user), context=self.context
        ).data

    def get_post_duration(self,data):
        difference = datetime.now() - data.created_at.replace(tzinfo=None)
        m, s = divmod(difference.total_seconds(), 60)
        hours  = int(m//60)
        if hours > 1:
            return f"{hours} hours ago"
        else:
            return f"{int(m%60)} minutes ago"


"""upload post model serializer"""

class UploadPostModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ["post","description"]


"""delete post serializer"""

class DeletePostSerializer(serializers.Serializer):
    post_id = serializers.CharField()

    def delete(self):
        Post.objects.get(id=self.validated_data.get("post_id")).delete()
        return None
