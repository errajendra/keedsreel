from django.urls import path
from .api_chat import (
    GetUserChatAPIView,
    GetParticularUserChatAPIView,
)


urlpatterns = [
    path("user/chats/", GetUserChatAPIView.as_view(), name="get-user-chats-api"),
    path("user/chats/<str:firebase_uid>/", GetParticularUserChatAPIView.as_view(), name="get-user-particular-chats-api"),
]
