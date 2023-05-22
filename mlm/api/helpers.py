from talvido_app.models import Talvidouser
from ..models import Level


class UserLevel:
    def __init__(self, request):
        self.user = Talvidouser.objects.get(firebase_uid=request.user)
        self.referral_users = self.user.referral_by_user.all().count()
        self.levels = Level.objects.all()

    def get_level_referral_user(self, level):
        return self.levels.get(level=level)

    def check_level(self, level):
        for i in range(1, level + 1):
            try:
                if (
                    self.referral_users
                    >= self.get_level_referral_user(level=i).referral_users
                    and self.referral_users
                    < self.get_level_referral_user(level=i + 1).referral_users
                ):
                    return i
            except:
                return 7

    def get_user_level(self):
        return self.check_level(7)
