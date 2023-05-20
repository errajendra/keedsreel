from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .payment_serializers import CreateOrderSerializer, TransactionModelSerializer
from .main import razorpayClient
from talvido_app.firebase.authentication import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateOrderAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        create_order_serializer = CreateOrderSerializer(data=request.data)
        if create_order_serializer.is_valid():
            razorpay = razorpayClient()
            order_response = razorpay.create_order(
                amount=create_order_serializer.validated_data.get("amount"),
                currency=create_order_serializer.validated_data.get("currency"),
                receipt=create_order_serializer.validated_data.get("receipt")
            )
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "order created",
                "data": order_response
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": create_order_serializer.errors
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
            "data" : tranasaction_serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
