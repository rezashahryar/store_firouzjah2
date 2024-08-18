from rest_framework import serializers

from panel.models import Profile
from store import models as store_models

# create your serializers here


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
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
