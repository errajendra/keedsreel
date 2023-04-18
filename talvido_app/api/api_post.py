from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from talvido_app.models import Story
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication
from . import StoryModelSerializer, DeleteStorySerializer
from datetime import datetime


"""This api return the active stories of an user"""

class ActiveStoryAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """filter the active stories of current user"""
        story = Story.objects.filter(user=request.user, ends_at__gt=datetime.today())
        """serialize the data"""
        story_serializer = StoryModelSerializer(
            story, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": story_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


"""This api return the archive stories of an user"""

class ArchiveStoryAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """filter archive stories of current user"""
        story = Story.objects.filter(user=request.user)
        """serialize the data"""
        story_serializer = StoryModelSerializer(
            story, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": story_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


"""This api will create a new story"""

class CreateStoryAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """deserialize the data"""
        create_story_serializer = StoryModelSerializer(data=request.data)
        """checking the validation on data"""
        if create_story_serializer.is_valid():
            create_story_serializer.save(user=request.user)
            response = {"status_code": status.HTTP_201_CREATED, "message": "ok"}
            return Response(response, status=status.HTTP_201_CREATED)

        """return this if validation fails"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": create_story_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This api will delete the story"""

class DeleteStoryAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """deserialize the data"""
        delete_story_serializer = DeleteStorySerializer(data=request.data)
        """checking the validation on data"""
        if delete_story_serializer.is_valid():
            """get the story id"""
            story_id = delete_story_serializer.validated_data.get("story_id")
            """checking the story is belong to the current user or not"""
            if Story.objects.filter(user=request.user, id=story_id).exists():
                delete_story_serializer.delete(id=story_id)
                response = {
                    "status_code": status.HTTP_204_NO_CONTENT,
                    "message": "story deleted",
                }
                return Response(response, status=status.HTTP_204_NO_CONTENT)
            else:
                """response this if story is not belong to the current user or story id is invalid"""
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {
                        "story_id": [
                            "The story id is either invalid nor associate with current user"
                        ]
                    },
                }
                return Response(response, status=status.HTTP_204_NO_CONTENT)

        """return this response if validation fails"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "badd request",
            "data": delete_story_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
