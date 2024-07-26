from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CategoryProduct(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    logo = models.ImageField(upload_to='categories_logo/')

    def __str__(self):
        return self.name


class SubCategoryProduct(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    logo = models.ImageField(upload_to='sub_categories_logo/')

    def __str__(self):
        return self.name


class ProductType(models.Model):
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='products_type')
    sub_category = models.ForeignKey(SubCategoryProduct, on_delete=models.CASCADE, related_name='products_type')

    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BaseProduct(models.Model):

    class ProductAuthenticity(models.TextChoices):
        ORIGINAL = 'o', _('اصل ، اوریجینال')

    class SendingMethod(models.TextChoices):
        TIPAX = 'ti', _('تیپاکس')
        POST_PISHTAZ = 'pi', _('پست پیشتاز')
        BAARBARI = 'ba', _('باربری')
        PEYK_MOTORI = 'mo', _('پیک موتوری')

    # store
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='products')
    sub_category = models.ForeignKey(SubCategoryProduct, on_delete=models.CASCADE, related_name='products')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')
    product_code = models.CharField(max_length=10)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')

    title_farsi = models.CharField(max_length=255)
    title_english = models.CharField(max_length=255)

    product_authenticity = models.CharField(max_length=2, choices=ProductAuthenticity.choices)
    product_warranty = models.BooleanField(default=True)
    sending_method = models.CharField(max_length=2, choices=SendingMethod.choices)

    def __str__(self):
        return self.title_farsi
