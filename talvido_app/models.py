from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.core.validators import RegexValidator
from .utils import phone_regex
from .manager import TalvidouserManager
from datetime import datetime, timedelta


"""base model"""

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


"""Modify the regular user"""

class Talvidouser(AbstractUser):
    LOGIN_WITH_CHOICES = (
        ("Mobile Number", "Mobile Number"),
        ("Google", "Google"),
        ("Facebook", "Facebook"),
    )
    firebase_uid = models.CharField(_("Firebase UID"), max_length=100, primary_key=True)
    referral_code = models.CharField(
        _("Referral Code"), max_length=200, unique=True, blank=True, null=True
    )
    username = models.CharField(
        _("Username"), max_length=100, unique=True, blank=True, null=True
    )
    mobile_number = models.CharField(
        _("Mobile Number"),
        max_length=100,
        validators=[phone_regex],
        blank=True,
        null=True,
        unique=True,
    )
    login_with = models.CharField(
        verbose_name=_("Login with"),
        max_length=100,
        choices=LOGIN_WITH_CHOICES,
        default="",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "firebase_uid"
    REQUIRED_FIELDS = []

    objects = TalvidouserManager()

    def __str__(self):
        return str(self.firebase_uid)
    
    def save(self, *args, **kwargs):
        if not self.referral_code:
            code = get_random_string(length=8).upper()
            check = False
            while not check:
                if Talvidouser.objects.filter(referral_code=code).exists():
                    code = get_random_string(length=8).upper()
                else:
                    check = True
            self.referral_code = code
        super().save(*args, **kwargs)
    


"""profile model that will store extra information of user"""

class Profile(BaseModel):
    GENDER_CHOICES = (("MALE", "MALE"), ("FEMALE", "FEMALE"), ("OTHER", "OTHER"))

    user = models.OneToOneField(Talvidouser, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="profile", default="default.png", verbose_name="Profile Image"
    )
    gender = models.CharField(
        verbose_name="Gender", blank=False, choices=GENDER_CHOICES, max_length=100
    )
    location = models.CharField(verbose_name="Location", blank=True, null=True, max_length=100)
    description = models.TextField(verbose_name="Description", blank=True, null=True)

    def __str__(self):
        return str(self.user)


"""story model that will store the story content of users"""

class Story(BaseModel):
    user = models.ForeignKey(Talvidouser, verbose_name="User", on_delete=models.CASCADE)
    story = models.FileField(
        upload_to="story/users/", null=True, blank=True, verbose_name="User Story"
    )
    post_at = models.DateTimeField(
        auto_now=True, editable=False, verbose_name="Story Post At"
    )
    ends_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Post Ends At", editable=False
    )

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.ends_at = datetime.now() + timedelta(hours=24)
        super().save(*args, **kwargs)


"""This model will store the followers and following users"""

class Follow(BaseModel):
    user_to = models.ForeignKey(
        Talvidouser,
        on_delete=models.CASCADE,
        related_name="user_to",
        verbose_name="User To",
    )
    user_from = models.ForeignKey(
        Talvidouser,
        on_delete=models.CASCADE,
        related_name="user_from",
        verbose_name="User From",
    )

    def __str__(self):
        return str(self.user_to)


"""This model will store the stories views"""


class StoryViews(BaseModel):
    user = models.ForeignKey(
        Talvidouser, verbose_name="User", on_delete=models.CASCADE, related_name="user"
    )
    story = models.ForeignKey(
        Story,
        verbose_name="Story",
        related_name="story_content",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.user)


"""This model will store the post data"""

class Post(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="post_user",
    )
    description = models.TextField(
        verbose_name="Post Description", max_length=1000, blank=True, null=True
    )
    post = models.FileField(verbose_name="Post", upload_to="post/users/")

    def __str__(self):
        return str(self.id)


"""This model will store the comments under posts"""

class PostComment(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="post_comment_user",
    )
    post = models.ForeignKey(
        Post, verbose_name="Post", on_delete=models.CASCADE, related_name="post_comment"
    )
    comment = models.TextField(verbose_name="Comment")

    def __str__(self):
        return str(self.id)


"""This model will store post like data"""

class PostLike(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="post_like_user",
    )
    post = models.ForeignKey(
        Post, verbose_name="Post", on_delete=models.CASCADE, related_name="post_like"
    )

    def __str__(self):
        return str(self.id)


"""This model will store post comment like data"""

class PostCommentLike(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="post_comment_like_user",
    )
    comment = models.ForeignKey(
        PostComment,
        verbose_name="Comment",
        on_delete=models.CASCADE,
        related_name="post_comment"
    )

    def __str__(self):
        return str(self.id)


"""This model will store notifications"""

class Notification(BaseModel):

    NOTIFICATION_TYPE = (
        ("POST_LIKE","POST_LIKE"),
        ("POST_COMMENT","POST_COMMENT"),
        ("POST_COMMENT_LIKE","POST_COMMENT_LIKE"),
    )

    user_to = models.ForeignKey(Talvidouser, verbose_name="User To", on_delete=models.CASCADE, related_name="notification_user_to")
    user_from = models.ForeignKey(Talvidouser, verbose_name="User From", on_delete=models.CASCADE, related_name="notification_user_from")
    notification_type = models.CharField(max_length=100, verbose_name="Notification Type", choices=NOTIFICATION_TYPE)
    post_like = models.ForeignKey(PostLike, verbose_name="Post Like", on_delete=models.CASCADE, null=True, blank=True)
    post_comment = models.ForeignKey(PostComment, verbose_name="Post Comment", on_delete=models.CASCADE, null=True, blank=True)
    post_comment_like = models.ForeignKey(PostCommentLike, verbose_name="Post Comment Like", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)


