from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend

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
    queryset = store_models.Product.objects.select_related('base_product__store').all()
    permission_classes = [IsAuthenticated, HasStore]
    filter_backends = [OrderingFilter]
    ordering_fields = ['datetime_created']

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        create_product_serializer = serializers.CreateProductSerializer(
            data=request.data,
            many=many,
            context={
                'base_product_id': request.data['base_product_id']
            }
        )
        create_product_serializer.is_valid(raise_exception=True)
        product_obj = create_product_serializer.save()

        models.RequestAddProduct.objects.create(
            user=request.user,
            product=product_obj,
        )
        serializer = serializers.CreateProductSerializer(product_obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateProductSerializer
        return serializers.ProductSerializer
    

class ProductImageViewSet(ModelViewSet):
    queryset = store_models.ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer
    permission_classes = [IsAuthenticated, HasStore]


class ShipingCostViewSet(ModelViewSet):
    queryset = models.ShipingCost.objects.all()
    serializer_class = serializers.ShipingCostSerializer
    permission_classes = [IsAuthenticated, HasStore]


class ProductsIngoDisplay(APIView):

    def get(self, request):
        return Response(
            {
                'count_all_products': store_models.Product.objects.all().count(),
                'count_approved_products': store_models.Product.objects.filter(product_status=store_models.Product.ProductStatus.CONFIRM).count(),
                'count_waiting_products': store_models.Product.objects.filter(product_status=store_models.Product.ProductStatus.WAITING).count(),
                'count_not_approved_products': store_models.Product.objects.filter(product_status=store_models.Product.ProductStatus.NOT_CONFIRMED).count(),
                'count_active_products': store_models.Product.objects.filter(product_is_active=True).count(),
                'count_inactive_products': store_models.Product.objects.filter(product_is_active=False).count(),
            },
            status=status.HTTP_200_OK,
        )
    

class ActivateAllProducts(APIView):
    permission_classes = [IsAuthenticated, HasStore]

    def post(self, request):
        if not request.data:
            queryset = store_models.Product.objects.all()
        else:
            queryset = store_models.Product.objects.filter(id__in=request.data['id'])

        for product in queryset:
            product.product_is_active = True
            product.save()
        
        return Response(status=status.HTTP_200_OK)
    

class DeActivateAllProducts(APIView):
    permission_classes = [IsAuthenticated, HasStore]

    def post(self, request):
        if not request.data:
            queryset = store_models.Product.objects.all()
        else:
            queryset = store_models.Product.objects.filter(id__in=request.data['id'])

        for product in queryset:
            product.product_is_active = False
            product.save()
        
        return Response(status=status.HTTP_200_OK)


class OrderInfoDisplay(APIView):
    
    def get(self, request):
        return Response(
            {
                'count_all_orders': store_models.Order.objects.all().count(),
                'count_current_orders': store_models.Order.objects.filter(order_status=store_models.Order.OrderStatus.CURRENT_ORDERS).count(),
                'count_delivered_orders': store_models.Order.objects.filter(order_status=store_models.Order.OrderStatus.ORDERS_DELIVERED).count(),
                'count_return_orders': store_models.Order.objects.filter(order_status=store_models.Order.OrderStatus.RETURN_ORDERS).count(),
                'count_canceled_orders': store_models.Order.objects.filter(order_status=store_models.Order.OrderStatus.CANCELED).count(),
            }
        )
    

class OrderViewSet(ModelViewSet):
    serializer_class = serializers.ListOrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['order_status']
    search_fields = [
        'tracking_code', 'items__product__base_product__product_code', 'items__product__base_product__store__code',
        'customer__user__mobile'
    ]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = store_models.Order.objects.select_related('customer__user').all()
        try:
            store = store_models.Store.objects.get(user_id=self.request.user.pk)
            if store:
                return queryset.prefetch_related('items').filter(items__product__base_product__store_id=store.pk)
        except store_models.Store.DoesNotExist:
            return queryset.filter(customer__user_id=self.request.user.pk)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.DetailOrderSerializer
        return serializers.ListOrderSerializer
    

class FavoriteProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.FavoriteProductSerializer

    def get_queryset(self):
        user = self.request.user

        return store_models.FavoriteProduct.objects.select_related('product__base_product__category') \
            .filter(user_id=user.pk)
    

class LetMeKnowProductViewSet(ModelViewSet):
    serializer_class = serializers.LetMeKnowProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return store_models.LetMeKnowProduct.objects.select_related('product__base_product__category') \
            .filter(user_id=user.pk)
    

class SupportTicketViewSet(ModelViewSet):
    serializer_class = serializers.SupportTicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # print(self.request.user.is_authenticated)
        return models.SupportTicket.objects.filter(user_id=self.request.user.pk)
    
    def get_serializer_context(self):
        return {
            'user_id': self.request.user.pk,
        }
    

class AnswerSupportTicketViewSet(ModelViewSet):
    serializer_class = serializers.AnswerSupprtTicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ticket_id = self.request.data['ticket_id']
        return models.AnswerSupportTicket.objects.filter(ticket_id=ticket_id)
    
    def get_serializer_context(self):
        return {
            'user_id': self.request.user.pk,
            'ticket_id': self.request.data['ticket_id']
        }
    

class RequestPhotographyViewSet(mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.ListModelMixin,
                                GenericViewSet):
    queryset = store_models.RequestPhotography.objects.select_related('province') \
        .select_related('city').select_related('neighbourhood').all()
    serializer_class = serializers.RequestPhotographySerializer
