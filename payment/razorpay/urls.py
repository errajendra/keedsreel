from django.urls import path
from .api_payment import CreateOrderAPIView, TransactionAPIView


urlpatterns = [
    path("create/order/", CreateOrderAPIView.as_view(), name="create-order-api"),
    path("complete/order/", TransactionAPIView.as_view(), name="complete-order-api"),
]
