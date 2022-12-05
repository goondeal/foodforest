from django.contrib import admin
from .models import Order, OrderItem, OrderStatus, OrderType
from modeltranslation.admin import TranslationAdmin


class OrderStatusAdmin(TranslationAdmin):
    pass

class OrderTypeAdmin(TranslationAdmin):
    pass


# Register your models here.
admin.site.register(OrderStatus, OrderStatusAdmin)
admin.site.register(OrderType, OrderTypeAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
