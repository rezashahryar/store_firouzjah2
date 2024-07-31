from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from store import models

from . import serializers

# create your views here


class ProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST' and self.action == 'create':
            return serializers.CreateProductSerializer
        return serializers.CreateProductSerializer
    
    def get_serializer_context(self):
        return {
            'user_pk': self.request.user.pk,
        }