"""This model will store user story highlights"""

class StoryHighlight(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="story_hightlight_user",
    )
    title = models.CharField(verbose_name="Story Highlight Title", max_length=100)
    stories = models.ManyToManyField(Story, verbose_name="Stories")

    def __str__(self):
        return str(self.id)
        

""" Reel data model """

class Reel(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="reel_user",
    )
    description = models.TextField(blank=True, null=True)
    reel = models.FileField(verbose_name="Reel", upload_to="reel/")

    def __str__(self):
        return str(self.id)



"""This model will store the comments under Reels """

class ReelComment(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE
    )
    reel = models.ForeignKey(
        Reel, verbose_name="Reel", on_delete=models.CASCADE
    )
    comment = models.TextField(verbose_name="Comment")

    def __str__(self):
        return str(self.id)



""" This model will store reel like data"""
class ReelLike(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="reel_like_user",
    )
    reel = models.ForeignKey(
        Reel, on_delete=models.CASCADE, related_name="reel_like"
    )
    
    class Meta:
        unique_together = ('user', 'reel')

    def __str__(self):
        return str(self.id)


""" This model will store Reel Comment like data"""
class ReelCommentLike(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="reel_comment_like_user",
    )
    comment = models.ForeignKey(
        ReelComment,
        verbose_name="Comment",
        on_delete=models.CASCADE,
        related_name="reel_comment"
    )

    def __str__(self):
        return str(self.id)


"""This model will store the total views on reels"""

class ReelView(BaseModel):
    reel = models.OneToOneField(
        Reel, on_delete=models.CASCADE, related_name="reel_view_reel", verbose_name="Reel"
    )
    views = models.IntegerField(verbose_name="Reel Views", default=0)

    def __str__(self):
        return str(self.reel)



class BankDetail(BaseModel):
    # user = models.OneToOneField(
    #     Talvidouser,
    #     verbose_name="User",
    #     on_delete=models.CASCADE
    # )
    bank_name = models.CharField(verbose_name="Bank Name", max_length=100)
    account_number = models.CharField(verbose_name="Account Number", max_length=100)
    ifsc_code = models.CharField(verbose_name="IFSC Code", max_length=100)
    account_holder_name = models.CharField(verbose_name="Account Holder Name", max_length=100)

    def __str__(self):
        return str(self.bank_name)


class BankPayment(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="user_bank_payment",
    )
    screenshot = models.FileField(verbose_name="Payment Screenshot", upload_to="bank/")

    def __str__(self):
        return str(self.id)


class CompanyPaymentInfo(BaseModel):
    name = models.CharField(verbose_name="Display Name", max_length=100)
    qrcode = models.ImageField(verbose_name="QRCode", upload_to="qrcode/")
    upi_id = models.CharField(verbose_name="UPI ID", max_length=256, validators=[RegexValidator(
        regex="^[a-zA-Z0-9.-]{2,100}@[a-zA-Z][a-zA-Z]{2,64}$",
        message="Enter a valid UPI ID.")]
    )

    def __str__(self):
        return str(self.name)


class UPIPayment(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="user_upi_payment",
    )
    screenshot = models.FileField(verbose_name="Payment Screenshot", upload_to="upi/")

    def __str__(self):
        return str(self.id)


class RecentAccountSearch(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="user_recent_search",
    )
    search_user = models.ForeignKey(
        Talvidouser,
        verbose_name="Search User",
        on_delete=models.CASCADE,
        related_name="search_user_recent_search",
    )

    def __str__(self):
        return str(self.id)


class Subscription(BaseModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    validity = models.CharField(choices=[('1','1'), ('3','3'), ('6','6'), ('12','12')],
                                max_length=2, default="12", verbose_name="Validity In Months")
    image = models.ImageField(upload_to='subscription-image/', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    

class Level(BaseModel):
    level = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    min_points = models.IntegerField(verbose_name="Minimum point")
    image = models.ImageField(upload_to='levels/', verbose_name="Image", null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    

class ReferralUser(BaseModel):
    user = models.ForeignKey(
        Talvidouser,
        verbose_name="Joined User",
        on_delete=models.CASCADE,
        related_name="referral_user",
    )
    referral_user = models.ForeignKey(
        Talvidouser,
        verbose_name="Refered by User",
        on_delete=models.CASCADE,
        related_name="referral_by_user",
    )
    
    def __str__(self) -> str:
        return str(self.id)
    
    def jonied_user(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

    def referred_user(self):
        return str(self.referral_user.first_name) + " " + str(self.referral_user.last_name)


class PointSetting(BaseModel):
    activity = models.CharField(
        choices=[
            ('Time Spends', 'Time Spends'),
            ('Referral', 'Referral'),
            ('Share', 'Share'),
            ('Comments', 'Comments'),
            ('Like', 'Like'),
        ],
        verbose_name="User Activity",
        unique=True,
        max_length=100
        )
    count = models.IntegerField(
        verbose_name="Activity Perform Count")
    points = models.FloatField(
        verbose_name="Points",
        help_text="""Point will be added on user points when user perform activity on
        given Activity Perform Count."""
        )
    
    def __str__(self) -> str:
        return f"{self.activity} - {self.count} - {self.points}"
    

class Point(BaseModel):
    user = models.OneToOneField(
        Talvidouser,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="user_point",
    )
    points = models.FloatField(verbose_name="Points")
    
    def __str__(self) -> str:
        return f"{self.activity} - {self.points}"
