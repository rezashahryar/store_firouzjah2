from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.


class Province(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Neighbourhood(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='neighbourhoods')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductProperties(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class CategoryProduct(models.Model):
    properties = models.ManyToManyField(ProductProperties, related_name='categories')
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    logo = models.ImageField(upload_to='categories_logo/')

    def __str__(self):
        return self.name


class SubCategoryProduct(models.Model):
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='sub_categories', null=True)
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
    description = models.TextField(null=True)

    product_authenticity = models.CharField(max_length=2, choices=ProductAuthenticity.choices)
    product_warranty = models.BooleanField(default=True)
    sending_method = models.CharField(max_length=2, choices=SendingMethod.choices)

    def __str__(self):
        return self.title_farsi
    

class SetProductProperty(models.Model):
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='properties')
    property = models.ForeignKey(ProductProperties, on_delete=models.CASCADE)
    value = models.CharField(max_length=250)

    def __str__(self):
        return f'property {self.property} for {self.product.title_farsi} with value {self.value}'
    

class Size(models.Model):
    size = models.CharField(max_length=3)

    def __str__(self):
        return str(self.size)
    

class Color(models.Model):
    name = models.CharField(max_length=255)
    code_of_color = models.CharField(max_length=16, null=True)

    def __str__(self):
        return str(self.name)
    

class Product(models.Model):

    class ProductUnit(models.TextChoices):
        PAIR = 'pi', _('جفت')
        NUMBER = 'na', _('عددی')

    class ProductStatus(models.TextChoices):
        CONFIRM = 'c', _('تایید')
        WAITING = 'w', _('در انتظار تایید')
        NOT_CONFIRMED = 'n', _('عدم تایید')

    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='products')

    slug = models.SlugField(null=True)

    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='products')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='products')

    inventory = models.PositiveIntegerField()

    unit = models.CharField(max_length=2, choices=ProductUnit.choices)

    price = models.IntegerField()
    price_after_discount = models.IntegerField()
    discount_percent = models.PositiveIntegerField()

    start_discount = models.DateTimeField()
    end_discount = models.DateTimeField()

    length_package = models.IntegerField(null=True, blank=True)
    width_package = models.IntegerField(null=True, blank=True)
    height_package = models.IntegerField(null=True, blank=True)
    weight_package = models.IntegerField(null=True, blank=True)

    shenase_kala = models.CharField(max_length=14, null=True)
    barcode = models.CharField(max_length=16, null=True)

    product_status = models.CharField(max_length=1, choices=ProductStatus.choices, default=ProductStatus.WAITING)

    product_is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.base_product.title_farsi} - {self.color} - {self.size}'
    
    def save(self, *args, **kwargs):
        self.slug = self.generate_unique_slug(self.base_product.title_farsi, self.color.name, self.size.size)
        return super().save(*args, **kwargs)
    
    def generate_unique_slug(self, title, color, size):
        return f'{title}-{color}-{size}'
    

class ProductImage(models.Model):
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product-images/')
    is_cover = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title_farsi
    

class ProductComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='comments')

    text = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True)


class ProductAnswerComment(models.Model):
    comment = models.ForeignKey(ProductComment, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers_comments')

    text = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')


class Order(models.Model):

    class OrderStatus(models.TextChoices):
        UNPAID = 'u', _('پرداخت نشده')
        CANCELED = 'c', _('کنسل شده')
        PAID = 'p', _('پرداخت شده')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')

    receiver_full_name = models.CharField(max_length=255)
    receiver_mobile = models.CharField(max_length=11)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='orders')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='orders')
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, related_name='orders')
    region = models.CharField(max_length=255)
    house_num = models.CharField(max_length=55)

    vahed = models.CharField(max_length=3)
    post_code = models.CharField(max_length=10)
    identification_code = models.CharField(max_length=55)

    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=OrderStatus.choices, default=OrderStatus.UNPAID)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()

    class Meta:
        unique_together = [['order', 'product']]
