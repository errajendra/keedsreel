from rest_framework import status
from rest_framework.response import Response
from talvido_app.models import Talvidouser, Post
from talvido_app.api.serializers.search_serializers import (
    SearchAccountModelSerializer,
    AddRecentSearchSerializer,
)
from talvido_app.api.serializers.post_serializers import GetPostModelSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication
from django.db.models import Q


"""This API will search the user account by username and 
    return the result if matched"""

class SearchAccountAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """get the query parameter username"""
        search_username = request.query_params.get("username", " ")

        """checking the account is avaliable in database"""
        user = Talvidouser.objects.filter(
            Q(username__icontains=search_username)
            | Q(first_name__icontains=search_username)
            | Q(last_name__icontains=search_username)
        )

        """serialize the data and return the response"""
        user_serializer = SearchAccountModelSerializer(
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


""""This API will get, post, delete recent account"""

class RecentAccountSearchAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recent_search_account = Talvidouser.objects.get(
            firebase_uid=request.user
        ).user_recent_search.all()
        users = Talvidouser.objects.filter(
            firebase_uid__in=recent_search_account.values_list("search_user", flat=True)
        )
        user_serializer = SearchAccountModelSerializer(
            users, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": user_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        add_recent_account_search_serializer = AddRecentSearchSerializer(
            data=request.data, context={"request": request}
        )
        if add_recent_account_search_serializer.is_valid():
            add_recent_account_search_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "created",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": add_recent_account_search_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        delete_recent_account_search_serializer = AddRecentSearchSerializer(
            data=request.data, context={"request": request}
        )
        if delete_recent_account_search_serializer.is_valid():
            delete_recent_account_search_serializer.delete()
            response = {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "created",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": delete_recent_account_search_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
