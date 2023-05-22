from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from talvido_app.firebase.authentication import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated
from .helpers import UserLevel


class GetUserLevelAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        level = UserLevel(request=request)

        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data":{
                "level" : level.get_user_level() if level.get_user_level() else 1
            }
        }
        return Response(response, status=status.HTTP_200_OK)
