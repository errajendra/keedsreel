from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class TalvidouserManager(BaseUserManager):
    """
    Custom user model manager where firebase is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, firebase_uid, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not firebase_uid:
            raise ValueError(_("The Firebase uid must be set"))
        user = self.model(firebase_uid=firebase_uid, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, firebase_uid, password, **extra_fields):
        """
        Create and save a SuperUser with the given firebase_uid and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(firebase_uid, password, **extra_fields)
