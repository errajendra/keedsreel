from rest_framework import serializers
from talvido_app.models import Story


class StoryModelSerializer(serializers.ModelSerializer):

    hours = serializers.SerializerMethodField('get_hours')

    def get_hours(self, data):
        hours =  data.ends_at - data.post_at
        return hours.days

    class Meta:
        model = Story
        fields = ['user','story','post_at','ends_at','hours']
