from rest_framework import serializers

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
