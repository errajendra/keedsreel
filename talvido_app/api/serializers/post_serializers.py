from rest_framework import serializers
from talvido_app.models import Story


""" story model serializer"""

class StoryModelSerializer(serializers.ModelSerializer):
    hours = serializers.SerializerMethodField("get_hours")
    user = serializers.CharField(read_only=True)
    story = serializers.FileField()

    def get_hours(self, data):
        hours = data.ends_at - data.post_at
        return hours.days

    class Meta:
        model = Story
        fields = ["id", "user", "story", "post_at", "ends_at", "hours"]


"""delete story serializer"""

class DeleteStorySerializer(serializers.Serializer):
    story_id = serializers.CharField()

    """this method will delete the story"""

    def delete(self, id):
        Story.objects.get(id=id).delete()
        return None
