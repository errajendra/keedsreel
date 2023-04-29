from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers.reels_serializer import ReelSerializer, Reel, ReelDetailSerializer
from rest_framework.permissions import IsAuthenticated
from talvido_app.firebase.authentication import FirebaseAuthentication



""" API View for Reels. """
class ReelViewset(viewsets.ModelViewSet):
    serializer_class = ReelSerializer
    # authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Reel.objects.all()

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs)
        return Response(
            data={
                "status_code": status.HTTP_200_OK,
                "message": "success",
                "data": data.data
            },
            status=status.HTTP_200_OK
        )
        
    
    def create(self, request, *args, **kwargs):
        try:
            request.data._mutable = True
            request.data['user'] = request.user.pk
        except:
            request.data['user'] = request.user.pk
        data = super().create(request, *args, **kwargs)
        response = {
            'status': data.status_code,
            'message': data.status_text,
            'data': data.data
        }
        return Response(response, status=data.status_code)
    
    
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ReelDetailSerializer
        data = super().retrieve(request, *args, **kwargs)
        response = {
            'status': data.status_code,
            'message': data.status_text,
            'data': data.data
        }
        return Response(response, status=data.status_code)
    
    
    def update(self, request, *args, **kwargs):
        self.queryset = Reel.objects.filter(user=request.user)
        try:
            request.data._mutable = True
            request.data['user'] = request.user.id
        except:
            request.data['user'] = request.user.id
        data = super().update(request, *args, **kwargs)
        response = {
            'status': data.status_code,
            'message': data.status_text,
            'data': data.data
        }
        return Response(response, status=data.status_code)
    
    
    def destroy(self, request, *args, **kwargs):
        self.queryset = Reel.objects.filter(user=request.user)
        data = super().destroy(request, *args, **kwargs)
        response = {
            'status': data.status_code,
            'message': data.status_text,
            'data': data.data
        }
        return Response(response, status=data.status_code)
    

