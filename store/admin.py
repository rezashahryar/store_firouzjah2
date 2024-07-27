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
    prepopulated_fields = {"slug": ('base_product', )}


@admin.register(models.ProductProperties)
class ProductPropertiesAdmin(admin.ModelAdmin):
    ...


@admin.register(models.SetProductProperty)
class SetProductPropertyAdmin(admin.ModelAdmin):
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


@admin.register(models.ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ProductAnswerComment)
class ProductAnswerCommentAdmin(admin.ModelAdmin):
    ...
