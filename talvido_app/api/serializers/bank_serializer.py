from rest_framework import serializers
from talvido_app.models import BankDetail, BankPayment


class BankDetailsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankDetail
        fields = ["bank_name", "account_number", "ifsc_code", "account_holder_name"]
    
    def update(self, instance, validated_data):
        Bank_details = BankDetail.objects.get(user=instance)
        Bank_details.bank_name = validated_data.get("bank_name")
        Bank_details.account_number = validated_data.get("account_number")
        Bank_details.ifsc_code = validated_data.get("ifsc_code")
        Bank_details.account_holder_name = validated_data.get("account_holder_name")
        Bank_details.save()
        return Bank_details


class BankPaymentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankPayment
        fields = ["screenshot"]
