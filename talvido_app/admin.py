from django.contrib import admin
from .forms import TalvidouserChangeForm, TalvidouserCreationForm
from .models import (
    Talvidouser,
    Profile,
    Story,
    Follow,
    StoryViews,
    Post,
    PostComment,
    PostLike,
    PostCommentLike,
    Notification,
    StoryHighlight,
    Reel,
    ReelLike,
    ReelComment,
    ReelCommentLike,
    ReelView,
)
from django.contrib.auth.admin import UserAdmin


"""Register the talvido user in django admin"""

@admin.register(Talvidouser)
class TalvidouserAdmin(UserAdmin):
    add_form = TalvidouserCreationForm
    form = TalvidouserChangeForm
    model = Talvidouser
    list_display = (
        "firebase_uid",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            "User Information",
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "mobile_number",
                    "firebase_uid",
                    "referral_code",
                )
            },
        ),
        (
            "User Permissions",
            {"fields": ("is_superuser", "is_staff", "is_active", "user_permissions")},
        ),
        ("Login with", {"fields": ("login_with",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("username",)
    ordering = (
        "first_name",
        "last_name",
    )


"""Register profile model in  django admin"""

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ["user", "image", "gender"]


"""Register story model in  django admin"""

@admin.register(Story)
class StoryModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "story", "post_at", "ends_at"]


"""Register storyviews model in  django admin"""

@admin.register(StoryViews)
class StoryViewsModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "story", "created_at"]


"""Register follow model in  django admin"""

@admin.register(Follow)
class FollowModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user_to", "user_from", "created_at", "updated_at"]


"""Register post model in  django admin"""

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "description", "post", "created_at", "updated_at"]


"""Register post comment model in  django admin"""

@admin.register(PostComment)
class PostCommentModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post", "comment", "created_at", "updated_at"]


"""Register post like model in django admin"""

@admin.register(PostLike)
class PostLikeModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post", "created_at", "updated_at"]


"""Register post like model in django admin"""

@admin.register(PostCommentLike)
class PostCommentLikeModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "comment", "created_at", "updated_at"]


"""Register notification model in django admin"""

@admin.register(Notification)
class NotificationModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user_to", "user_from", "notification_type", "post_like", "post_comment", "post_comment_like", "created_at", "updated_at"]


"""Register story highlights model in django admin"""

@admin.register(StoryHighlight)
class StoryHighlightModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "title", "created_at", "updated_at"]


"""Register reel model in django admin"""

@admin.register(Reel)
class ReelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "description", "created_at", "updated_at"]


"""Register reel like model in django admin"""

@admin.register(ReelLike)
class ReelLikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "reel"]


"""Register reel comment model in django admin"""

@admin.register(ReelComment)
class ReelCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "reel"]


"""Register reel comment model in django admin"""

@admin.register(ReelCommentLike)
class ReelCommentLikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "comment"]


"""Register reel comment model in django admin"""

@admin.register(ReelView)
class ReelViewAdmin(admin.ModelAdmin):
    list_display = ["id", "reel", "views"]
