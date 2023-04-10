from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .utils import phone_regex


class Talvidouser(AbstractUser):

    LOGIN_WITH_CHOICES = (
        ("Mobile Number","Mobile Number"),
        ("Google","Google"),
        ("Facebook","Facebook")
    )

    first_name = None
    last_name = None
    full_name = models.CharField(_("Full Name"), max_length=100, blank=True, null=True)
    mobile_number = models.CharField(_("Mobile Number"), max_length=100, validators=[phone_regex], blank=True, null=True)
    login_with = models.CharField(verbose_name=_("Login with"), max_length=100, choices=LOGIN_WITH_CHOICES)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
