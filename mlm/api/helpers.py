from talvido_app.models import Talvidouser
from ..models import Level


class UserLevel:
    def __init__(self, user, request):
        self.request = request
        self.user = Talvidouser.objects.get(firebase_uid=user)
        self.referral_users = self.user.referral_by_user.all()

    def get_level_referral_team(self, level=None):
        if level:
            try:
                return Level.objects.get(level=level)
            except:
                return Level.objects.get(level=7)
        return None

    def get_indirect_joined_user(self, user, many=None):
        if many is None:
            try:
                user = Talvidouser.objects.get(firebase_uid=user)
                return user.referral_by_user.all().values_list("user", flat=True)
            except Talvidouser.DoesNotExist:
                return None
        else:
            users = Talvidouser.objects.filter(firebase_uid__in=user)
            self.indirect_joined_users = []
            for idr_jnd_usrs in range(len(users)):
                get_referral_user_info = users.get(
                    firebase_uid=users[idr_jnd_usrs]
                ).referral_by_user.all()
                for get_idr_jnd_usrs in range(len(get_referral_user_info)):
                    self.indirect_joined_users.append(
                        get_referral_user_info[get_idr_jnd_usrs].user.firebase_uid
                    )
            return self.indirect_joined_users

    def get_direct_joined_user(self, ref_users, end=None):
        self.user_data = self.referral_users.order_by("created_at").values_list("user", flat=True)[
            ref_users - 1 : end
        ]
        return self.user_data

    def get_user_info(self, data):
        self.user_info = []
        for i in range(len(data)):
            talvido_user = Talvidouser.objects.get(firebase_uid=data[i])
            self.user_info.append(
                {
                    "firebase_uid": talvido_user.firebase_uid,
                    "full_name": talvido_user.first_name + " " + talvido_user.last_name,
                    "image": "https://" + self.request.META["HTTP_HOST"] + talvido_user.profile.image.url
                }
            )
        return self.user_info

    @property
    def create_level_info(self):
        self.levels_info = []
        for ref_users in range(1, self.referral_users.count() + 1)[:11]:
            if ref_users <= 4:
                self.levels_info.append(
                    {
                        "level": self.get_level_referral_team(level=ref_users).level,
                        "max_referral_team": self.get_level_referral_team(
                            level=ref_users
                        ).referral_team,
                        "daily_income": self.get_level_referral_team(
                            level=ref_users
                        ).daily_income,
                        "direct_joined_user": 
                            self.get_user_info(
                                data = self.get_direct_joined_user(
                                ref_users=ref_users, end=ref_users
                                )
                            )
                        ,
                        "indirect_joined_users": self.get_user_info(
                            data = self.get_indirect_joined_user(
                                user=self.get_direct_joined_user(
                                    ref_users=ref_users, end=ref_users
                                )
                            )
                        ),
                        "current_referral_team": len(
                            self.get_indirect_joined_user(
                                user=self.get_direct_joined_user(
                                    ref_users=ref_users, end=ref_users
                                )
                            )
                        ),
                    }
                )
            elif ref_users == 6 or ref_users == 8 or ref_users == 10:
                self.ref_user = (
                    ref_users - 2
                    if ref_users >= 8 and ref_users <= 10
                    else ref_users - 1
                )
                self.dir_jnd_usr = self.get_direct_joined_user(
                    ref_users=self.ref_user + 1
                    if ref_users >= 8 and ref_users <= 10
                    else self.ref_user,
                    end=ref_users,
                )
                self.dir_jnd_usr = [
                    self.dir_jnd_usr[dir_jned_usr]
                    for dir_jned_usr in range(len(self.dir_jnd_usr))
                ]
                self.levels_info.append(
                    {
                        "level": self.get_level_referral_team(
                            level=self.ref_user
                        ).level,
                        "max_referral_team": self.get_level_referral_team(
                            level=self.ref_user
                        ).referral_team,
                        "daily_income": self.get_level_referral_team(
                            level=self.ref_user
                        ).daily_income,
                        "direct_joined_user": self.get_user_info(
                            data = self.dir_jnd_usr
                        ),
                        "indirect_joined_users": self.get_user_info(
                            data = self.get_indirect_joined_user(
                                user=self.dir_jnd_usr, many=True
                            )
                        ),
                        "current_referral_team": len(
                            self.get_indirect_joined_user(
                                user=self.dir_jnd_usr, many=True
                            )
                        ),
                    }
                )

        return self.levels_info


class UserWallet(object):
    def __init__(self, user, request):
        self.user_level = UserLevel(user, request)
        self.user_levels_info = self.user_level.create_level_info
