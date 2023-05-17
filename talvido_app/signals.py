from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import (
    Talvidouser,
    Profile,
    Reel,
    ReelView,
)


"""this signal will create user profile, when new user get created"""
@receiver(post_save, sender=Talvidouser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


"""this signal will create reel view, when new reel get created"""
@receiver(post_save, sender=Reel)
def create_reelview(sender, instance, created, **kwargs):
    if created:
        ReelView.objects.create(reel=instance)
