from django.urls import path
from .import (
    GetUserLevelAPIView,
    GetWalletAPIView,
)


urlpatterns = [
    path("user/level/", GetUserLevelAPIView.as_view(), name="get-user-level-api"),
    path("user/level/<str:firebase_uid>/", GetUserLevelAPIView.as_view(), name="get-any-user-level-api"),
    path("user/wallet/", GetWalletAPIView.as_view(), name="user-wallet-api"),
]
