from payment.models import UserSubscription


def check_user_subscription(request):
    subscription = UserSubscription.objects.filter(user=request.user).order_by(
            "-created_at"
        )
    from datetime import datetime

    if (
        subscription.exists()
        and subscription.first().subscription_end_date().replace(tzinfo=None)
        >= datetime.now()
    ):
        return True, subscription
    return False, subscription
