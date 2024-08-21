from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...


@admin.register(models.SendingMethod)
class SendingMethodAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ShipingCost)
class ShipingCostAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ShipingRange)
class ShipingRangeAdmin(admin.ModelAdmin):
    ...
