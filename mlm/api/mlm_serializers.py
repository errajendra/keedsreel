from rest_framework import serializers
from mlm.models import WalletHistory


class WalletModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WalletHistory
        fields = ["user", "amount", "date"]

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data["activity"] = "browsing"
        return data
