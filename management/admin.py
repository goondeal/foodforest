from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

class CountryAdmin(TranslationAdmin):
    pass

class StateAdmin(TranslationAdmin):
    pass

class CityAdmin(TranslationAdmin):
    pass


# Register your models here.
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
