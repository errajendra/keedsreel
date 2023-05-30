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
        data["last_message"] = decrypt_message(
            encoded_message=self.get_last_message(instance).encode("utf_8")
        )
        return data

    def get_last_message(self, data):
        last_message = Chat.objects.select_related().filter(
            sender__in=[data.sender, data.reciever],
            reciever__in=[data.reciever, data.sender],
        )

        return last_message.order_by("-created_at")[0].message if last_message else None


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
        decode_msg = decrypt_message(encoded_message=data.message.encode("utf_8"))
        return decode_msg
