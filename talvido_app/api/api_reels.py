from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers.reels_serializer import GetReelModelSerializer
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
