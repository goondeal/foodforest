from modeltranslation.translator import translator, TranslationOptions
from .models import FoodCategory, RestaurantStatus, MenuItemFeatureCategory, MenuItemFeature

class RestaurantStatusTranslationOptions(TranslationOptions):
    fields = ('title',)

class FoodCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

class MenuItemFeatureCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

class MenuItemFeatureTranslationOptions(TranslationOptions):
    fields = ('title',)    


translator.register(RestaurantStatus, RestaurantStatusTranslationOptions)
translator.register(FoodCategory, FoodCategoryTranslationOptions)
translator.register(MenuItemFeatureCategory, MenuItemFeatureCategoryTranslationOptions)
translator.register(MenuItemFeature, MenuItemFeatureTranslationOptions)