from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers.reels_serializer import GetReelModelSerializer, UploadUserReelsModelSerializer
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication
from talvido_app.models import Talvidouser
    

class GetUserReelsAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Talvidouser.objects.get(firebase_uid=request.user)
        user_reels = user.reel_user.all()
        reels_serializer = GetReelModelSerializer(user_reels, many=True, context={"request":request})
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "data" : reels_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class UploadUserReelsAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        upload_reels_serializer = UploadUserReelsModelSerializer(data=request.data)
        if upload_reels_serializer.is_valid():
            upload_reels_serializer.save(user=request.user)
            response = {
                "status_code" : status.HTTP_201_CREATED,
                "message" : "reel uploaded",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code" : status.HTTP_400_BAD_REQUEST,
            "message" : "bad request",
            "data" : upload_reels_serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
