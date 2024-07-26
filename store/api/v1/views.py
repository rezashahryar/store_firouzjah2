from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from store import models

from . import serializers

# create your views here


class ProductListViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = models.Product.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        elif self.action == 'retrieve':
            return serializers.ProductDetailSerializer
        return serializers.ProductListSerializer
