from django.contrib import admin
from .models import Settlement, SettlementStatus
from modeltranslation.admin import TranslationAdmin


class SettlementStatusAdmin(TranslationAdmin):
    pass


# Register your models here.
admin.site.register(SettlementStatus, SettlementStatusAdmin)
admin.site.register(Settlement)
