import random

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
    

def random_code_store():

    while True:
        code = random.randint(100000, 999999)

        if Store.objects.filter(code=code).exists():
            continue
        return code


class Store(models.Model):

    class StoreType(models.TextChoices):
        HAGHIGHY = "ha", _("حقیقی")
        HOGHOUGHY = "ho", _("حقوقی")
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='store', null=True)

    name = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=11)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField()
    code = models.CharField(max_length=6, unique=True, default=random_code_store)
    
    shomare_shaba = models.CharField(max_length=26)

    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='stores')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='stores')
    mantaghe = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, related_name='stores')
    mahalle = models.CharField(max_length=255)

    address = models.CharField(max_length=555)
    post_code = models.CharField(max_length=10)

    parvane_kasb = models.FileField(upload_to='parvane_kasb__/%Y/%m/%d/')
    tasvire_personely = models.ImageField(upload_to='tasvire_personely__/%Y/%m/%d/')
    kart_melli = models.ImageField(upload_to='kart_melli__/%Y/%m/%d/')
    shenasname = models.ImageField(upload_to='tasvire_shenasname__/%Y/%m/%d/')
    logo = models.ImageField(upload_to='logo__/%Y/%m/%d/')
    roozname_rasmi_alamat = models.FileField(upload_to='roozname_rasmi_alamat__/%Y/%m/%d/')

    gharardad = models.FileField(upload_to='gharardad__/%Y/%m/%d/')

    store_type = models.CharField(max_length=2, choices=StoreType.choices)

    def __str__(self):

        if self.name:
            return str(self.name)
        else:
            return str(self.mobile_number)


class HaghighyStore(Store):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    name_father = models.CharField(max_length=255)
    code_melli = models.CharField(max_length=10, unique=True)
    shomare_shenasname = models.CharField(max_length=255)

    def __str__(self):
        return str(self.full_name)


class HoghoughyStore(Store):
    ceo_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    date_of_registration = models.DateField()
    num_of_registration = models.CharField(max_length=255)
    economic_code = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name


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

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products', null=True)
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='products')
    sub_category = models.ForeignKey(SubCategoryProduct, on_delete=models.CASCADE, related_name='products')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products', null=True)
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

    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='products', null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='products', null=True)

    inventory = models.PositiveIntegerField()

    unit = models.CharField(max_length=2, choices=ProductUnit.choices)

    price = models.IntegerField()
    price_after_discount = models.IntegerField(null=True, blank=True)
    discount_percent = models.PositiveIntegerField(null=True, blank=True)

    start_discount = models.DateTimeField(null=True)
    end_discount = models.DateTimeField(null=True)

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
        self.slug = self.generate_unique_slug(self.base_product.pk, self.color.name, self.size.size)
        return super().save(*args, **kwargs)
    
    def generate_unique_slug(self, id, color, size):
        return f'{id}--{color}--{size}'
    

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

    def get_total_price_of_cart(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    def get_amount_payable(self):
        result = None
        for item in self.items.all():
            if item.product.discount_percent and item.product.price_after_discount:
                result = self.get_total_price_of_cart() - sum(item.quantity * item.product.price_after_discount for item in self.items.all())
                return result
            result = self.get_total_price_of_cart()
        return result


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
        return self.user.mobile
    

class OrderDateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)
    

class OrderDate(models.Model):
    date = models.DateField()
    status = models.BooleanField(default=True)

    objects = models.Manager()
    active = OrderDateManager()

    def __str__(self):
        return str(self.date)
    

class OrderTimeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)
    

class OrderTime(models.Model):
    time = models.TimeField()
    status = models.BooleanField(default=True)

    objects = models.Manager()
    active = OrderTimeManager()

    def __str__(self):
        return str(self.time)


class Order(models.Model):

    class OrderStatus(models.TextChoices):
        CURRENT_ORDERS = 'co', _('جاری')
        ORDERS_DELIVERED = 'd', _('تحویل شده')
        RETURN_ORDERS = 'r', _('مرجوعی')
        CANCELED = 'c', _('لغو شده')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')

    date = models.ForeignKey(OrderDate, on_delete=models.SET_NULL, null=True, related_name='orders')
    time = models.ForeignKey(OrderTime, on_delete=models.SET_NULL, null=True, related_name='orders')

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

    total_price = models.IntegerField(null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=2, choices=OrderStatus.choices, default=OrderStatus.CURRENT_ORDERS)
    status_paid = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    purchased_price = models.IntegerField()

    class Meta:
        unique_together = [['order', 'product']]


class RequestPhotography(models.Model):
    full_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=11)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='requests_photography')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='requests_photography')
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, related_name='requests_photography')
    mahalle = models.CharField(max_length=255)
    address = models.TextField()
    store_name = models.CharField(max_length=255)
    request_text = models.TextField()


class SameProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='same_products', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='same_products')


class ReportProduct(models.Model):
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='reports')
    text = models.TextField()


def generate_tracking_code():
    code = random.randint(100000000, 999999999)
    return code


class ContactUs(models.Model):
    full_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=11)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    text = models.TextField()
    tracking_code = models.CharField(max_length=9, unique=True, default=generate_tracking_code)
