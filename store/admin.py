from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    ...


@admin.register(models.SubCategoryProduct)
class SubCategoryProduct(admin.ModelAdmin):
    ...


@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    ...


@admin.register(models.BaseProduct)
class BaseProductAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    ...
