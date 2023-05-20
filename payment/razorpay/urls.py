from django.urls import path
from .api_payment import CreateOrderAPIView, TransactionAPIView, UserSubscriptionAPIView


urlpatterns = [
    path("create/order/", CreateOrderAPIView.as_view(), name="create-order-api"),
    path("complete/order/", TransactionAPIView.as_view(), name="complete-order-api"),
    path(
        "user/subscription/",
        UserSubscriptionAPIView.as_view(),
        name="user-subscription-api",
    ),
]
