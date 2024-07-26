from rest_framework import serializers

from store import models

# create your serializers here


class BaseProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = models.BaseProduct
        fields = ['id', 'category', 'title_farsi']


class ProductListSerializer(serializers.ModelSerializer):
    base_product = BaseProductListSerializer()
    
    class Meta:
        model = models.Product
        fields = ['id', 'base_product', 'price', 'price_after_discount', 'end_discount', 'discount_percent']
