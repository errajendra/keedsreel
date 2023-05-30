from rest_framework import serializers
from chat.models import Chat
from talvido_app.api.serializers.profile_serializers import UserModelSerializer
from chat.helpers import decrypt_message


class GetChatModelSerializer(serializers.ModelSerializer):
    reciever = UserModelSerializer()

    class Meta:
        model = Chat
        fields = ["reciever"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["reciever"]["image"] = (
            "https://"
            + self.context["request"].META["HTTP_HOST"]
            + instance.reciever.profile.image.url
        )
        return data


class GetParticularUserChatModelSerializer(serializers.ModelSerializer):
    sender = UserModelSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ["id", "sender", "message", "seen", "created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["message"] = self.decode_msg(instance)
        data["sender"]["image"] = (
            "https://"
            + self.context["request"].META["HTTP_HOST"]
            + instance.sender.profile.image.url
        )
        return data

    def decode_msg(self, data):
        decode_msg =  decrypt_message(encoded_message=data.message.encode('utf_8'))
        return decode_msg
