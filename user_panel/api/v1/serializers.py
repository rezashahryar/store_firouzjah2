from rest_framework import serializers
from django.contrib.auth import get_user_model

from store import models as store_models

# create your serializers here


class CreateBaseProductSerializer(serializers.ModelSerializer):
    store_code = serializers.CharField(source='store.code')

    class Meta:
        model = store_models.BaseProduct
        fields = [
            'id', 'store_code', 'category', 'sub_category', 'product_type', 'product_code',
            'brand', 'title_farsi', 'title_english', 'description', 'product_authenticity',
            'product_warranty', 'sending_method'
        ]


class CreateProductSerializer(serializers.ModelSerializer):
    base_product = CreateBaseProductSerializer()

    class Meta:
        model = store_models.Product
        fields = [
            'id', 'base_product', 'size', 'color', 'inventory', 'unit', 'price',
            'price_after_discount', 'discount_percent', 'start_discount', 'end_discount',
            'length_package', 'width_package', 'height_package', 'weight_package',
            'shenase_kala', 'barcode',
        ]
