from rest_framework.response import Response
from rest_framework import status
from .import BankDetailsModelSerializer
from rest_framework.views import APIView
from talvido_app.models import BankDetail, Talvidouser
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication


class BankDetailsAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bank_detail = BankDetail.objects.get(user=request.user)
        bank_detail_serializer = BankDetailsModelSerializer(bank_detail)
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "data" : bank_detail_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request):
        update_bank_detail_serializer = BankDetailsModelSerializer(
            request.user, data=request.data, partial=False
        )
        if update_bank_detail_serializer.is_valid():
            bank_detail = update_bank_detail_serializer.save()
            response = {
                "status_code" : status.HTTP_201_CREATED,
                "message" : "bank details updated",
                "data" :  BankDetailsModelSerializer(bank_detail).data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        response = {
                "status_code" : status.HTTP_400_BAD_REQUEST,
                "message" : "bad request",
                "data" :  update_bank_detail_serializer.errors
            }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
