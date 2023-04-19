from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from talvido_app.models import Story, StoryViews
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication
from . import (
    StoryModelSerializer,
    DeleteStorySerializer,
    StoryViewModelSerializer,
    AddStoryViewSerializer,
)
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


"""This API will get the views and add the views to the story"""

class StoryViewAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            story_id = request.query_params.get("story_id")
            story_view = StoryViews.objects.select_related().filter(story=story_id)
            story_view_serializer = StoryViewModelSerializer(story_view,many=True,context={"request":request})
            response = {
                "status_code" : status.HTTP_200_OK,
                "message" : "ok",
                "data" : {
                    "users" : story_view_serializer.data,
                    "story_views" : story_view.count()
                }
            }
            return Response(response,status=status.HTTP_200_OK)
        except:
            response = {
                "status_code" : status.HTTP_400_BAD_REQUEST,
                "message" : "bad request",
                "data" : {  
                    "story_id" : [
                        "The story_id query params is invalid, make sure it should be integer like (1, 2, 3)"
                    ]
                }
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        add_storyview_serializer = AddStoryViewSerializer(data=request.data,context={"request":request})
        if add_storyview_serializer.is_valid():
            add_storyview_serializer.save()
            response = {
                "status" : status.HTTP_200_OK,
                "message" : "ok"
            }
            return Response(response,status=status.HTTP_200_OK)
        
        """return this response if validation fails"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "badd request",
            "data": add_storyview_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
