from rest_framework import serializers, status
from talvido_app.models import Talvidouser, Profile, RecentAccountSearch


"""search by username model serializer"""

class SearchAccountModelSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image")

    class Meta:
        model = Talvidouser
        fields = ["firebase_uid", "username", "first_name", "last_name", "image"]
    
    """this method will return the user profile image url"""

    def get_image(self, data):
        profile = Profile.objects.get(user=data.firebase_uid)
        return "https://" + self.context["request"].META["HTTP_HOST"] + profile.image.url


class AddRecentSearchSerializer(serializers.Serializer):
    user_firebase_id = serializers.CharField()

    def create(self, validated_data):
        search_user = validated_data.get("user_firebase_id")
        try:
            user = Talvidouser.objects.get(firebase_uid=search_user)
        except Talvidouser.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "bad request",
                    "data" : {
                        "user_firebase_id" : [
                            "user_firebase_id is invalid"
                        ]
                    }
                }
            )
        return RecentAccountSearch.objects.get_or_create(
            user = self.context["request"].user,
            search_user = user
        )
