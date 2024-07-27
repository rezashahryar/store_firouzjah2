from django.db.models import Prefetch
from rest_framework.viewsets import GenericViewSet, ModelViewSet
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
    

class CartViewSet(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    serializer_class = serializers.CartSerializer
    queryset = models.Cart.objects.prefetch_related(Prefetch(
        'items',
        queryset=models.CartItem.objects.select_related('product__base_product') \
            .prefetch_related('product__base_product__images')
    ))


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_context(self):
        return {'cart_pk': self.kwargs['cart_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return serializers.UpdateCartItemSerializer
        return serializers.CartItemSerializer
    
    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return models.CartItem.objects.filter(cart_id=cart_pk).select_related('product') \
            .select_related('product__base_product').prefetch_related('product__base_product__images').all()
    
    
    
    
    # .select_related('product__base_product').select_related('product__size') \
    #         .prefetch_related('product__base_product__images').all()
