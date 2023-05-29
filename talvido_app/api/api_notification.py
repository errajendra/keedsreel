from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .import NotificationModelSerializer
from talvido_app.models import Talvidouser
from talvido_app.firebase.authentication import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated


class NotificationAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = Talvidouser.objects.get(firebase_uid=request.user)
        user_notifications = user.notification_user_to.all()
        user_notification_serializer = NotificationModelSerializer(
            user_notifications, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": user_notification_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
