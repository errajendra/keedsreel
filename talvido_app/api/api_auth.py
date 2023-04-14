from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    TalvidoMobileRegisterSerializer,
    TalvidoMobileLoginSerializer,
    TavlidoGoogleLoginSerializer,
    TavlidoFacebokLoginSerializer,
    RegenerateAccessTokenSerializer,
)


"""This API handle registration with mobile otp"""

class RegisterMobileOTPAPIView(APIView):
    def post(self, request):
        """Adding login_with field"""
        request.data['login_with'] = 'Mobile Number'

        """serialize the data"""
        mobile_register_serializer = TalvidoMobileRegisterSerializer(data=request.data)

        """validate the data"""
        if mobile_register_serializer.is_valid():
            mobile_register_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "created",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        """return this response if validation failed"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": mobile_register_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API handle login with mobile otp"""

class LoginMobileOTPAPIView(APIView):
    def post(self, request):
        """serialize the data"""
        mobile_login_serializer = TalvidoMobileLoginSerializer(data=request.data)

        """validate the data"""
        if mobile_login_serializer.is_valid():
            mobile_login_serializer.save()
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "success",
            }
            return Response(response, status=status.HTTP_200_OK)

        """return this response if validation failed"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": mobile_login_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API handle login with google"""

class LoginGoogleAPIView(APIView):
    def post(self, request):
        """serialize the data"""
        google_login_serializer = TavlidoGoogleLoginSerializer(data=request.data)

        """validate the data"""
        if google_login_serializer.is_valid():
            google_login_serializer.save()
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "success",
            }
            return Response(response, status=status.HTTP_200_OK)

        """return this response if validation failed"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": google_login_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This API handle login with facebook"""

class LoginFacebookAPIView(APIView):
    def post(self, request):
        """serialize the data"""
        facebook_login_serializer = TavlidoFacebokLoginSerializer(data=request.data)

        """validate the data"""
        if facebook_login_serializer.is_valid():
            facebook_login_serializer.save()
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "success",
            }
            return Response(response, status=status.HTTP_200_OK)

        """return this response if validation failed"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": facebook_login_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


"""This api generate the access token using refresh token"""

class RegenerateAccessTokenAPIVIew(APIView):
    def post(self, request):
        """serialize the data"""
        regenerate_access_token_serialzier = RegenerateAccessTokenSerializer(
            data=request.data
        )

        """validate the data"""
        if regenerate_access_token_serialzier.is_valid():
            """generate the new token on the base of refresh token"""
            token_data = regenerate_access_token_serialzier.get_access_token(
                grant_type=regenerate_access_token_serialzier.validated_data.get(
                    "grant_type"
                ),
                refresh_token=regenerate_access_token_serialzier.validated_data.get(
                    "refresh_token"
                ),
            )
            return Response(token_data.json(), status=token_data.status_code)

        """return this response if validation failed"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": regenerate_access_token_serialzier.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
