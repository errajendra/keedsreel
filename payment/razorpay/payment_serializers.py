from rest_framework import serializers
from payment.models import Transaction


class CreateOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField()
    receipt = serializers.CharField(allow_blank=True, required=False)


class TransactionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["order_id", "payment_id", "signature", "amount", "status"]
