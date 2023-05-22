from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .payment_serializers import CreateOrderSerializer, TransactionModelSerializer
from .main import RazorpayClient
from talvido_app.firebase.authentication import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated
from payment.helpers import check_user_subscription


class CreateOrderAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        create_order_serializer = CreateOrderSerializer(data=request.data)
        if create_order_serializer.is_valid():
            razorpay = RazorpayClient()
            order_response = razorpay.create_order(
                amount=create_order_serializer.validated_data.get("amount"),
                currency=create_order_serializer.validated_data.get("currency"),
                receipt=create_order_serializer.validated_data.get("receipt"),
            )
            order_response["name"] = request.user.first_name + " " + request.user.last_name
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "order created",
                "data": order_response,
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": create_order_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TransactionAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tranasaction_serializer = TransactionModelSerializer(data=request.data)
        if tranasaction_serializer.is_valid():
            tranasaction_serializer.save(user=request.user)
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "created",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": tranasaction_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserSubscriptionAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        has_subscription, subscription = check_user_subscription(request)
        if has_subscription:
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "ok",
                "status": 1,
                "data": {
                    "status": 1,
                    "subscription_start": subscription.first().created_at,
                    "expire_on": subscription.first().subscription_end_date(),
                },
            }
            return Response(response, status=status.HTTP_200_OK)

        response = {
            "status_code": status.HTTP_200_OK,
            "message": "ok",
            "status": 0,
        }
        return Response(response, status=status.HTTP_200_OK)
