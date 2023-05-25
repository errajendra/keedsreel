from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from talvido_app.firebase.authentication import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated
from .helpers import UserLevel
from talvido_app.models import Talvidouser


class GetUserLevelAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, firebase_uid=None):
        if firebase_uid is None:
            user = request.user 
        else:
            try:
                user = Talvidouser.objects.get(firebase_uid=firebase_uid)
            except Talvidouser.DoesNotExist:
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "firebase_uid is invalid"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
        level = UserLevel(user=user)
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data":{
                "level": level.get_user_level,
                "level_max_users": level.get_level_max_users,
                "total_referral_user": level.get_total_referral_users,
                "current_level_referral_user": level.get_current_level_referral_users,
                "full_name": user.first_name + " " + user.last_name,
                "description": user.profile.description,
                "followers": user.user_to.all().count(),
            }
        }
        return Response(response, status=status.HTTP_200_OK)


class GetWalletAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        level = UserLevel(user=request.user)
        get_user_level = level.level.get_user_level
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": {
                "total_balance": 100
            }
        }
        return Response(response, status=status.HTTP_200_OK)
