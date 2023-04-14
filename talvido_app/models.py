from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .utils import phone_regex
from .manager import TalvidouserManager


"""Modify the regular user"""

class Talvidouser(AbstractUser):
    LOGIN_WITH_CHOICES = (
        ("Mobile Number", "Mobile Number"),
        ("Google", "Google"),
        ("Facebook", "Facebook"),
    )

    first_name = None
    last_name = None
    full_name = models.CharField(_("Full Name"), max_length=100, blank=True, null=True)
    firebase_uid = models.CharField(_("Firebase UID"), max_length=100, primary_key=True)
    referral_code = models.CharField(_("Referral Code"), max_length=200, blank=True, null=True)
    username = models.CharField(_("Username"), max_length=100, unique=True, blank=True, null=True)
    mobile_number = models.CharField(
        _("Mobile Number"),
        max_length=100,
        validators=[phone_regex],
        blank=True,
        null=True,
        unique=True
    )
    login_with = models.CharField(
        verbose_name=_("Login with"), max_length=100, choices=LOGIN_WITH_CHOICES, default='', blank=True, null=True
    )

    USERNAME_FIELD = "firebase_uid"
    REQUIRED_FIELDS = []

    objects = TalvidouserManager()

    def __str__(self):
        return str(self.firebase_uid)
