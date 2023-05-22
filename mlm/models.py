from django.db import models
from talvido_app.models import BaseModel


class Level(BaseModel):
    level = models.IntegerField(verbose_name="Level")
    referral_users = models.IntegerField(verbose_name="Referral Users")

    def __str__(self):
        return str(self.level)
