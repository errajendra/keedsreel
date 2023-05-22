from django.urls import path
from .import GetUserLevelAPIView


urlpatterns = [
    path("user/level/", GetUserLevelAPIView.as_view(), name="get-user-level-api"),
    path("user/level/<str:firebase_uid>/", GetUserLevelAPIView.as_view(), name="get-any-user-level-api"),
]
