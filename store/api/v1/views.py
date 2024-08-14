from decimal import Decimal
from django.db.models import Prefetch
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from store import models

from . import serializers

# create your views here


class CategoryListApiView(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.CategoryProduct.objects.all().prefetch_related('sub_categories')


class ProductsOfCategoryListApiView(generics.ListAPIView):
    serializer_class = serializers.ProductsOfCategorySerializer

    def get_queryset(self):
        category_pk = self.kwargs['category_pk']
        queryset = models.Product.objects.select_related('base_product__category') \
            .filter(base_product__category_id=category_pk) \
                .defer(
                    'unit', 'base_product__brand', 'base_product__product_code', 'base_product__description',
                    'base_product__category__logo', 'base_product__sub_category', 'inventory',
                    'length_package', 'width_package', 'height_package', 'weight_package', 'base_product__store',
                    'size', 'color', 'start_discount', 'shenase_kala', 'barcode', 'product_status', 'product_is_active',
                    'base_product__product_type', 'base_product__title_english', 'base_product__product_authenticity',
                    'base_product__product_warranty', 'base_product__sending_method', 'base_product__category__slug'
                )
        return queryset


class ProductViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['base_product__category_id', 'base_product__brand']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        colors = models.Color.objects.filter(products__base_product=instance.base_product).values('products__slug', 'products__color')
        return Response({
            'lowest_price_on_the_size': "salam",
            'product_colors': serializers.ColorSerializer(colors, many=True, context={'instance_pk': instance.pk}).data,
            'product': serializer.data,
        })

    def get_queryset(self):
        if self.action == 'list':
            products_queryset = models.Product.objects.select_related('base_product') \
                .select_related('base_product__category') \
                    .all().defer(
                        'unit', 'base_product__brand', 'base_product__product_code', 'base_product__description',
                        'base_product__category__logo', 'base_product__sub_category', 'inventory',
                        'length_package', 'width_package', 'height_package', 'weight_package', 'base_product__store',
                        'size', 'color', 'start_discount', 'shenase_kala', 'barcode', 'product_status', 'product_is_active',
                        'base_product__product_type', 'base_product__title_english', 'base_product__product_authenticity',
                        'base_product__product_warranty', 'base_product__sending_method', 'base_product__category__slug'
                    )
            return products_queryset
        elif self.action == 'retrieve':
            product_queryset = models.Product.objects.select_related('base_product') \
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
                        )).select_related('base_product__store__province').all()
            return product_queryset

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
    

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        create_order_serializer = serializers.CreateOrderSerializer(data=request.data,
                                                                    context={'user_id': request.user.pk}
                                                                )
        create_order_serializer.is_valid(raise_exception=True)
        created_order = create_order_serializer.save()
        serializer = serializers.OrderForUserSerializer(created_order)
        return Response(serializer.data)


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrderSerializer
        if self.request.user.is_staff:
            return serializers.OrderForAdminSerializer
        return serializers.OrderForUserSerializer

    def get_queryset(self):
        queryset = models.Order.objects.select_related('customer__user').prefetch_related(Prefetch(
            'items',
            queryset=models.OrderItem.objects.select_related('product__base_product')
        )).all()

        user = self.request.user

        if user.is_staff:
            return queryset
        
        return queryset.filter(customer__user_id=user.pk)
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.pk}
    

class CreateStoreApiView(generics.CreateAPIView):

    def get_serializer_class(self):
        if self.request.data['store_type'] == 'ha':
            return serializers.HaghighyStoreSerializer
        elif self.request.data['store_type'] == 'ho':
            return serializers.HoghoughyStoreSerializer
        return serializers.StoreSerializer
    

class OrderDateListApiView(generics.ListAPIView):
    queryset = models.OrderDate.active.all()
    serializer_class = serializers.OrderDateSerializer


class OrderTimeListApiView(generics.ListAPIView):
    queryset = models.OrderTime.active.all()
    serializer_class = serializers.OrderTimeSerializer


class SendRequestPhotographyApiView(generics.CreateAPIView):
    serializer_class = serializers.RequestPhotographySerializer


class ListSameProductApiView(generics.ListAPIView):
    serializer_class = serializers.SameProductsListSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        base_product_obj = models.BaseProduct.objects.get(pk=pk)
        return models.SameProduct.objects.select_related('product__base_product').filter(
            product__base_product__category=base_product_obj.category,
            product__base_product__sub_category=base_product_obj.sub_category,
            product__base_product__brand=base_product_obj.brand,
            product__base_product__product_type_id=base_product_obj.product_type.id
        ).exclude(store_id=base_product_obj.store.pk)


class SendReportProduct(generics.CreateAPIView):
    serializer_class = serializers.ReportproductSerializer


class ContactUsApiView(generics.CreateAPIView):
    serializer_class = serializers.ContactUsSerializer


class ApplyCouponDiscount(generics.GenericAPIView):
    serializer_class = serializers.CouponDiscountSerializer

    def post(self, request):
        serializer = serializers.CouponDiscountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_id = serializer.validated_data['cart_id']
        coupon_code = serializer.validated_data['code']

        cart_obj = models.Cart.objects.get(id=cart_id)
        coupon_obj = models.CouponDiscount.objects.get(code=coupon_code)

        amount_payable = cart_obj.get_amount_payable()
        amount_discount = coupon_obj.discount_percent / Decimal(100) * amount_payable

        cart_obj.amount_discount = amount_discount
        cart_obj.coupon_discount_percent = coupon_obj.discount_percent
        cart_obj.coupon_discount = True
        cart_obj.save()

        return Response(status=status.HTTP_200_OK)
    

class ProvinceListApiView(generics.ListAPIView):
    queryset = models.Province.objects.all()
    serializer_class = serializers.ProvinceSerializer


class CityListApiView(generics.ListAPIView):
    serializer_class = serializers.CitySerializer

    def get_queryset(self):
        province_pk = self.kwargs['province_pk']
        return models.City.objects.filter(province_id=province_pk)
    

class NeighbourhoodListApiView(generics.ListAPIView):
    serializer_class = serializers.neighbourhoodSerializer

    def get_queryset(self):
        city_pk = self.kwargs['city_pk']
        return models.Neighbourhood.objects.filter(city_id=city_pk)
