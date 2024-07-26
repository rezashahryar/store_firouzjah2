from django.db.models import Prefetch
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from store import models

from . import serializers

# create your views here


class ProductListViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    lookup_field = 'slug'

    def get_queryset(self):
        if self.action == 'list':
            return models.Product.objects.select_related('base_product') \
                .select_related('base_product__category').select_related('base_product__sub_category').all()
        elif self.action == 'retrieve':
            return models.Product.objects.select_related('base_product') \
                .select_related('base_product__category').select_related('base_product__sub_category') \
                    .select_related('base_product__product_type').select_related('base_product__brand') \
                        .select_related('size').select_related('color').prefetch_related(Prefetch(
                            'base_product__properties',
                            queryset=models.SetProductProperty.objects.select_related('property')
                        )).all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        elif self.action == 'retrieve':
            return serializers.ProductDetailSerializer
        return serializers.ProductListSerializer
