from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from store import models as store_models

from panel import models

from . import serializers
from .permissions import HasStore

# create your views here


class ProfileApiView(generics.RetrieveUpdateAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return models.Profile.objects.get(user_id=user.pk)
    

class BaseProductCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.CreateBaseProductSerializer
    permission_classes = [IsAuthenticated, HasStore]

    def get_serializer_context(self):
        return {'store_id': self.request.user.store.pk}
    

class ProductViewSet(ModelViewSet):
    queryset = store_models.Product.objects.select_related('base_product').all()
    permission_classes = [IsAuthenticated, HasStore]

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = serializers.CreateProductSerializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateProductSerializer
        return serializers.ProductSerializer
