from decimal import Decimal
from rest_framework import serializers
from django.db import transaction
from django.utils import timezone

from store import models

# create your serializers here


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SubCategoryProduct
        fields = ['id', 'name', 'slug', 'logo']


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = models.CategoryProduct
        fields = ['id', 'name', 'slug', 'logo', 'sub_categories']


class BaseProductOfCategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = models.BaseProduct
        fields = [
            'id', 'title_farsi', 'category'
        ]


class ProductsOfCategorySerializer(serializers.ModelSerializer):
    base_product = BaseProductOfCategorySerializer()

    class Meta:
        model = models.Product
        fields = [
            'id', 'base_product', 'slug', 'end_discount', 'discount_percent',
            'price', 'price_after_discount'
        ]


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
    

class BaseProductListStoreSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField()

    class Meta:
        model = models.Store
        fields = ['code', 'province']


class BaseProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    # store = BaseProductListStoreSerializer()

    class Meta:
        model = models.BaseProduct
        fields = ['id', 'category', 'title_farsi']


class ProductListSerializer(serializers.ModelSerializer):
    base_product = BaseProductListSerializer()
    # title_farsi = serializers.CharField(source='base_product.title_farsi')
    # category = serializers.CharField(source='base_product.category')
    
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
    

class BaseProductDetailCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CategoryProduct
        fields = ['id', 'name']


class BaseProductDetailSubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SubCategoryProduct
        fields = ['id', 'name']


class BaseProductDetailImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductImage
        fields = ['image', 'is_cover']


class BaseProductDetailStoreSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField()

    class Meta:
        model = models.Store
        fields = ['id', 'name', 'code', 'province']


class BaseProductDetailSerializer(serializers.ModelSerializer):
    properties = ProductPropertySerializer(many=True)
    comments = BaseProductDetailCommentSerializer(many=True)
    
    category = BaseProductDetailCategorySerializer()
    sub_category = BaseProductDetailSubCategorySerializer()
    product_type = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    sending_method = serializers.CharField(source='get_sending_method_display')

    images = BaseProductDetailImageSerializer(many=True)
    store = BaseProductDetailStoreSerializer()

    class Meta:
        model = models.BaseProduct
        fields = [
            'id', 'store', 'category', 'sub_category', 'product_type', 'product_code', 'brand',
            'title_farsi', 'title_english', 'description', 'product_authenticity', 'product_warranty',
            'sending_method', 'properties', 'comments', 'images'
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
    store_code = serializers.CharField(source='store.code')

    class Meta:
        model = models.BaseProduct
        fields = ['title_farsi', 'product_code', 'store_code', 'images']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            image = models.ProductImage.objects.get(product_id=instance.pk, is_cover=True)
        except models.ProductImage.DoesNotExist:
            image = None
        rep['images'] = CartItemBaseProductImageSerializer(image).data

        return rep


class CartItemProductSerializer(serializers.ModelSerializer):
    base_product = CartItemBaseProductSerializer()
    color = serializers.StringRelatedField()
    amount_discount = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ['id', 'base_product', 'color', 'slug', 'price', 'price_after_discount', 'amount_discount']

    def get_amount_discount(self, product):
        return int(product.price * (product.discount_percent / Decimal(100)))

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
    amount_discount_products = serializers.SerializerMethodField()
    amount_payable = serializers.SerializerMethodField()

    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'total_price_of_cart', 'coupon_discount_percent', 'amount_discount_products', 'amount_payable']
        read_only_fields = ['id', 'coupon_discount_percent']

    def get_total_price_of_cart(self, cart):
        return sum(item.product.price * item.quantity for item in cart.items.all())
    
    def get_amount_discount_products(self, cart):
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
            result = self.get_total_price_of_cart(cart)

        if cart.coupon_discount_percent and cart.amount_discount and cart.coupon_discount:
            result = result - cart.amount_discount
        return result
    

class OrderItemProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='base_product.title_farsi')
    cuttent_price = serializers.CharField(source='price')

    class Meta:
        model = models.Product
        fields = ['id', 'title', 'cuttent_price']
    

class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()

    class Meta:
        model = models.OrderItem
        fields = ['id', 'product', 'quantity', 'purchased_price']


class OrderCustomerSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(source='user.mobile')

    class Meta:
        model = models.Customer
        fields = ['mobile']
    

class OrderForAdminSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    order_status = serializers.CharField(source='get_order_status_display')
    customer = OrderCustomerSerializer()

    class Meta:
        model = models.Order
        fields = [
            'id', 'customer', 'order_status', 'status_paid', 'receiver_full_name', 'receiver_mobile', 'province', 'city',
            'neighbourhood', 'region', 'house_num', 'vahed', 'post_code', 'identification_code'
            'datetime_created', 'tracking_code', 'items'
        ]


class OrderForUserSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    province = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    neighbourhood = serializers.StringRelatedField()
    date = serializers.StringRelatedField()
    time = serializers.StringRelatedField()

    order_status = serializers.CharField(source='get_order_status_display')
    status_paid = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        fields = [
            'id', 'order_status', 'status_paid', 'receiver_full_name', 'receiver_mobile', 'province', 'city', 'neighbourhood',
            'region', 'house_num', 'vahed', 'post_code', 'identification_code', 'date', 'time',
            'datetime_created', 'tracking_code', 'total_price', 'items'
        ]

    def get_status_paid(self, order):
        if order.status_paid:
            return 'موفق'
        return 'ناموفق'


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

    date = serializers.IntegerField()
    time = serializers.IntegerField()

    def validate_cart_id(self, cart_id):
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
    
    def validate(self, attrs):
        date_pk = attrs['date']
        try:
            date_obj = models.OrderDate.objects.get(pk=date_pk)
        except models.Province.DoesNotExist:
            raise serializers.ValidationError('لطفا آیدی معتبر وارد کنید')

        # validation id of time
        time_pk = attrs['time']
        try:
            time_obj = models.OrderTime.objects.get(pk=time_pk)
        except models.Province.DoesNotExist:
            raise serializers.ValidationError('لطفا آیدی معتبر وارد کنید')
        return attrs
    
    def save(self, **kwargs):
        with transaction.atomic():
            data = self.validated_data

            cart_id = data['cart_id']
            user_id = self.context['user_id']

            customer = models.Customer.objects.get(user_id=user_id)
            cart = models.Cart.objects.get(pk=cart_id)

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
                date_id=data['date'],
                time_id=data['time'],
                total_price=cart.get_amount_payable(),
                discount_percent=cart.coupon_discount_percent
            )
            order.save()

            cart_items = models.CartItem.objects.select_related('product').filter(cart_id=cart_id)

            order_items = [
                models.OrderItem(
                    order=order,
                    product_id=cart_item.product_id,
                    purchased_price=cart_item.product.price,
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

            # models.Cart.objects.get(id=cart_id).delete()

            return order
        

class HaghighyStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HaghighyStore
        fields = [
            'id', 'name', 'mobile_number', 'phone_number', 'email', 'code', 'shomare_shaba',
            'province', 'city', 'mantaghe', 'mahalle', 'parvane_kasb', 'tasvire_personely',
            'kart_melli', 'shenasname', 'logo', 'roozname_rasmi_alamat', 'gharardad',
            'post_code', 'address', 'store_type',
            'full_name', 'birth_date', 'name_father', 'code_melli', 'shomare_shenasname',
        ]


class HoghoughyStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HoghoughyStore
        fields = [
            'id', 'name', 'mobile_number', 'phone_number', 'email', 'code', 'shomare_shaba',
            'province', 'city', 'mantaghe', 'mahalle', 'parvane_kasb', 'tasvire_personely',
            'kart_melli', 'shenasname', 'logo', 'roozname_rasmi_alamat', 'gharardad',
            'address', 'post_code', 'num_of_registration', 'store_type',
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


class OrderDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderDate
        fields = ['id', 'date']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep['time'] = timezone.localtime(instance.time)

        # tz = timezone.get_current_timezone()
        # rep['date'] = timezone.make_aware(instance.date, tz)

        return rep


class OrderTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderTime
        fields = ['id', 'time']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep['time'] = timezone.localtime(instance.time)

        tz = timezone.get_current_timezone()
        rep['time'] = timezone.make_aware(instance.time, tz)

        return rep
    

class RequestPhotographySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RequestPhotography
        fields = [
            'id', 'full_name', 'mobile', 'province', 'city', 'neighbourhood',
            'mahalle', 'address', 'store_name', 'request_text'
        ]


class SameProductStoreSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField()

    class Meta:
        model = models.Store
        fields = ['id', 'code', 'province']


class SameProductDetailSerializer(serializers.ModelSerializer):
    title_farsi = serializers.CharField(source='base_product.title_farsi')
    send_method = serializers.CharField(source='base_product.get_sending_method_display')

    class Meta:
        model = models.Product
        fields = [
            'id', 'title_farsi', 'slug', 'send_method', 'price', 'price_after_discount',
            'discount_percent', 'end_discount', 'datetime_created',
        ]


class SameProductsListSerializer(serializers.ModelSerializer):
    product = SameProductDetailSerializer()
    store = SameProductStoreSerializer()

    class Meta:
        model = models.SameProduct
        fields = ['store', 'product']


class ReportProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BaseProduct
        fields = ['title_farsi']


class ReportproductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReportProduct
        fields = ['product', 'text']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['product'] = ReportProductDetailSerializer(instance.product).data

        return rep
    

class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ContactUs
        fields = ['id', 'full_name', 'mobile', 'email', 'subject', 'text', 'tracking_code']
        read_only_fields = ['tracking_code']


class CouponDiscountSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    code = serializers.CharField(max_length=50)

    def validate_code(self, code):
        try:
            coupon = models.CouponDiscount.objects.get(code=code)
        except models.CouponDiscount.DoesNotExist:
            raise serializers.ValidationError('این کد معتبر نمی باشد')
        
        return code
        
    def validate_cart_id(self, cart_id):
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
    

class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Province
        fields = ['name']


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = ['name']


class neighbourhoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Neighbourhood
        fields = ['name']


class AddFavoriteProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


class FavoriteProductSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.base_product.title_farsi')
    user = serializers.StringRelatedField()

    class Meta:
        model = models.FavoriteProduct
        fields = ['user', 'product']


class AddLetMeKnowProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


class LetMeKnowProductSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.base_product.title_farsi')
    user = serializers.StringRelatedField()

    class Meta:
        model = models.LetMeKnowProduct
        fields = ['user', 'product']
