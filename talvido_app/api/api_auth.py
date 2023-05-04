from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import (
    TalvidoMobileRegisterSerializer,
    TalvidoMobileLoginSerializer,
    TavlidoGoogleLoginSerializer,
    TavlidoFacebokLoginSerializer,
    RegenerateAccessTokenSerializer,
    CheckMobileNumberExistSerializer,
    TalvidoEmailRegisterSerializer,
    TalvidoEmailLoginSerializer,
    ResetEmailPasswordSerializer,
)


class RegisterMobileOTPAPIView(APIView):
    """
    This API will register new user using mobile otp
    """

    def post(self, request):
        """Adding login_with field data"""
        request.data["login_with"] = "Mobile Number"

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


class LoginMobileOTPAPIView(APIView):
    """
    This API will handle login with mobile otp
    """

    def post(self, request):
        """serialize the data"""
        mobile_login_serializer = TalvidoMobileLoginSerializer(data=request.data)

        """validate the data"""
        if mobile_login_serializer.is_valid():
            """checking credentials"""
            if mobile_login_serializer.check_credentials(
                firebase_uid=mobile_login_serializer.validated_data.get("firebase_uid"),
                mobile_number=mobile_login_serializer.validated_data.get(
                    "mobile_number"
                ),
            ):
                response = {
                    "status_code": status.HTTP_200_OK,
                    "message": "success",
                }
                return Response(response, status=status.HTTP_200_OK)

            else:
                """return this if credentials failed"""
                response = {
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                    "message": "unauthorized",
                    "data": {
                        "mobile_number": [
                            "The mobile number you are trying with is not registered"
                        ]
                    },
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        """return this response if validation failed"""
        response = {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "message": "bad request",
            "data": mobile_login_serializer.errors,
        }
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class CheckMobileNumberExistAPIView(APIView):
    """
    This API will check mobile number exist in our database, 
    it return status 1 if it's exists other status 0
    """

    def post(self, request):
        """deserialize the data"""
        check_mobile_serializer = CheckMobileNumberExistSerializer(data=request.data)

        """validate the data"""
        if check_mobile_serializer.is_valid():
            response = {
                "status_code": status.HTTP_200_OK,
                "status": "1"
                if check_mobile_serializer.check_mobile_number_exists(
                    mobile_number=check_mobile_serializer.validated_data.get(
                        "mobile_number"
                    )
                )
                else "0",
            }
            return Response(response, status=status.HTTP_200_OK)

        """return this response if validation failed"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": check_mobile_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LoginGoogleAPIView(APIView):
    """
    This API will handle login with google
    """

    def post(self, request):
        """deserialize the data"""
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


class LoginFacebookAPIView(APIView):
    """
    This API will handle login with facebook
    """

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


class RegenerateAccessTokenAPIVIew(APIView):
    """
    This api will generate the access token on the base refresh token
    """

    def post(self, request):
        """deserialize the data"""
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


class RegsiterEmailAPIView(APIView):
    """
    This API will handle registration with email address and password
    """

    def post(self, request):
        """deserialize the request data"""
        email_regsiter_serializer = TalvidoEmailRegisterSerializer(data=request.data)

        """validate the data if validation success it will 
            call the save method and save the data"""
        if email_regsiter_serializer.is_valid():
            user = email_regsiter_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "created",
                "data": user,
            }
            return Response(response, status=status.HTTP_201_CREATED)

        """if validation fails it will response this"""
        response = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": email_regsiter_serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LoginEmailAPIView(APIView):
    """
    This API will handle login with email address and password
    """

    def post(self, request):
        """deserialize the request data"""
        email_login_serializer = TalvidoEmailLoginSerializer(data=request.data)

        """validate the data if validation success it will 
            check the credentails and return this response if crendentials is correct"""
        if email_login_serializer.is_valid():
            user = email_login_serializer.check_credentials()
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "ok",
                "data": user,
            }
            return Response(response, status=status.HTTP_200_OK)

        """if validation fails it will response this"""
        response = {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "message": "bad request",
            "data": email_login_serializer.errors,
        }
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class ResetEmailPasswordAPIView(APIView):
    """
    This API will send reset password link to registered email address
    """

    def post(self, request):
        """deserialize the data"""
        reset_email_password_serializer = ResetEmailPasswordSerializer(data=request.data)

        """validate the data"""
        if reset_email_password_serializer.is_valid():
            """
            this will send a reset password link to email address 
            if email address and requestType is correct and return the response
            """
            reset_email_password_serializer.send_reset_password_email()
            response = {
                "status_code" : status.HTTP_200_OK,
                "message" : "reset password email send"
            }
            return Response(response, status=status.HTTP_200_OK)
        
        """if validation fails it will return this response"""
        response = {
            "status_code" : status.HTTP_400_BAD_REQUEST,
            "message" : "bad request",
            "data" : reset_email_password_serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
