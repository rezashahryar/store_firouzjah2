from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from store import models

from . import serializers

# create your views here


class ProductListViewSet(mixins.ListModelMixin,
                        GenericViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer
