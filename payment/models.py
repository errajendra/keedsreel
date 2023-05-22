from django.db import models
from talvido_app.models import BaseModel, Talvidouser


class Transaction(BaseModel):
    PAYMENT_STATUS = (
        ("", ""),
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
        ("CANCELLED", "CANCELLED"),
    )

    user = models.ForeignKey(
        Talvidouser, verbose_name="User", on_delete=models.SET_NULL, null=True, related_name="transaction_user"
    )
    payment_id = models.CharField(max_length=200, verbose_name="Payment ID")
    order_id = models.CharField(max_length=200, verbose_name="Order ID")
    signature = models.CharField(
        max_length=300, verbose_name="Signature", blank=True, null=True
    )
    status = models.CharField(
        verbose_name="Payment Status",
        max_length=100,
        choices=PAYMENT_STATUS,
        default="",
    )
    amount = models.IntegerField(verbose_name="Amount")

    def __str__(self):
        return str(self.user)


class UserSubscription(BaseModel):
    user = models.ForeignKey(
        Talvidouser, verbose_name="User", on_delete=models.CASCADE, null=True, related_name="subscription_user"
    )

    def subscription_end_date(self):
        from datetime import date
        startDate = self.created_at
        endDate = date(startDate.year + 1, startDate.month, startDate.day)
        endDate = startDate.replace(startDate.year + 1)
        return endDate

    def __str__(self):
        return str(self.user)
