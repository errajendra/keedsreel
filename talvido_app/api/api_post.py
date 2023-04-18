from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from talvido_app.models import Story
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication
from . import (
    StoryModelSerializer
)
from datetime import datetime


"""This api return the active stories of an user"""

class ActiveStoryAPIView(APIView):

    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        story = Story.objects.filter(user=request.user,ends_at__gt=datetime.today())
        story_serializer = StoryModelSerializer(story,many=True,context={"request":request})
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "data" : story_serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)



"""This api return the archive stories of an user"""

class ArchiveStoryAPIView(APIView):

    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        story = Story.objects.filter(user=request.user)
        story_serializer = StoryModelSerializer(story,many=True,context={"request":request})
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "data" : story_serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)



class CreateStoryAPIView(APIView):

    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):

        create_story_serializer = StoryModelSerializer(data=request.data)
        if create_story_serializer.is_valid():
            response = {
                "status_code" : status.HTTP_201_CREATED,
                "message" : "ok"
            }
            return Response(response,status=status.HTTP_201_CREATED)
        
        response = {
            "status_code" : status.HTTP_400_BAD_REQUEST,
            "message" : "bad request",
            "data" : create_story_serializer.errors
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
