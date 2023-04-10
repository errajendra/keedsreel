from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TalvidoMobileLoginSerializer


"""This API handle login with mobile otp"""

class LoginMobileOTPAPIView(APIView):
    """Handle post request"""
    
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
