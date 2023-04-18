from rest_framework import serializers
from talvido_app.models import Story


class StoryModelSerializer(serializers.ModelSerializer):

    hours = serializers.SerializerMethodField('get_hours')
    user = serializers.CharField(read_only=True)
    story = serializers.FileField()

    def get_hours(self, data):
        hours =  data.ends_at - data.post_at
        return hours.days

    class Meta:
        model = Story
        fields = ['user','story','post_at','ends_at','hours']
