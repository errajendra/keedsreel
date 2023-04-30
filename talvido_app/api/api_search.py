from rest_framework import status
from rest_framework.response import Response
from talvido_app.models import Talvidouser, Post
from talvido_app.api.serializers.search_serializers import (
    SearchByUsernameModelSerializer,
)
from talvido_app.api.serializers.post_serializers import GetPostModelSerializer
from rest_framework.views import APIView


"""This API will search the user account by username and 
    return the result if matched"""

class SearchByUsernameAPIView(APIView):
    def get(self, request):
        search_username = request.query_params.get("username", " ")
        user = Talvidouser.objects.filter(username__icontains=search_username)
        user_serializer = SearchByUsernameModelSerializer(
            user, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": user_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


"""This API will search the post by its description"""

class SearchPostAPIView(APIView):
    def get(self, request):
        post_query = request.query_params.get("post", " ")
        post = Post.objects.filter(description__icontains=post_query)
        post_serializer = GetPostModelSerializer(
            post, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": post_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
