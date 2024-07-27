from rest_framework import serializers
from django.contrib.auth import get_user_model

from store import models

# create your serializers here

class ProductSlugSerializer(serializers.Serializer):
    slug = serializers.Serializer()


class ColorSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    code_of_color = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ['color', 'code_of_color', 'slug']

    def get_color(self, product):
        global color
        color = models.Color.objects.get(pk=product['products__color'])
        return color.name
    
    def get_code_of_color(self, product):

        return color.code_of_color

    def get_slug(self, product):
        return product['products__slug']


class BaseProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = models.BaseProduct
        fields = ['id', 'category', 'title_farsi']


class ProductListSerializer(serializers.ModelSerializer):
    base_product = BaseProductListSerializer()
    
    class Meta:
        model = models.Product
        fields = ['id', 'base_product', 'slug', 'price', 'price_after_discount', 'end_discount', 'discount_percent']


class ProductPropertySerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField()

    class Meta:
        model = models.SetProductProperty
        fields = ['property', 'value']


class BaseProductDetailAnswerCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = models.ProductAnswerComment
        fields = ['id', 'comment', 'user', 'text', 'datetime_created']
        extra_kwargs = {
            'comment': {'write_only': True}
        }

    def create(self, validated_data):
        user_id = self.context['user_id']

        return models.ProductAnswerComment.objects.create(
            user_id=user_id,
            **validated_data
        )


class BaseProductDetailCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    answers = BaseProductDetailAnswerCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.ProductComment
        fields = ['id', 'user', 'product', 'text', 'datetime_created', 'answers']
        extra_kwargs = {
            'product': {'write_only': True}
        }

    def create(self, validated_data):
        user_id = self.context['user_id']

        return models.ProductComment.objects.create(
            user_id=user_id,
            **validated_data
        )


class BaseProductDetailSerializer(serializers.ModelSerializer):
    properties = ProductPropertySerializer(many=True)
    comments = BaseProductDetailCommentSerializer(many=True)
    
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()
    product_type = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    sending_method = serializers.CharField(source='get_sending_method_display')

    class Meta:
        model = models.BaseProduct
        fields = [
            'id', 'category', 'sub_category', 'product_type', 'product_code', 'brand',
            'title_farsi', 'title_english', 'description', 'product_authenticity', 'product_warranty',
            'sending_method', 'properties', 'comments'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    base_product = BaseProductDetailSerializer()

    size = serializers.StringRelatedField()
    color = serializers.StringRelatedField()
    unit = serializers.CharField(source='get_unit_display')

    class Meta:
        model = models.Product
        fields = [
            'id', 'base_product', 'size', 'color', 'unit', 'inventory', 'price', 'price_after_discount', 'discount_percent',
            'start_discount', 'end_discount', 'length_package', 'width_package', 'height_package', 'weight_package',
            'shenase_kala', 'barcode',
        ]


class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CartItem
        fields = ['quantity']


class AddCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        cart_pk = self.context['cart_pk']

        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        try:
            cart_item = models.CartItem.objects.get(cart_id=cart_pk, product_id=product.pk)
            cart_item.quantity += quantity
            cart_item.save()
        except models.CartItem.DoesNotExist:
            cart_item = models.CartItem.objects.create(cart_id=cart_pk,**validated_data)

        # if models.CartItem.objects.filter(cart_id=cart_pk, product_id=product.pk).exists():
        #     cart_item = models.CartItem.objects.get(cart_id=cart_pk, product_id=product.pk)
        #     cart_item.quantity += quantity
        #     cart_item.save()
        # else:
        #     cart_item = models.CartItem.objects.create(cart_id=cart_pk,**validated_data)
        
        self.instance = cart_item

        return cart_item


class CartItemBaseProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BaseProduct
        fields = ['title_farsi']


class CartItemProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ['id', 'base_product', 'price', 'price_after_discount']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['base_product'] = CartItemBaseProductSerializer(instance.base_product).data

        return rep


class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    total_price_item = serializers.SerializerMethodField()

    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity', 'total_price_item']

    def get_total_price_item(self, cart_item):
        return cart_item.quantity * cart_item.product.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price_of_cart = serializers.SerializerMethodField()

    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'total_price_of_cart']
        read_only_fields = ['id']

    def get_total_price_of_cart(self, cart):
        return sum(item.product.price * item.quantity for item in cart.items.all())
