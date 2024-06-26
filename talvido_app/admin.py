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
    BankDetail,
    BankPayment,
    CompanyPaymentInfo,
    UPIPayment,
    RecentAccountSearch,
    ReferralUser,
    PointSetting,
    Point,
    TimeSpend,
)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


admin.site.site_header = "Talvido Administration"
admin.site.index_title = "Talvido"
admin.site.site_title = "Talvido Administration"
admin.site.unregister(Group)


class BaseModelAdmin(admin.ModelAdmin):
    """Base model admin that will hold common data for all
    other model admins.
    """

    """This method will display first and last 
    name of user"""

    def name(self, instance):
        return instance.user.first_name + " " + instance.user.last_name

@admin.register(Talvidouser)
class TalvidouserAdmin(UserAdmin):
    """Customize the custom user model"""

    add_form = TalvidouserCreationForm
    form = TalvidouserChangeForm
    model = Talvidouser
    list_display = (
        "firebase_uid",
        "email",
        "first_name",
        "last_name",
        "is_active",
    )
    list_filter = ("is_active",)
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
    search_fields = ("firebase_uid", "email", "first_name", "last_name")
    ordering = (
        "first_name",
        "last_name",
    )


"""Register profile model in  django admin"""

@admin.register(Profile)
class ProfileModelAdmin(BaseModelAdmin):
    list_display = ["user", "name", "image", "gender", "location", "description"]
    list_filter = ("gender",)
    search_fields = ("user",)

    def get_search_results(self, request, queryset, search_term):
        search_term_list = search_term.split(" ")

        if not any(search_term_list):
            return queryset, False

        queryset = Profile.objects.filter(user=search_term_list[0])
        return queryset, False


"""Register story model in  django admin"""

@admin.register(Story)
class StoryModelAdmin(BaseModelAdmin):
    list_display = ["id", "user", "name", "story", "post_at", "ends_at"]


"""Register storyviews model in  django admin"""

@admin.register(StoryViews)
class StoryViewsModelAdmin(BaseModelAdmin):
    list_display = ["id", "user", "name", "story", "created_at"]


"""Register follow model in  django admin"""

@admin.register(Follow)
class FollowModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user_to", "user_from", "created_at", "updated_at"]


"""Register post model in  django admin"""

@admin.register(Post)
class PostModelAdmin(BaseModelAdmin):
    list_display = [
        "id",
        "user",
        "name",
        "description",
        "post",
        "created_at",
        "updated_at",
    ]


"""Register post comment model in  django admin"""

@admin.register(PostComment)
class PostCommentModelAdmin(BaseModelAdmin):
    list_display = ["id", "user", "name", "post", "comment", "created_at", "updated_at"]


"""Register post like model in django admin"""

@admin.register(PostLike)
class PostLikeModelAdmin(BaseModelAdmin):
    list_display = ["id", "user", "name", "post", "created_at", "updated_at"]


"""Register post like model in django admin"""

@admin.register(PostCommentLike)
class PostCommentLikeModelAdmin(BaseModelAdmin):
    list_display = ["id", "user", "name", "comment", "created_at", "updated_at"]


"""Register notification model in django admin"""

@admin.register(Notification)
class NotificationModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user_to",
        "user_from",
        "notification_type",
        "post_like",
        "post_comment",
        "follow",
        "seen",
        "created_at",
        "updated_at",
    ]


"""Register story highlights model in django admin"""

@admin.register(StoryHighlight)
class StoryHighlightModelAdmin(BaseModelAdmin):
    list_display = ["id", "user", "name", "title", "created_at", "updated_at"]


"""Register reel model in django admin"""

@admin.register(Reel)
class ReelAdmin(BaseModelAdmin):
    list_display = [
        "id",
        "user",
        "name",
        "description",
        "thumbnail",
        "created_at",
        "updated_at",
    ]


"""Register reel like model in django admin"""

@admin.register(ReelLike)
class ReelLikeAdmin(BaseModelAdmin):
    list_display = ["id", "user", "name", "reel"]


"""Register reel comment model in django admin"""

@admin.register(ReelComment)
class ReelCommentAdmin(BaseModelAdmin):
    list_display = ["id", "user", "name", "reel"]


"""Register reel comment model in django admin"""

@admin.register(ReelCommentLike)
class ReelCommentLikeAdmin(BaseModelAdmin):
    list_display = ["id", "user", "name", "comment"]


"""Register reel comment model in django admin"""

@admin.register(ReelView)
class ReelViewAdmin(admin.ModelAdmin):
    list_display = ["id", "reel", "views"]


"""Register bank details model in django admin"""

@admin.register(BankDetail)
class BankDetailAdmin(admin.ModelAdmin):
    list_display = ["id", "bank_name", "account_number", "account_holder_name"]


"""Register bank payment model in django admin"""

@admin.register(BankPayment)
class BankPaymentAdmin(BaseModelAdmin):
    list_display = ["id", "name", "screenshot", "approve", "created_at"]


"""Register company payment info model in django admin"""

@admin.register(CompanyPaymentInfo)
class CompanyPaymentInfoAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "qrcode", "upi_id", "created_at"]


"""Register upi payment model in django admin"""

@admin.register(UPIPayment)
class UPIPaymentAdmin(BaseModelAdmin):
    list_display = ["id", "name", "screenshot", "approve", "created_at"]


"""Register upi payment model in django admin"""

@admin.register(RecentAccountSearch)
class RecentAccountSearchAdmin(BaseModelAdmin):
    list_display = ["id", "user", "name", "search_user", "created_at"]


"""Register upi payment model in django admin"""

@admin.register(ReferralUser)
class ReferalUserAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "referral_user", "created_at"]


"""Register point setting model in django admin"""

@admin.register(PointSetting)
class PointSettingAdmin(admin.ModelAdmin):
    list_display = ["id", "activity", "count", "points", "created_at"]


"""Register point model in django admin"""

@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "points", "created_at"]


"""Register time spends model in django admin"""

@admin.register(TimeSpend)
class TimeSpendAdmin(BaseModelAdmin):
    list_display = ["id", "user", "name", "date", "seconds", "created_at"]
