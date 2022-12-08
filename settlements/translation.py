from modeltranslation.translator import translator, TranslationOptions
from .models import SettlementStatus


class SettlementStatusTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(SettlementStatus, SettlementStatusTranslationOptions)
