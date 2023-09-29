from modeltranslation.translator import translator, TranslationOptions
from .models import Country, State, City


class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)

class StateTranslationOptions(TranslationOptions):
    fields = ('name',)

class CityTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Country, CountryTranslationOptions)
translator.register(State, StateTranslationOptions)
translator.register(City, CityTranslationOptions)
