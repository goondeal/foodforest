from modeltranslation.translator import translator, TranslationOptions
from .models import OrderStatus, OrderType


class OrderStatusTranslationOptions(TranslationOptions):
    fields = ('title',)

class OrderTypeTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(OrderStatus, OrderStatusTranslationOptions)
translator.register(OrderType, OrderTypeTranslationOptions)
