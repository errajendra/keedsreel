from rest_framework import serializers
from chat.models import Chat
from talvido_app.api.serializers.profile_serializers import UserModelSerializer


class GetChatModelSerializer(serializers.ModelSerializer):
    reciever = UserModelSerializer()

    class Meta:
        model = Chat
        fields = ["reciever"]

    def to_representation(self, instance):
        data  = super().to_representation(instance)
        data["reciever"]["image"] = (
            "https://" + 
            self.context["request"].META["HTTP_HOST"] 
            + 
            instance.reciever.profile.image.url
        )
        return data
