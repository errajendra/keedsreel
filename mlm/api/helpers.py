from talvido_app.models import Talvidouser
from ..models import Level


class UserLevel:
    def __init__(self, user):
        self.user = Talvidouser.objects.get(firebase_uid=user)
        self.referral_users = self.user.referral_by_user.all().count()

    def get_level_referral_user(self, level):
        return Level.objects.get(level=level)

    def check_level(self, max_level):
        for i in range(1, max_level + 1):
            try:
                if (
                    self.referral_users
                    >= self.get_level_referral_user(level=i).referral_users
                    and self.referral_users
                    < self.get_level_referral_user(level=i + 1).referral_users
                ):
                    return i
            except:
                return max_level

    @property
    def get_user_level(self):
        return self.check_level(max_level=7)

    @property
    def get_level_max_users(self):
        self.get_level = self.check_level(max_level=7)
        try:
            return self.get_level_referral_user(self.get_level+1).referral_users
        except:
            return self.get_level_referral_user(self.get_level).referral_users 

    @property
    def get_total_referral_users(self):
        return self.referral_users
