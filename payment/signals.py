from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Transaction, UserSubscription


"""this signal will create user subscription, when new transaction succeed"""
@receiver(post_save, sender=Transaction)
def create_user_subscription(sender, instance, created, **kwargs):
    if created and instance.status == "SUCCESS":
        UserSubscription.objects.create(user=instance.user)
