from django.urls import path
from .api_chat import (
    GetUserChatAPIView
)


urlpatterns = [
    path("user/chats/", GetUserChatAPIView.as_view(), name="get-user-chats-api")
]
