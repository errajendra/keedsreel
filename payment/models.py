from django.db import models
from talvido_app.models import BaseModel, Talvidouser


class Transaction(BaseModel):
    PAYMENT_STATUS = (
        ("", ""),
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
    )

    user = models.ForeignKey(
        Talvidouser, verbose_name="User", on_delete=models.SET_NULL, null=True
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
