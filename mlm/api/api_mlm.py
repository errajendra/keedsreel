from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from talvido_app.firebase.authentication import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated
from .helpers import UserLevel
from talvido_app.models import Talvidouser
from .mlm_serializers import WalletModelSerializer
from django.db.models import Sum


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
                    "message": "firebase_uid is invalid",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        level = UserLevel(user=user, request=request)
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": {
                "levels": level.create_level_info,
                "followers": level.get_followers,
                "current_level": level.get_current_level,
                "score": level.get_followers * 1,
                "full_name": user.first_name + " " + user.last_name,
                "description": user.profile.description,
            },
        }
        return Response(response, status=status.HTTP_200_OK)


class GetWalletAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Talvidouser.objects.get(firebase_uid=request.user)
        wallet_history = user.user_wallet_history.all()
        wallet_history_serializer = WalletModelSerializer(wallet_history, many=True)

        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": {
                "total_balance": wallet_history.aggregate(Sum("amount"))["amount__sum"],
                "wallet_history": wallet_history_serializer.data,
            },
        }
        return Response(response, status=status.HTTP_200_OK)
