from .models import TimeSpend, Talvidouser
from mlm.models import WalletHistory
from datetime import datetime
from payment.helpers import check_user_subscription


class TimeSpendsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            time_spends = TimeSpend.objects.filter(
                user=request.user, date=datetime.now()
            )
            if time_spends.exists():
                time_spends = time_spends.first()
                time_spends.seconds += 0.5
                time_spends.save()
            else:
                TimeSpend.objects.create(user=request.user, seconds=0.5)
        return response


class WalletHistoryMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            time_spend = TimeSpend.objects.filter(
                user=request.user, date=datetime.now()
            )
            referrals = (
                Talvidouser.objects.get(firebase_uid=request.user)
                .referral_by_user.all()
                .count()
            )
            has_subscribe, subscribe = check_user_subscription(request=request)
            if (
                time_spend.exists()
                and time_spend.first().seconds >= 1800
                and referrals >= 1
                and has_subscribe
            ):
                if not WalletHistory.objects.filter(
                    user=request.user, date=datetime.now()
                ).exists():
                    WalletHistory.objects.create(
                        user=request.user,
                        amount=20,
                    )
        return response
