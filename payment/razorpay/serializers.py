from rest_framework import serializers


class CreateOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField()
    reciept = serializers.CharField(allow_blank=True, required=False)
