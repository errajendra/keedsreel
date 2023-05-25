from .models import TimeSpend
from datetime import datetime


class TimeSpendsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response =  self.get_response(request)
        if request.user.is_authenticated:
            time_spends = TimeSpend.objects.filter(user=request.user, date=datetime.now())
            if time_spends.exists():
                time_spends = time_spends.first()
                time_spends.seconds += .5
                time_spends.save()
            else:
                TimeSpend.objects.create(user=request.user, seconds=.5)
        return response
