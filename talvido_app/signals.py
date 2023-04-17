from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import (
    Talvidouser,
    Profile,
)


"""this signal will create user profile, when new user get created"""
@receiver(post_save, sender=Talvidouser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
