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
        user_notifications = user.notification_user_to.all().order_by("-created_at")
        user_notification_serializer = NotificationModelSerializer(
            user_notifications, many=True, context={"request": request}
        )
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "data": {
                "notifications": user_notification_serializer.data,
                "unseen_notification": user_notifications.filter(seen=False).count()
            }
        }
        return Response(response, status=status.HTTP_200_OK)


class SeenNotificationAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = Talvidouser.objects.get(firebase_uid=request.user)
        user_unseen_notification = user.notification_user_to.all().filter(seen=False)
        user_unseen_notification.update(seen = True)
        response = {
            "status": status.HTTP_201_CREATED,
            "message": "created"
        }
        return Response(response, status=status.HTTP_201_CREATED)
