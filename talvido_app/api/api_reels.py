from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers.reels_serializer import (
    GetReelModelSerializer,
    UploadUserReelsModelSerializer,
)
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication
from talvido_app.models import Talvidouser, Reel


"""This API will get the user all and particular reels"""

class GetUserReelsAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id is None:
            user = Talvidouser.objects.get(firebase_uid=request.user)
            user_reels = user.reel_user.all()
            reels_serializer = GetReelModelSerializer(
                user_reels, many=True, context={"request": request}
            )
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "ok",
                "data": reels_serializer.data,
            }
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
