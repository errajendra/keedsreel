from rest_framework import status
from rest_framework.response import Response
from talvido_app.models import Talvidouser
from talvido_app.api.serializers.search_serializers import SearchByUsernameModelSerializer
from rest_framework.views import APIView


class SearchByUsernameAPIView(APIView):
    def get(self, request):
        search_username = request.query_params.get("username")
        user = Talvidouser.objects.filter(username__icontains=search_username)
        user_serializer = SearchByUsernameModelSerializer(user, many=True, context={"request":request})
        response = {
            "status_code" : status.HTTP_200_OK,
            "message" : "ok",
            "data" : user_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
