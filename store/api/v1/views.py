from django.db.models import Prefetch
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from store import models

from . import serializers

# create your views here


class ProductListViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        colors = models.Color.objects.filter(products__base_product=instance.base_product).values('products__slug', 'products__color')
        return Response({
            'product_colors': serializers.ColorSerializer(colors, many=True, context={'instance_pk': instance.pk}).data,
            'product': serializer.data,
        })

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
                        )).prefetch_related(Prefetch(
                            'base_product__comments',
                            queryset=models.ProductComment.objects.select_related('user') \
                                .prefetch_related(Prefetch(
                                    'answers',
                                    queryset=models.ProductAnswerComment.objects.select_related('user')
                                ))
                        )).all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        elif self.action == 'retrieve':
            return serializers.ProductDetailSerializer
        return serializers.ProductListSerializer
    

class CreateProductCommentApiView(generics.CreateAPIView):
    queryset = models.ProductComment.objects.all()
    serializer_class = serializers.BaseProductDetailCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.pk}
    

class CreateProductAnswerCommentApiView(generics.CreateAPIView):
    queryset = models.ProductAnswerComment.objects.all()
    serializer_class = serializers.BaseProductDetailAnswerCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.pk}
