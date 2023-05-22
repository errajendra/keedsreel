from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Transaction, UserSubscription
from payment.razorpay.main import RazorpayClient


"""this signal will create user subscription, when new transaction succeed"""
@receiver(post_save, sender=Transaction)
def create_user_subscription(sender, instance, created, **kwargs):
    if created and instance.status == "SUCCESS":
        razorpay = RazorpayClient()
        razorpay.verify_payment_signature(
            razorpay_order_id = instance.order_id,
            razorpay_payment_id = instance.payment_id,
            razorpay_signature = instance.signature
        )
        UserSubscription.objects.create(user=instance.user)
