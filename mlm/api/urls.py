from django.urls import path
from .import GetUserLevelAPIView


urlpatterns = [
    path("user/level/", GetUserLevelAPIView.as_view(), name="get-user-level-api"),
]
