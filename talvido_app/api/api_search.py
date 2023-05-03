from rest_framework import status
from rest_framework.response import Response
from talvido_app.models import Talvidouser, Post
from talvido_app.api.serializers.search_serializers import (
    SearchByUsernameModelSerializer,
)
from talvido_app.api.serializers.post_serializers import GetPostModelSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication


"""This API will search the user account by username and 
    return the result if matched"""

class SearchByUsernameAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """get the query parameter username"""
        search_username = request.query_params.get("username", " ")

        """checking the username is avaliable in database"""
        user = Talvidouser.objects.filter(username__icontains=search_username)

        """serialize the data and return the response"""
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
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """get the query parameter post"""
        post_query = request.query_params.get("post", " ")

        """checking the post is avaliable in database"""
        post = Post.objects.filter(description__icontains=post_query)

        """serialize the data and return the response"""
        post_serializer = GetPostModelSerializer(
            post, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": post_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
