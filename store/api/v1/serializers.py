from rest_framework import serializers
from django.db import transaction

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
    product = serializers.PrimaryKeyRelatedField(
        queryset=models.Product.objects.select_related('base_product').select_related('size') \
            .select_related('color')
    )

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
    

class CartItemBaseProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductImage
        fields = ['image']


class CartItemBaseProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BaseProduct
        fields = ['title_farsi', 'images']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        image = models.ProductImage.objects.get(product_id=instance.pk, is_cover=True)
        rep['images'] = CartItemBaseProductImageSerializer(image).data

        return rep


class CartItemProductSerializer(serializers.ModelSerializer):
    base_product = CartItemBaseProductSerializer()

    class Meta:
        model = models.Product
        fields = ['id', 'base_product', 'slug', 'price', 'price_after_discount']

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
        # rep['base_product'] = CartItemBaseProductSerializer(instance.base_product).data

        # return rep


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
    amount_discount = serializers.SerializerMethodField()
    amount_payable = serializers.SerializerMethodField()

    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'total_price_of_cart', 'amount_discount', 'amount_payable']
        read_only_fields = ['id']

    def get_total_price_of_cart(self, cart):
        return sum(item.product.price * item.quantity for item in cart.items.all())
    
    def get_amount_discount(self, cart):
        amount_discount = 0
        for item in cart.items.all():
            if item.product.price_after_discount:
                amount_discount = sum(item.product.price_after_discount * item.quantity for item in cart.items.all())
        return amount_discount
    
    def get_amount_payable(self, cart):
        result = None
        for item in cart.items.all():
            if item.product.discount_percent:
                result = self.get_total_price_of_cart(cart) - sum(item.quantity * item.product.price_after_discount for item in cart.items.all())
                return result
            result = self.get_total_price_of_cart(cart) - sum(item.quantity * item.product.price for item in cart.items.all())
        return result
    

class OrderItemProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='base_product.title_farsi')

    class Meta:
        model = models.Product
        fields = ['id', 'title', 'price']
    

class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()

    class Meta:
        model = models.OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderCustomerSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(source='user.mobile')

    class Meta:
        model = models.Customer
        fields = ['mobile']
    

class OrderForAdminSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    status = serializers.CharField(source='get_status_display')
    customer = OrderCustomerSerializer()

    class Meta:
        model = models.Order
        fields = ['id', 'customer', 'status', 'datetime_created', 'items']


class OrderForUserSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = models.Order
        fields = ['id', 'status', 'datetime_created', 'items']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    receiver_full_name = serializers.CharField(max_length=255)
    receiver_mobile = serializers.IntegerField()
    province = serializers.IntegerField()
    city = serializers.IntegerField()
    neighbourhood = serializers.IntegerField()
    region = serializers.CharField()
    house_num = serializers.IntegerField()
    vahed = serializers.IntegerField()
    post_code = serializers.IntegerField()
    identification_code = serializers.IntegerField()

    def validate_cart_id(self, cart_id):
        print(cart_id)
        try:
            if models.Cart.objects.prefetch_related('items').get(id=cart_id).items.count() == 0:
                raise serializers.ValidationError('your cart is empty')
        except models.Cart.DoesNotExist:
            raise serializers.ValidationError('there is not cart with this cart id')

        # if not models.Cart.objects.filter(id=cart_id).exists():
        #     raise serializers.ValidationError('there is not cart with this cart id')
        
        # if models.CartItem.objects.filter(cart_id=cart_id).count() == 0:
        #     raise serializers.ValidationError('your cart is empty')
        
        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            data = self.validated_data

            cart_id = data['cart_id']
            user_id = self.context['user_id']

            customer = models.Customer.objects.get(user_id=user_id)

            order = models.Order(
                customer=customer,
                receiver_full_name=data['receiver_full_name'],
                receiver_mobile=data['receiver_mobile'],
                province_id=data['province'],
                city_id=data['city'],
                neighbourhood_id=data['neighbourhood'],
                region=data['region'],
                house_num=data['house_num'],
                vahed=data['vahed'],
                post_code=data['post_code'],
                identification_code=data['identification_code'],
            )
            order.save()

            cart_items = models.CartItem.objects.select_related('product').filter(cart_id=cart_id)

            order_items = [
                models.OrderItem(
                    order=order,
                    product_id=cart_item.product_id,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity
                ) for cart_item in cart_items
            ]

            # order_items = list()
            # for cart_item in cart_items:
            #     order_item = models.OrderItem()
            #     order_item.order = order
            #     order_item.product_id = cart_item.product_id
            #     order_item.price = cart_item.product.price
            #     order_item.quantity = cart_item.quantity
            #     order_items.append(order_item)

            models.OrderItem.objects.bulk_create(order_items)

            models.Cart.objects.get(id=cart_id).delete()

            return order
        

class HaghighyStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HaghighyStore
        fields = [
            'id', 'name', 'mobile_number', 'phone_number', 'email', 'code', 'shomare_shaba',
            'province', 'city', 'mantaghe', 'mahalle', 'parvane_kasb', 'tasvire_personely',
            'kart_melli', 'shenasname', 'logo', 'roozname_rasmi_alamat', 'gharardad', 'store_type',
            'full_name', 'birth_date', 'name_father', 'code_melli', 'shomare_shenasname',
        ]


class HoghoughyStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HoghoughyStore
        fields = [
            'id', 'name', 'mobile_number', 'phone_number', 'email', 'code', 'shomare_shaba',
            'province', 'city', 'mantaghe', 'mahalle', 'parvane_kasb', 'tasvire_personely',
            'kart_melli', 'shenasname', 'logo', 'roozname_rasmi_alamat', 'gharardad', 'store_type',
            'ceo_name', 'company_name', 'date_of_registration', 'economic_code',
        ]


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Store
        fields = [
            'id', 'name', 'mobile_number', 'phone_number', 'email', 'code', 'shomare_shaba',
            'province', 'city', 'mantaghe', 'mahalle', 'parvane_kasb', 'tasvire_personely',
            'kart_melli', 'shenasname', 'logo', 'roozname_rasmi_alamat', 'gharardad', 'store_type',
        ]
