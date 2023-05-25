from django.db import models
from talvido_app.models import BaseModel, Talvidouser


class Level(BaseModel):
    level = models.IntegerField(verbose_name="Level")
    referral_users = models.IntegerField(verbose_name="Referral Users")

    def __str__(self):
        return str(self.level)


class WalletHistory(BaseModel):
    user = models.ForeignKey(
        Talvidouser, 
        verbose_name="User",
        related_name="user_wallet_history",
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(verbose_name="Amount")
    date = models.DateField(verbose_name="Date", auto_now_add=True)

    def __str__(self):
        return str(self.user)
