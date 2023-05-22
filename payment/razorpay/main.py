from . import client
from rest_framework.serializers import ValidationError
from rest_framework import status


class RazorpayClient():

    """This method will create an order"""
    def create_order(self, amount, currency, receipt=None):
        self.data = {"amount": amount, "currency": currency, "receipt": receipt}
        try:
            self.payment = client.order.create(data=self.data)
        except Exception as e:
            raise ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": e,
                }
            )
        return self.payment

    """This method will verify payment signature"""
    def verify_payment_signature(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        try:
            client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
            })
        except Exception as e:
            raise ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": e,
                }
            )
        return True
