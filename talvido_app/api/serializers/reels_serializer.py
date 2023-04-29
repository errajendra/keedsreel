from rest_framework import serializers
from rest_framework.fields import empty
from talvido_app.models import Reel, ReelComment, ReelLike, ReelCommentLike


""" Reel Comment List, Create, delete Serializer """
class ReelCommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReelCommentLike
        fields = '__all__'
    

""" ReelComment List, Create, delete Serializer """
class ReelCommentSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=..., **kwargs):
        if instance:
            self.comment_likes = ReelCommentLike.objects.filter(comment__in=instance)
        else:
            self.comment_likes = ReelCommentLike.objects.all()
        super().__init__(instance, data, **kwargs)
        
    class Meta:
        model = ReelComment
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['like_count'] = self.comment_likes.filter(comment=instance).count()
        return data
    

""" ReelLike List, Create, delete Serializer """
class ReelLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReelLike
        fields = '__all__'
    

""" Reel List, Create, delete Serializer """
class ReelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reel
        fields = '__all__'
    


""" Reel Detail Serializer """
class ReelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reel
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data['user] = 
        data['comment'] = ReelCommentSerializer(ReelComment.objects.filter(reel=instance), many=True).data
        data['like_count'] = ReelLike.objects.filter(reel=instance).count()
        return data
    
