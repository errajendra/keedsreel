from django.urls import path
from .api_payment import CreateOrderAPIView


urlpatterns = [
    path("create/order/", CreateOrderAPIView.as_view(), name="create-order-api")
]
