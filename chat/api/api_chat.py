from rest_framework.response import Response
from rest_framework import status
from talvido_app.models import Talvidouser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication
from .chat_serializers import (
    GetChatModelSerializer,
    GetParticularUserChatModelSerializer,
)
from chat.models import Chat


class GetUserChatAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Talvidouser.objects.get(firebase_uid=request.user)
        user_chats = user.sender_chat.all().distinct("reciever")
        get_chats_serializer = GetChatModelSerializer(user_chats, many=True, context={"request": request})
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "data" : get_chats_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class GetParticularUserChatAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, firebase_uid):
        try:
            reciever_user = Talvidouser.objects.get(firebase_uid=firebase_uid)
        except Talvidouser.DoesNotExist:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "data" : {
                    "firebase_uid" : [
                        "firebase_uid is invalid"
                    ]
                }
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        users_chats = Chat.objects.select_related().filter(
            sender__in=[request.user, reciever_user],
            reciever__in=[reciever_user, request.user],
        )
        get_chats_serializer = GetParticularUserChatModelSerializer(users_chats, many=True, context={"request": request})
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "data" : get_chats_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)