from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import (
    Talvidouser,
    Profile,
    Reel,
    ReelView,
    PostLike,
    Notification,
    PostComment,
    Follow,
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


"""this signal will create post like """
@receiver(post_save, sender=PostLike)
def create_postlike_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user_to = instance.post.user,
            user_from = instance.user,
            notification_type = "POST_LIKE",
            post_like = instance,
        )

"""this signal will create post comment """
@receiver(post_save, sender=PostComment)
def create_postcomment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user_to = instance.post.user,
            user_from = instance.user,
            notification_type = "POST_COMMENT",
            post_comment = instance,
        )

"""this signal will create post comment """
@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user_to = instance.user_to,
            user_from = instance.user_from,
            notification_type = "FOLLOW",
            follow = instance,
        )
