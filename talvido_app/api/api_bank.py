from rest_framework.response import Response
from rest_framework import status
from .import BankDetailsModelSerializer, BankPaymentModelSerializer, CompanyPaymentInfoModelSerializer, UPIPaymentModelSerializer
from rest_framework.views import APIView
from talvido_app.models import BankDetail, CompanyPaymentInfo, BankPayment, UPIPayment
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication


class BankDetailsAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bank_detail = BankDetail.objects.order_by('-id').all()[:2]
        bank_detail_serializer = BankDetailsModelSerializer(bank_detail, many=True)
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "data" : {
                "bank_detail": bank_detail_serializer.data
            }
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


class BankPaymentAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        upload_bank_payment_serializer = BankPaymentModelSerializer(data=request.data)
        if upload_bank_payment_serializer.is_valid():
            upload_bank_payment_serializer.save(user=request.user)
            response = {
                "status_code" : status.HTTP_201_CREATED,
                "message": "created",
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        response = {
            "status_code" : status.HTTP_400_BAD_REQUEST,
            "message" : "bad request",
            "data" : upload_bank_payment_serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CompanyPaymentInfoAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company_payment_info = CompanyPaymentInfo.objects.all().order_by("-created_at")[0]
        company_payment_info_serializer = CompanyPaymentInfoModelSerializer(company_payment_info, context={"request": request})
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "data" : company_payment_info_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class UPIPaymentAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        upload_upi_payment_serializer = UPIPaymentModelSerializer(data=request.data)
        if upload_upi_payment_serializer.is_valid():
            upload_upi_payment_serializer.save(user=request.user)
            response = {
                "status_code" : status.HTTP_201_CREATED,
                "message": "created",
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        response = {
            "status_code" : status.HTTP_400_BAD_REQUEST,
            "message" : "bad request",
            "data" : upload_upi_payment_serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserSubscriptionAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "status" : (
                1 
                if 
                BankPayment.objects.filter(user=request.user).order_by("-created_at").first().approve 
                or 
                UPIPayment.objects.filter(user=request.user).order_by("-created_at").first().approve
                else
                0
            )
        }
        return Response(response, status=status.HTTP_200_OK)
            