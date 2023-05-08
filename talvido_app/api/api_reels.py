from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers.reels_serializer import (
    GetReelModelSerializer,
    UploadUserReelsModelSerializer,
    AddReelViewsSerializer,
    AddReelLikeSerializer,
    AddReelCommentSerializer,
    RemoveReelCommentSerializer,
    AddReelCommentLikeSerializer
)
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication
from talvido_app.models import Talvidouser, Reel, ReelLike
from talvido_app.pagination import PageNumberPaginationView


"""This API will get the user all and particular reels"""

class GetUserReelsAPIView(APIView, PageNumberPaginationView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    page_size = 9
    def get(self, request, id=None):
        if id is None:
            user = Talvidouser.objects.get(firebase_uid=request.user)
            user_reels = user.reel_user.all()
            reels_paginated = self.paginate_queryset(user_reels, request, view=self)
            reels_serializer = GetReelModelSerializer(
                reels_paginated, many=True, context={"request": request}
            )
            return self.get_paginated_response(reels_serializer.data)
        else:
            try:
                reel = Reel.objects.get(id=id)
            except Reel.DoesNotExist:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": [{"reel_id": "This reel_id is invalid"}],
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            reels_serializer = GetReelModelSerializer(
                reel, context={"request": request}
            )
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "ok",
                "data": reels_serializer.data,
            }
        return Response(response, status=status.HTTP_200_OK)


"""This API will upload new reel for current authenticate user"""

class UploadUserReelsAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        upload_reels_serializer = UploadUserReelsModelSerializer(data=request.data)
        if upload_reels_serializer.is_valid():
            upload_reels_serializer.save(user=request.user)
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "reel uploaded",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": upload_reels_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API will get all user reels"""

class GetUsersAllReelsAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reels = Reel.objects.select_related()
        all_reels_serializer = GetReelModelSerializer(
            reels, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": all_reels_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


"""This API will get all the trendings reels"""

class GetTrendingReelsAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reels = Reel.objects.select_related()[:5]
        all_reels_serializer = GetReelModelSerializer(
            reels, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": all_reels_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

class AddReelViewAPIView(APIView):
    def post(self, request):
        reel_view_serializer = AddReelViewsSerializer(data=request.data)
        if reel_view_serializer.is_valid():
            reel_view_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "reels view count",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": reel_view_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class AddReelLikeAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        add_reel_like_serializer = AddReelLikeSerializer(
            data=request.data, context={"request": request}
        )
        if add_reel_like_serializer.is_valid():
            add_reel_like_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "like added on reel",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": add_reel_like_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RemoveReelLikeAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        reel_like = ReelLike.objects.select_related().filter(
            user=request.user, reel=id
        )
        if reel_like.exists():
            reel_like.first().delete()
            response = {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "like remove on reel",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        
        response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request !! you need to like first",
            }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
            

class AddReelCommentAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        add_reel_comment_serializer = AddReelCommentSerializer(data=request.data)
        if add_reel_comment_serializer.is_valid():
            try:
                reel = Reel.objects.get(
                    id=add_reel_comment_serializer.validated_data.get("reel_id")
                )
            except Reel.DoesNotExist:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "data": {"reel_id": ["reel_id is invalid"]},
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            add_reel_comment_serializer.save(user=request.user, reel=reel)
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "comment added on reel",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": add_reel_comment_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RemoveReelCommentAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        remove_reel_comment_serializer = RemoveReelCommentSerializer(
            data=request.data, context={"request": request}
        )
        if remove_reel_comment_serializer.is_valid():
            remove_reel_comment_serializer.delete()
            response = {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "comment remove from reel",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": remove_reel_comment_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class AddReelCommentLikeAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        add_reel_comment_like_serializer = AddReelCommentLikeSerializer(
            data=request.data, context={"request": request}
        )
        if add_reel_comment_like_serializer.is_valid():
            add_reel_comment_like_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "like added on reel comment",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": add_reel_comment_like_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RemoveReelCommentLikeAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        remove_reel_comment_like_serializer = AddReelCommentLikeSerializer(
            data=request.data, context={"request": request}
        )
        if remove_reel_comment_like_serializer.is_valid():
            remove_reel_comment_like_serializer.delete()
            response = {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "comment like remove from reel",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": remove_reel_comment_like_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserReelAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            reel = Reel.objects.get(id=id, user=request.user)
        except Reel.DoesNotExist:
            response = {
                "status_code" : status.HTTP_400_BAD_REQUEST,
                "message" : "bad request ! reel id is invalid or not associate with current user"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        reel.delete()

        response = {
            "status_code" : status.HTTP_204_NO_CONTENT,
            "message" : "reel deleted"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
