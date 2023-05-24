from rest_framework import serializers, status
from talvido_app.models import (
    Story,
    StoryViews,
    Profile,
    Follow,
    Post,
    PostComment,
    Talvidouser,
    PostLike,
    PostCommentLike,
    StoryHighlight,
)
from talvido_app.api.serializers.profile_serializers import (
    ProfileModelSerializer,
    UserModelSerializer,
)
from datetime import datetime
import os
from talvido_app.utils import get_duration
from talvido_app.utils import get_duration


""" story model serializer"""

class StoryModelSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField("get_story_duration")
    user = serializers.SerializerMethodField("get_user_profile", read_only=True)
    story = serializers.FileField()
    story_views = serializers.SerializerMethodField("get_story_views", read_only=True)
    finish = serializers.CharField(default=0, read_only=True)
    story_type = serializers.SerializerMethodField("get_story_type", read_only=True)
    story_view_status = serializers.SerializerMethodField(
        "get_story_view_status", read_only=True
    )

    def get_story_duration(self, data):
        return get_duration(data=data)

    def get_user_profile(self, data):
        user = Talvidouser.objects.get(firebase_uid=data.user)
        user_serializer = UserModelSerializer(
            user, context={"request": self.context["request"]}
        ).data
        user_serializer["image"] = (
            "http://"
            + self.context["request"].META["HTTP_HOST"]
            + user.profile.image.url
        )
        return user_serializer

    def get_story_views(self, data):
        story = Story.objects.get(id=data.id)
        story_views = story.story_content.all().count()
        return story_views

    def get_story_type(self, data):
        image_formats = [".jpg", ".jpeg", ".png"]
        video_formats = [
            ".mp4",
            ".mov",
            ".wmv",
            ".webm",
            ".avi",
            ".fli",
            ".mkv",
            ".mts",
        ]
        name, extension = os.path.splitext(data.story.name)
        if extension.lower() in image_formats:
            return "image"
        elif extension.lower() in video_formats:
            return "video"
        return []

    def get_story_view_status(self, data):
        return (
            1
            if StoryViews.objects.select_related()
            .filter(user=self.context["request"].user, story=data)
            .exists()
            else 0
        )

    def get_video_length(self, data):
        if self.get_story_type(data=data) == "video":
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(data.story.path)
            return int(clip.duration)
        return 0    

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data["vido_duration"] = self.get_video_length(data=instance)
        return data

    class Meta:
        model = Story
        fields = [
            "id",
            "user",
            "story",
            "post_at",
            "ends_at",
            "duration",
            "story_views",
            "finish",
            "story_type",
            "story_view_status",
        ]


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
        model = Story
        fields = ["user", "stories"]

    def get_profile(self, data):
        return ProfileModelSerializer(
            Profile.objects.get(user=data.user), context=self.context
        ).data

    def get_stories(self, data):
        return StoryModelSerializer(
            Story.objects.select_related().filter(
                user=data.user, ends_at__gt=datetime.today()
            ),
            many=True,
            context=self.context,
        ).data


"""Get Post model serializer"""

class GetPostModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_profile")
    duration = serializers.SerializerMethodField("get_post_duration")
    comments = serializers.SerializerMethodField("get_post_comments")
    total_comments = serializers.SerializerMethodField("count_comments")
    liked_by = serializers.SerializerMethodField("get_post_liked_by_user")
    total_likes = serializers.SerializerMethodField("get_total_likes")
    is_like = serializers.SerializerMethodField("is_post_like")
    is_follow = serializers.SerializerMethodField("get_is_follow")

    def get_profile(self, data):
        user = Talvidouser.objects.get(firebase_uid=data.user)
        user_serializer = UserModelSerializer(
            user, context={"request": self.context["request"]}
        ).data
        user_serializer["image"] = (
            "https://"
            + self.context["request"].META["HTTP_HOST"]
            + user.profile.image.url
        )
        return user_serializer

    def get_post_duration(self, data):
        return get_duration(data)

    def get_post_comments(self, data):
        post = Post.objects.get(id=data.id)
        post_comments = post.post_comment.all()
        self.comments_count = post_comments.count()
        return GetPostCommentModelSerializer(
            post_comments, many=True, context=self.context
        ).data

    def count_comments(self, data):
        return self.comments_count

    def get_post_liked_by_user(self, data):
        post = Post.objects.get(id=data.id)
        post_liked_user = post.post_like.all()
        self.total_likes = post_liked_user.count()
        return GetPostLikeModelSerializer(post_liked_user, many=True, context=self.context).data

    def get_total_likes(self, data):
        return self.total_likes

    def is_post_like(self, data):
        return (
            1
            if PostLike.objects.select_related()
            .filter(user=self.context["request"].user, post=data)
            .exists()
            else 0
        )

    def get_is_follow(self, data):
        return (
            1
            if Follow.objects.select_related()
            .filter(
                user_to=data.user.firebase_uid, user_from=self.context["request"].user
            )
            .exists()
            else 0
        )

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "description",
            "post",
            "duration",
            "created_at",
            "updated_at",
            "comments",
            "liked_by",
            "total_comments",
            "total_likes",
            "is_like",
            "is_follow",
        ]


"""upload post model serializer"""

class UploadPostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["post", "description"]


"""delete post serializer"""

class DeletePostSerializer(serializers.Serializer):
    post_id = serializers.CharField()

    def delete(self):
        Post.objects.get(id=self.validated_data.get("post_id")).delete()
        return None


"""post comment model serializer"""

class PostCommentModelSerializer(serializers.ModelSerializer):
    post_id = serializers.CharField()

    class Meta:
        model = PostComment
        fields = ["post_id", "comment"]

    def create(self, validated_data):
        request = self.context["request"]
        try:
            post = Post.objects.get(id=self.validated_data.get("post_id"))
        except Post.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {"post_id": ["This post_id is invalid"]},
                }
            )
        post_comment = PostComment.objects.create(
            user=request.user, post=post, comment=self.validated_data.get("comment")
        )
        return post_comment


"""delete post comment serializer"""

class DeletePostCommentSerializer(serializers.Serializer):
    comment_id = serializers.CharField()

    def delete(self):
        request = self.context["request"]
        post_comment = PostComment.objects.filter(
            user=request.user, id=self.validated_data.get("comment_id")
        )
        if post_comment.exists():
            post_comment.first().delete()
            return None
        raise serializers.ValidationError(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "data": {
                    "comment_id": [
                        "comment_id is either invalid nor associate with current user"
                    ]
                },
            }
        )


"""get post comments model serializer"""

class GetPostCommentModelSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField("get_comment_duration")
    user = serializers.SerializerMethodField("get_user_profile")
    comment_likes = serializers.SerializerMethodField("get_comment_likes")
    total_comment_likes = serializers.SerializerMethodField("get_total_comment_likes")

    class Meta:
        model = PostComment
        fields = [
            "id",
            "user",
            "post",
            "comment",
            "created_at",
            "duration",
            "comment_likes",
            "total_comment_likes",
        ]

    def get_comment_duration(self, data):
        return get_duration(data=data)

    def get_user_profile(self, data):
        user = Talvidouser.objects.get(firebase_uid=data.user)
        user_serializer = UserModelSerializer(
            user, context={"request": self.context["request"]}
        ).data
        user_serializer["image"] = (
            "https://"
            + self.context["request"].META["HTTP_HOST"]
            + user.profile.image.url
        )
        return user_serializer

    def get_comment_likes(self, data):
        comment = PostComment.objects.get(id=data.id)
        comment_like = comment.post_comment.all()
        self.total_comment_likes = comment_like.count()
        return GetPostCommentLikeModelSerializer(comment_like, many=True).data

    def get_total_comment_likes(self, data):
        return self.total_comment_likes

    def to_representation(self, instance):
        data  = super().to_representation(instance)
        data["post"] = (
            "https://"
            + self.context["request"].META["HTTP_HOST"] 
            + instance.post.post.url
        )
        data["post_id"] = instance.post.id
        return data

"""add post like serializer"""

class AddPostLikeSerializer(serializers.Serializer):
    post_id = serializers.CharField()

    def create(self, validated_data):
        request = self.context["request"]
        try:
            post = Post.objects.get(id=self.validated_data.get("post_id"))
        except Post.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {"post_id": ["post_id is invalid"]},
                }
            )
        post_like = PostLike.objects.get_or_create(user=request.user, post=post)
        return post_like

    def delete(self):
        request = self.context["request"]
        post_like = PostLike.objects.select_related().filter(
            user=request.user, post=self.validated_data.get("post_id")
        )
        if post_like.exists():
            post_like.first().delete()
            return None
        raise serializers.ValidationError(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "data": {
                    "comment_id": [
                        "post_id is either invalid nor like associate with current user"
                    ]
                },
            }
        )


"""post comment like serializer"""

class AddPostCommentLikeSerializer(serializers.Serializer):
    comment_id = serializers.CharField()

    def create(self, validated_data):
        request = self.context["request"]
        try:
            post_comment = PostComment.objects.get(
                id=self.validated_data.get("comment_id")
            )
        except PostComment.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {"post_id": ["comment_id is invalid"]},
                }
            )
        post_comment_like = PostCommentLike.objects.get_or_create(
            user=request.user, comment=post_comment
        )
        return post_comment_like

    def delete(self):
        request = self.context["request"]
        post_comment_like = PostCommentLike.objects.filter(
            user=request.user, comment=self.validated_data.get("comment_id")
        )
        if post_comment_like.exists():
            post_comment_like.first().delete()
            return None
        raise serializers.ValidationError(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "data": {"comment_id": ["comment_id is invalid"]},
            }
        )


"""get post comment like model serializer"""

class GetPostCommentLikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentLike
        fields = ["id", "user"]


"""get post like model serializer"""

class GetPostLikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ["id", "user", "post"]

    def to_representation(self, instance):
        data  = super().to_representation(instance)
        data["post"] = (
            "https://"
            + self.context["request"].META["HTTP_HOST"] 
            + instance.post.post.url
        )
        data["post_id"] = instance.post.id
        return data


"""get story highlights model serializer"""

class GetStoryHighlightsModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    stories = StoryModelSerializer(many=True)

    class Meta:
        model = StoryHighlight
        fields = ["id", "user", "title", "stories", "created_at", "updated_at"]
