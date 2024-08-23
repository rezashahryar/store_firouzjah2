from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.SupportTicket)
class SuppportTicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'ticket_text', 'datetime_created', 'has_annex']

    def ticket_text(self, obj):
        return obj.text[:15]
    
    def has_annex(self, obj):
        if obj.annex:
            return 'has annex'
        else:
            return 'doesn\'t have annex'
        

@admin.register(models.AnswerSupportTicket)
class AnswerSupportTicketAdmin(admin.ModelAdmin):
    ...


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


@admin.register(models.RequestAddProduct)
class RequestAddProductAdmin(admin.ModelAdmin):
    ...
