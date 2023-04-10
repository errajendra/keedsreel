from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    TalvidoMobileLoginSerializer,
    TavlidoGoogleLoginSerializer,
    TavlidoFacebokLoginSerializer
)


"""This API handle login with mobile otp"""

class LoginMobileOTPAPIView(APIView):
    
    def post(self,request):

        """serialize the data"""
        mobile_login_serializer = TalvidoMobileLoginSerializer(data=request.data)

        """validate the data"""
        if mobile_login_serializer.is_valid():
            mobile_login_serializer.save()
            response = {
                "status_code" : status.HTTP_200_OK,
                "message" : "success",
            }
            return Response(response,status=status.HTTP_200_OK)
        
        """return this response if validation failed"""
        response = {
            "status_code" : status.HTTP_400_BAD_REQUEST,
            "message" : "bad request",
            "data" : mobile_login_serializer.errors
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)


"""This API handle login with google"""

class LoginGoogleAPIView(APIView):

    def post(self,request):
        
        """serialize the data"""
        google_login_serializer = TavlidoGoogleLoginSerializer(data=request.data)

        """validate the data"""
        if google_login_serializer.is_valid():
            google_login_serializer.save()
            response = {
                "status_code" : status.HTTP_200_OK,
                "message" : "success",
            }
            return Response(response,status=status.HTTP_200_OK)
        
        """return this response if validation failed"""
        response = {
            "status_code" : status.HTTP_400_BAD_REQUEST,
            "message" : "bad request",
            "data" : google_login_serializer.errors
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)


"""This API handle login with facebook"""

class LoginFacebookAPIView(APIView):

    def post(self,request):
        
        """serialize the data"""
        facebook_login_serializer = TavlidoFacebokLoginSerializer(data=request.data)

        """validate the data"""
        if facebook_login_serializer.is_valid():
            facebook_login_serializer.save()
            response = {
                "status_code" : status.HTTP_200_OK,
                "message" : "success",
            }
            return Response(response,status=status.HTTP_200_OK)
        
        """return this response if validation failed"""
        response = {
            "status_code" : status.HTTP_400_BAD_REQUEST,
            "message" : "bad request",
            "data" : facebook_login_serializer.errors
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
