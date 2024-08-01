from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from store import models as store_models

from . import serializers

# create your views here

class BaseProductCreateApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CreateBaseProductSerializer

    def get(self, request):
        return Response({
            "store_code": store_models.Store.objects.get(user_id=request.user.pk).code
        })


class ProductViewSet(ModelViewSet):
    queryset = store_models.Product.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST' and self.action == 'create':
            return serializers.CreateProductSerializer
        return serializers.CreateProductSerializer
    
    def get_serializer_context(self):
        return {
            'user_pk': self.request.user.pk,
        }
