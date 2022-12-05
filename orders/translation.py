from modeltranslation.translator import translator, TranslationOptions
from .models import OrderStatus, OrderType


class OrderStatusTranslationOptions(TranslationOptions):
    fields = ('title',)

class OrderTypeTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(OrderStatus, OrderStatusTranslationOptions)
translator.register(OrderType, OrderTypeTranslationOptions)
