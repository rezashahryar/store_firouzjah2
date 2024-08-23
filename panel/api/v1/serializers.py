from rest_framework import serializers
from django.contrib.auth import get_user_model

from panel import models
from store import models as store_models

# create your serializers here


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Profile
        fields = ['full_name', 'email', 'mobile']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = store_models.CategoryProduct
        fields = ['name']


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = store_models.CategoryProduct
        fields = ['name']


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = store_models.ProductType
        fields = ['name']


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = store_models.Brand
        fields = ['name']


class CreateBaseProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = store_models.BaseProduct
        fields = [
            'id', 'category', 'sub_category', 'product_type', 'brand', 'model',
            'title_farsi', 'title_english', 'product_authenticity', 'product_warranty', 'sending_method'
        ]

    def create(self, validated_data):
        return store_models.BaseProduct.objects.create(
            store_id=self.context['store_id'],
            **validated_data
        )

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['category'] = CategorySerializer(instance.category).data
    #     rep['sub_category'] = SubCategorySerializer(instance.sub_category).data
    #     rep['product_type'] = ProductTypeSerializer(instance.product_type).data
    #     rep['brand'] = BrandSerializer(instance.brand).data

    #     return rep
    
    # def get_sending_method(self, base_product):
    #     return base_product.get_sending_method_display()
    
    # # def get_product_authenticity(self, base_product):
    # #     return base_product.get_product_authenticity_display


class CreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = store_models.Product
        fields = [
            'size', 'color', 'inventory', 'unit', 'price', 'price_after_discount', 'discount_percent',
            'start_discount', 'end_discount', 'length_package', 'width_package', 'height_package', 'weight_package',
            'shenase_kala', 'barcode'
        ]

    def validate(self, attrs):
        base_product_id = self.context['base_product_id']
        try:
            base_product_obj = store_models.BaseProduct.objects.get(pk=base_product_id)
            if base_product_obj:
                ...
        except store_models.BaseProduct.DoesNotExist:
            raise serializers.ValidationError('please enter a valid base product id, base product obj with this id does not exist')

        return attrs

    def create(self, validated_data):
        return store_models.Product.objects.create(
            base_product_id=self.context['base_product_id'],
            **validated_data
        )


class BaseProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = store_models.BaseProduct
        fields = [
            'id', 'title_farsi'
        ]


class ProductSerializer(serializers.ModelSerializer):
    base_product = BaseProductSerializer()

    class Meta:
        model = store_models.Product
        fields = [
            'id', 'base_product', 'size', 'color'
        ]


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = store_models.ProductImage
        fields = [
            'id', 'product', 'image', 'is_cover'
        ]


class SendingMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SendingMethod
        fields = ['id', 'name']


class OriginSerializer(serializers.ModelSerializer):

    class Meta:
        model = store_models.Province
        fields = ['id', 'name']


class DestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = store_models.Province
        fields = ['id', 'name']


class ShipingCostSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ShipingCost
        fields = [
            'id', 'sending_method', 'origin', 'destination', 'cost'
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['sending_method'] = SendingMethodSerializer(instance.sending_method).data
        rep['origin'] = OriginSerializer(instance.origin).data
        rep['destination'] = DestinationSerializer(instance.destination).data

        return rep
    

# class ProductInfoInPanelSerializer(serializers.Serializer):
#     count_all_products = serializers.SerializerMethodField()
#     count_approved_products = serializers.SerializerMethodField()

#     def get_count_all_products(self, product):
#         return store_models.Product.objects.all().count()
    
#     def get_count_approved_products(self, product):
#         return store_models.Product.objects.filter(product_status=store_models.Product.ProductStatus.CONFIRM).count()


class ListOrderSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.user')

    class Meta:
        model = store_models.Order
        fields = [
            'id', 'customer', 'tracking_code', 'total_price', 'datetime_created'
        ]


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = store_models.OrderItem
        fields = ['product', 'quantity', 'purchased_price']


class DetailOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    date = serializers.StringRelatedField()
    time = serializers.StringRelatedField()
    province = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    neighbourhood = serializers.StringRelatedField()
    order_status = serializers.CharField(source='get_order_status_display')

    class Meta:
        model = store_models.Order
        fields = [
            'id', 'date', 'time', 'receiver_full_name', 'receiver_mobile', 'province', 'city', 'neighbourhood',
            'region', 'house_num', 'vahed', 'post_code', 'identification_code', 'discount_percent', 'total_price', 'tracking_code',
            'datetime_created', 'order_status', 'status_paid', 'items'
        ]


class FavoriteDetailProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='base_product.title_farsi')
    category = serializers.CharField(source='base_product.category')


    class Meta:
        model = store_models.Product
        fields = [
            'id', 'category', 'title', 'price', 'price_after_discount', 'discount_percent'
        ]


class FavoriteProductSerializer(serializers.ModelSerializer):
    product = FavoriteDetailProductSerializer()

    class Meta:
        model = store_models.FavoriteProduct
        fields = [
            'id', 'product'
        ]


class LetMeKnowDetailProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='base_product.title_farsi')
    category = serializers.CharField(source='base_product.category')


    class Meta:
        model = store_models.Product
        fields = [
            'id', 'category', 'title', 'price', 'price_after_discount', 'discount_percent'
        ]


class LetMeKnowProductSerializer(serializers.ModelSerializer):
    product = LetMeKnowDetailProductSerializer()

    class Meta:
        model = store_models.FavoriteProduct
        fields = [
            'id', 'product'
        ]


class ReviewerSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['mobile']


class AnswerSupprtTicketSerializer(serializers.ModelSerializer):
    # reviewer = serializers.CharField(source='reviewer.user')

    class Meta:
        model = models.AnswerSupportTicket
        fields = ['id', 'reviewer', 'text', 'annex']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['reviewer'] = ReviewerSerializer(instance.reviewer).data

        return rep

    def create(self, validated_data):
        return models.AnswerSupportTicket.objects.create(
            reviewer_id=self.context['user_id'],
            ticket_id=self.context['ticket_id'],
            **validated_data
        )


class SupportTicketSerializer(serializers.ModelSerializer):
    answers = AnswerSupprtTicketSerializer(many=True)

    class Meta:
        model = models.SupportTicket
        fields = ['id', 'subject', 'text', 'annex', 'answers']

    def create(self, validated_data):
        user_id = self.context['user_id']
        return models.SupportTicket.objects.create(
            user_id=user_id,
            **validated_data
        )
    

class RequestPhotographySerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    neighbourhood = serializers.StringRelatedField()

    class Meta:
        model = store_models.RequestPhotography
        fields = [
            'id', 'full_name', 'mobile', 'province', 'city', 'neighbourhood',
            'mahalle', 'address', 'store_name', 'request_text'
        ]
