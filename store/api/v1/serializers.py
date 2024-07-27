from rest_framework import serializers

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


class BaseProductDetailSerializer(serializers.ModelSerializer):
    properties = ProductPropertySerializer(many=True)
    
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
            'sending_method', 'properties'
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
