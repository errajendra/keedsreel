from . import client
from rest_framework.serializers import ValidationError
from rest_framework import status


class razorpayClient():

    """This method will create an order"""
    def create_order(self, amount, currency, receipt=None):
        self.data = {"amount": amount, "currency": currency, "receipt": receipt}
        try:
            self.payment = client.order.create(data=self.data)
        except Exception as e:
            raise ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": e
                }
            )
        return self.payment
